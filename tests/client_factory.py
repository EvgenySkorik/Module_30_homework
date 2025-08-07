import factory
from faker import Faker

from src.database import db
from src.models import Client, Parking

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    # credit_card = None
    # car_number = None

    credit_card = factory.LazyAttribute(
        lambda x: fake.credit_card_number() if fake.boolean(70) else None
    )
    car_number = factory.Faker("license_plate")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_places = factory.Faker("random_int", min=5, max=50)
    count_available_places = factory.LazyAttribute(
        lambda o: o.count_places if o.opened else 0
    )
