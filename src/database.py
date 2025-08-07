# mypy: ignore-errors
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


class Base(db.Model):  # type: ignore[name-defined]
    __abstract__ = True

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return f"{self.__class__.__name__}({data})"
