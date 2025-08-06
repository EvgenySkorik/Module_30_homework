from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.sql.ddl import CreateTable

from database import Base, db


class Client(Base):
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    credit_card: Mapped[str | None] = mapped_column(String(50))
    car_number : Mapped[str | None] = mapped_column(String(10))

    parkings = relationship(
        "ClientParking", back_populates="client", cascade="all, delete-orphan", passive_deletes=True
    )

class Parking(Base):
    __tablename__ = "parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    opened: Mapped[bool] = mapped_column(nullable=True)
    count_places: Mapped[int] = mapped_column(nullable=False)
    count_available_places: Mapped[int] = mapped_column(nullable=False)

    clients = relationship(
        "ClientParking", back_populates="parking", cascade="all, delete-orphan", passive_deletes=True
    )

class ClientParking(Base):
    __tablename__ = "client_parking"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id", ondelete="CASCADE"))
    parking_id: Mapped[int] = mapped_column(ForeignKey("parking.id", ondelete="CASCADE"))
    time_in: Mapped[datetime] = mapped_column(nullable=True)
    time_out: Mapped[datetime] = mapped_column(nullable=True)

    client = relationship("Client", back_populates="parkings")
    parking = relationship("Parking", back_populates="clients")


    __table_args__ = (
        db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

# print(str(CreateTable(Client.__table__)))
# print(str(CreateTable(Parking.__table__)))
# print(str(CreateTable(ClientParking.__table__)))