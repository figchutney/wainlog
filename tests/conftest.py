import pytest
from flask.testing import FlaskClient

from wainlog import wainlog


@pytest.fixture
def client() -> FlaskClient:
    wainlog.app.config["DEBUG"] = True
    wainlog.app.config["TESTING"] = True
    wainlog.app.config["PROPAGATE_EXCEPTIONS"] = False
    wainlog.app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

    with wainlog.app.test_client() as client:
        yield client
