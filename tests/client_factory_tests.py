from models import Client, Parking

from ..tests.client_factory import ClientFactory, ParkingFactory


def test_create_client(client, db):
    """Проверка post роута на статус 201, добавление клиента"""
    initial_count = db.session.query(Client).count()

    client_obj = ClientFactory.build()
    resp = client.post("/api/clients/", json=client_obj.to_json())
    assert resp.status_code == 201
    assert "Добавлен клиент:" in resp.json
    assert db.session.query(Client).count() == initial_count + 1
    assert "id" in resp.json["Добавлен клиент:"]


# def test_create_client_many(client, db):
#     """Проверка массового post роута на статус 201, добавление клиента"""
#     CLIENT_COUNT = 50
#     for idx in range(2, CLIENT_COUNT):
#         client_obj = ClientFactory.build()
#         resp = client.post("/api/clients/", json=client_obj.to_json())
#         print(db.session.get(Client, idx))
#         assert resp.status_code == 201
#         assert "Добавлен клиент:" in resp.json


def test_create_parking(client, db):
    """Проверка post роута на статус 201, добавление парк зоны"""
    initial_count = db.session.query(Parking).count()

    parking_data = ParkingFactory.build()
    resp = client.post("/api/parkings/", json=parking_data.to_json())

    assert resp.status_code == 201
    assert "Добавлена парковочная зона:" in resp.json
    assert db.session.query(Parking).count() == initial_count + 1
    assert "id" in resp.json["Добавлена парковочная зона:"]
