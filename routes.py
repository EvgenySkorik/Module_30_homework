from typing import List

from flask_openapi3 import APIBlueprint, Tag

from models import Client
from repository import ClientRepository, CPRepository, ParkingRepository
from shemas import (ClientIdShema, ClientShema, ClientShemaOUT, CPShema,
                    CPShemaDel, ParkingShema)

index_bp = APIBlueprint("index", __name__)
clients_bp = APIBlueprint("clients", __name__, url_prefix="/api/clients")
parkings_bp = APIBlueprint("parkings", __name__, url_prefix="/api/parkings")
cp_bp = APIBlueprint("clients_parkings", __name__, url_prefix="/api/clients_parkings")

cli_tag = Tag(name="Клиенты 😎", description="Ручки с клиентами")
park_tag = Tag(name="Парковки 🅿️", description="Ручки с паковками")
cp_tag = Tag(name="Действия 🚗", description="Ручки с действиями клиента к парковке")


@index_bp.get("/", summary="Стартовая")
def main():
    return "Привет, это паркинг!"


# Ручки клиента


@clients_bp.get("/", summary="Список всех клиентов", tags=[cli_tag])
def get_clients() -> List[dict]:
    """Получение списка клиентов"""
    clients = ClientRepository.get_all_clients_db()
    return clients


@clients_bp.post("/", summary="Добавить клиента", tags=[cli_tag])
def add_client(body: ClientShema):
    """Создание клиента"""
    try:
        new_client = ClientRepository.add_client_db(body)
        return {"Добавлен клиент:": f"{new_client}"}, 201
    except ValueError as e:
        return {"Error": str(e)}, 409


@clients_bp.delete("/<int:client_id>", summary="Удалить клиента", tags=[cli_tag])
def delete_client(path: ClientIdShema):
    """Удаление клиента"""
    client_id = ClientRepository.delete_client_db(path.client_id)
    if client_id:
        return {"Клиент с ID": f"{path.client_id} удалён"}, 200
    else:
        return {f"Клиент c ID {path.client_id}": "не найден"}, 404


@clients_bp.get("/<int:client_id>", summary="Информация клиента по ID", tags=[cli_tag])
def get_client_by_id(path: ClientIdShema):
    """Информация клиента по ID"""
    client = ClientRepository.get_client_by_id_db(path.client_id)
    if client:
        return client, 200
    return {f"Клиент c ID {path.client_id}": "не найден"}, 404


@parkings_bp.post("/", summary="Добавить парковку", tags=[park_tag])
def add_parking(body: ParkingShema):
    """Создание парковочной зоны"""
    try:
        new_parking = ParkingRepository.add_parking_db(body)
        return {"Добавлена парковочная зона:": f"{new_parking}"}, 201
    except ValueError as e:
        return {"Error": str(e)}, 409


@cp_bp.post("/to/", summary="Заезд на парковку", tags=[cp_tag])
def add_cl_to_park(body: CPShema):
    """Роут добавления записи при въезде"""
    try:
        new_cp = CPRepository.client_in_to_parking_db(body)
        return {"Добавлена запись:": f"{new_cp}"}, 201
    except ValueError as e:
        return {"Error": str(e)}, 403


@cp_bp.put("/out/", summary="Выезд с парковки", tags=[cp_tag])
def add_cl_out_park(body: CPShema):
    """Роут обновления записи при выезде"""
    try:
        new_cp = CPRepository.client_out_of_parking_db(body)
        return {"Обновлена запись:": f"{new_cp[0]}", "Пробыл": f"{new_cp[1]}"}, 201
    except ValueError as e:
        return {"Error": str(e)}, 403


@cp_bp.delete("/<int:id>", summary="Удаление записи из client_parking", tags=[cp_tag])
def delete_cp(path: CPShemaDel):
    """Удаление записи из client_parking"""
    cp_id = CPRepository.delete_cp_db(path.id)
    if cp_id:
        return {"Запись с ID": f"{path.id} удалён"}, 200
    else:
        return {f"Запись c ID {path.id}": "не найден"}, 404
