from typing import Iterator

import pytest
from flask.testing import FlaskClient

from wainlog.app import app


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["PRESERVE_CONTEXT_ON_EXCEPTION"] = False

    with app.test_client() as client:
        yield client
