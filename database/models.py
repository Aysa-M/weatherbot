# Database models
from datetime import datetime

from sqlalchemy import (BigInteger, Column, DateTime,
                        Integer, ForeignKey, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Базовый класс для декларативных определений классов, т.е. данная функция
# позволяет нам определять таблицы и модели одновременно.
Base = declarative_base()


class Users(Base):  # type: ignore
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False)
    city = Column(String, nullable=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    reports = relationship('WeatherReports', backref='report',
                           lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.tg_id


class WeatherReports(Base):  # type: ignore
    __tablename__ = 'weatherreports'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.now, nullable=False)
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_mm = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return self.city
