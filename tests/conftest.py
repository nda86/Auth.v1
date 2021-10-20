import sys
from pathlib import Path

import pytest
from flask.testing import FlaskClient

sys.path.append(str(Path(__file__).parent.parent))
from src import create_app # noqa


@pytest.fixture(scope="session")
def flask_client() -> FlaskClient:
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client
