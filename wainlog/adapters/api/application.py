import enum
from typing import Optional, cast

from flask import Flask, g
from flask_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...adapters.postgres import persister
from ..config import Config, get_config
from . import views


def create_app(config: Optional[Config] = None) -> Flask:

    app = Flask(__name__)

    if config is None:
        config = get_config()

    app.config["DB_URL"] = config.DB_URL
    app.config["SECRET_KEY"] = config.SECRET_KEY

    engine = create_engine(
        url=config.DB_URL,
    )
    session_cls = sessionmaker(bind=engine)

    @app.before_request
    def create_db_session() -> None:
        g.app_config = config
        g.session = session_cls()

    @app.teardown_appcontext
    def shutdown_session(_exception: Optional[Exception] = None) -> None:
        if hasattr(g, "session"):
            g.session.close()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(id):
        return persister.get_user_db_from_id(session=g.session, id=id)

    @app.template_filter("beautify_enum")
    def beautify_enum(enum_member: enum.Enum) -> str:
        return cast(str, enum_member.value.lower().replace("_", " ").title())

    app.register_blueprint(blueprint=views.bp)

    return app
