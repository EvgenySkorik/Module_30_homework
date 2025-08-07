from datetime import datetime
from typing import List

from database import db
from loging import get_logger
from models import Client, ClientParking, Parking
from shemas import ClientShema, ClientShemaOUT, CPShema, ParkingShema, ParkingShemaOUT

rep_logger = get_logger()


class ClientRepository:
    @classmethod
    def check_client(cls, data_client: ClientShema) -> bool:
        """Проверка наличия клиента в базе"""
        return (
            db.session.query(Client)
            .filter(
                Client.name == data_client.name, Client.surname == data_client.surname
            )
            .first()
            is not None
        )

    @classmethod
    def add_client_db(cls, data_client: ClientShema) -> ClientShemaOUT:
        """Добавление в базу нового клиента"""
        if isinstance(data_client, dict):
            # Если пришел dict, преобразуем в схему
            data_client = ClientShema(**data_client)

        if cls.check_client(data_client):
            raise ValueError(
                f"Клиент {data_client.name} {data_client.surname} уже существует"
            )

        client = Client(**data_client.model_dump())
        db.session.add(client)
        db.session.commit()

        return ClientShemaOUT.model_validate(client, from_attributes=True)

    @classmethod
    def get_all_clients_db(cls) -> List[dict]:
        """Получает список всех клиентов из базы данных"""
        clients = db.session.query(Client).all()
        return [cl.to_json() for cl in clients]

    @classmethod
    def delete_client_db(cls, client_id):
        """Удаляет клиента из базы данных"""
        deleted = db.session.query(Client).filter(Client.id == client_id).delete()
        db.session.commit()
        return bool(deleted)

    @classmethod
    def get_client_by_id_db(cls, client_id):
        """Получить из БД инфо по клиенту"""
        client = db.session.query(Client).filter(Client.id == client_id).one_or_none()
        return client.to_json() if client else None


class ParkingRepository:
    @classmethod
    def check_parking(cls, data_client: ParkingShema) -> bool:
        """Проверка наличия парковочной зоны в базе"""
        return (
            db.session.query(Parking)
            .filter(Parking.address == data_client.address)
            .first()
            is not None
        )

    @classmethod
    def add_parking_db(cls, data_parking: ParkingShema) -> ParkingShemaOUT:
        """Добавление в базу новой парковочной зоны"""
        if cls.check_parking(data_parking):
            raise ValueError(
                f"Парковочная зона по адресу {data_parking.address} уже существует"
            )
        parking = Parking(**data_parking.model_dump())
        db.session.add(parking)
        db.session.commit()

        return ParkingShemaOUT.model_validate(parking, from_attributes=True)


class CPRepository:
    @classmethod
    def client_in_to_parking_db(cls, cp_data: CPShema):
        parking: Parking = (
            db.session.query(Parking)
            .filter(Parking.id == cp_data.parking_id)
            .one_or_none()
        )
        if not parking:
            raise ValueError("Парковки не существует")
        if not parking.opened:
            raise ValueError("Парковка закрыта, мест нет")

        check_unic = (
            db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == cp_data.client_id,
                ClientParking.parking_id == cp_data.parking_id,
                ClientParking.time_out.is_(None),
            )
            .first()
        )

        if check_unic:
            raise ValueError("Клиент уже на парковке")

        cp = ClientParking(
            client_id=cp_data.client_id,
            parking_id=cp_data.parking_id,
            time_in=datetime.now(),
        )

        parking.count_available_places -= 1
        if parking.count_available_places <= 0:
            parking.opened = False

        db.session.add(cp)
        db.session.commit()

        return cp

    @classmethod
    def client_out_of_parking_db(cls, cp_data: CPShema):
        """
        Получаем данные из базы по client_parking, parking, client,
        Обновляем запись при выезде из парковки в БД,
        Проверка кредитной карты у клиента, МОЖЕМ ВСТАВИТЬ ЛОГИКУ ОПЛАТЫ
        """
        cp = (
            db.session.query(ClientParking, Parking, Client)
            .join(Parking)
            .join(Client)
            .filter(
                ClientParking.client_id == cp_data.client_id,
                ClientParking.parking_id == cp_data.parking_id,
                ClientParking.time_out.is_(None),
            )
            .first()
        )

        if not cp:
            raise ValueError("Активная запись о парковке не найдена")

        client_parking, parking, client = cp

        if not client.credit_card:
            raise ValueError("Просьба обновить данные кредитной карты!")

        # Тут должна быть логика оплаты!

        client_parking.time_out = datetime.now()

        parking.count_available_places += 1
        if not parking.opened and parking.count_available_places > 0:
            parking.opened = True

        db.session.commit()

        return client_parking, client_parking.time_out - client_parking.time_in

    @classmethod
    def delete_cp_db(cls, cp_id):
        """Удаляет cp из базы данных"""
        deleted = (
            db.session.query(ClientParking).filter(ClientParking.id == cp_id).delete()
        )
        db.session.commit()
        return bool(deleted)
