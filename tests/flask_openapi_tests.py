from datetime import datetime, timedelta

import pytest

from models import Client, ClientParking, Parking


@pytest.mark.parametrize("route", ["/api/clients/", "/api/clients/1", "/"])
def test_route_status_get_all(client, route):
    """Проверка всех get роутов на статус 200"""
    rv = client.get(route)
    assert rv.status_code == 200


@pytest.mark.parametrize("route", ["/api/clients/2"])
def test_route_status_get(client, route):
    """Проверка get роута на статус 404, если нет в базе клиента"""
    rv = client.get(route)
    assert rv.status_code == 404


def test_create_client(client):
    """Проверка post роута на статус 201, добавление клиента"""
    client_data = {
        "name": "Лев",
        "surname": "Толстой",
        "credit_card": "1455 1211 1489 0006",
        "car_number": "ТЕЛЕГА",
    }

    resp = client.post("/api/clients/", json=client_data)

    assert resp.status_code == 201
    assert "Добавлен клиент:" in resp.json


def test_create_parking(client):
    """Проверка post роута на статус 201, добавление парк зоны"""
    parking_data = {
        "address": "Крассная д.2",
        "opened": True,
        "count_places": 3,
        "count_available_places": 3,
    }

    resp = client.post("/api/parkings/", json=parking_data)

    assert resp.status_code == 201
    assert "Добавлена парковочная зона:" in resp.json


@pytest.mark.parking
def test_parking_in_success(client, db):
    """Тест успешного заезда"""
    resp = client.post(
        "/api/clients_parkings/to/", json={"client_id": 1, "parking_id": 1}
    )
    assert resp.status_code == 201
    assert db.session.get(Parking, 1).count_available_places == 9


@pytest.mark.parking
def test_parking_in_when_full(client, db):
    """Тест заезда на заполненную парковку"""
    parking = db.session.get(Parking, 1)
    parking.count_available_places = 0
    parking.opened = False
    db.session.commit()

    resp = client.post(
        "/api/clients_parkings/to/", json={"client_id": 1, "parking_id": 1}
    )
    assert resp.status_code == 403


@pytest.mark.parking
def test_parking_out_success(client, db):
    """Тест успешного выезда"""
    client_obj = db.session.get(Client, 1)
    print("\nInitial client:", client_obj.__dict__)
    client_obj.credit_card = "0000 0000 0000 0000"
    db.session.commit()

    cp = ClientParking(
        client_id=1, parking_id=1, time_in=datetime.now() - timedelta(hours=1)
    )
    db.session.add(cp)
    db.session.commit()

    resp = client.put(
        "/api/clients_parkings/out/", json={"client_id": 1, "parking_id": 1}
    )

    assert resp.status_code == 201
    assert "Обновлена запись:" in resp.json
    assert "Пробыл" in resp.json

    parking = db.session.get(Parking, 1)
    assert parking.count_available_places == 11


@pytest.mark.parking
def test_parking_out_no_card(client, db):
    """Тест выезда без карты"""
    client_obj = db.session.get(Client, 1)
    client_obj.credit_card = None
    db.session.commit()

    ClientParking(client_id=1, parking_id=1, time_in=datetime.now())
    db.session.commit()

    resp = client.put(
        "/api/clients_parkings/out/", json={"client_id": 1, "parking_id": 1}
    )

    assert resp.status_code == 403
    assert "не найдена" in resp.json["Error"]
