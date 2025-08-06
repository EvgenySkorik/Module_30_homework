from pydantic import BaseModel


class ClientShema(BaseModel):
    name: str
    surname: str
    credit_card: str | None
    car_number: str | None


class ClientShemaOUT(ClientShema):
    id: int


class ClientIdShema(BaseModel):
    client_id: int


class ParkingShema(BaseModel):
    address: str
    opened: bool
    count_places: int | None
    count_available_places: int | None


class ParkingShemaOUT(ParkingShema):
    id: int


class CPShema(BaseModel):
    client_id: int
    parking_id: int


class CPShemaDel(BaseModel):
    id: int
