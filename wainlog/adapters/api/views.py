import secrets
from urllib.parse import urlencode

import requests
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_user, logout_user
from werkzeug import Response

from ...core import types
from ..postgres import model, persister
from . import forms, view_functions

bp = Blueprint(name="wainlog", import_name=__name__, url_prefix="/")


@bp.route("/", methods=["GET", "POST"])
def root() -> str | Response:
    fells_by_book = view_functions.get_fells_by_book(session=g.session)
    summit_events: list[types.SummitEvent] | None = None

    if current_user.is_authenticated:
        add_summit_form = forms.AddSummitEvent()
        delete_summit_form = forms.DeleteSummitEvent()

        if add_summit_form.validate_on_submit():
            persister.add_summit_event(
                session=g.session,
                user_id=current_user.get_id(),
                fell_name=types.FellName(add_summit_form.fell_name.data),
                summit_date=add_summit_form.date.data,
            )
            g.session.commit()
            summit_events = persister.get_summit_events_for_user(
                session=g.session, username=current_user.username
            )
            return redirect(url_for("wainlog.root"))
        elif delete_summit_form.validate_on_submit():
            persister.delete_summit_event(
                session=g.session,
                user_id=current_user.get_id(),
                fell_name=types.FellName(delete_summit_form.fell_name.data),
            )
            g.session.commit()
            summit_events = persister.get_summit_events_for_user(
                session=g.session, username=current_user.username
            )
            return redirect(url_for("wainlog.root"))

        summit_events = persister.get_summit_events_for_user(
            session=g.session, username=current_user.username
        )
        return render_template(
            "root.html",
            fells_by_book=fells_by_book,
            summit_events=summit_events,
            add_summit_form=add_summit_form,
            delete_summit_form=delete_summit_form,
        )

    return render_template(
        "root.html",
        fells_by_book=fells_by_book,
        summit_events=summit_events,
    )


@bp.route("/authorize/<provider>", methods=["GET"])
def oauth2_authorize(provider: str) -> Response:
    if not current_user.is_anonymous:
        return redirect(url_for("wainlog.root"))

    session["oauth2_state"] = secrets.token_urlsafe(16)

    query_string = urlencode(
        {
            "client_id": current_app.config["GOOGLE_OAUTH_CLIENT_ID"],
            "redirect_uri": url_for(
                "wainlog.oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(current_app.config["GOOGLE_OAUTH_SCOPES"]),
            "state": session["oauth2_state"],
        }
    )

    return redirect(
        current_app.config["GOOGLE_OAUTH_AUTHORIZE_URL"] + "?" + query_string
    )


@bp.route("/callback/<provider>", methods=["GET"])
def oauth2_callback(provider: str) -> Response:  # noqa: C901
    if not current_user.is_anonymous:
        return redirect(url_for("wainlog.root"))

    if "error" in request.args:
        for k, v in request.args.items():
            if k.startswith("error"):
                flash(f"{k}: {v}")
        return redirect(url_for("index"))

    if request.args["state"] != session.get("oauth2_state"):
        abort(401)

    if "code" not in request.args:
        abort(401)

    response = requests.post(
        current_app.config["GOOGLE_OAUTH_TOKEN_URL"],
        data={
            "client_id": current_app.config["GOOGLE_OAUTH_CLIENT_ID"],
            "client_secret": current_app.config["GOOGLE_OAUTH_CLIENT_SECRET"],
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": url_for(
                "wainlog.oauth2_callback", provider=provider, _external=True
            ),
        },
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get("access_token")
    if not oauth2_token:
        abort(401)

    response = requests.get(
        current_app.config["GOOGLE_OAUTH_USERINFO_URL"],
        headers={
            "Authorization": "Bearer " + oauth2_token,
            "Accept": "application/json",
        },
    )
    if response.status_code != 200:
        abort(401)
    email = response.json()["email"]

    user = persister.get_user_db_from_email(g.session, email)
    if user is None:
        user = model.User(email=email, username=email.split("@")[0])
        persister.add_user(g.session, user)
        g.session.commit()

    login_user(user)
    return redirect(url_for("wainlog.root"))


@bp.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("wainlog.root"))
