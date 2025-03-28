import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Doctor(SqlAlchemyBase):
    __tablename__ = 'doctors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    service_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("services.id"))

    services = orm.relationship('Service', back_populates="doctors")