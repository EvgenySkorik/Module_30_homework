import os
import sys

import pytest

hw_path = os.path.dirname(os.path.dirname(__file__))  # noqa: E402
sys.path.insert(0, hw_path)  # noqa: E402

from app import create_app  # noqa: E402
from src.database import db as _db  # noqa: E402
from src.models import Client, Parking  # noqa: E402


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        cl1 = Client(
            name="Алесандр",
            surname="Македонский",
            credit_card="4514 5585 3012 4411",
            car_number="В777ОР77",
        )
        park = Parking(
            address="г. Москва, ул. Тверская, 11с2",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        _db.session.add(cl1)
        _db.session.add(park)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
