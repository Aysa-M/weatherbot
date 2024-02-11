# Functions for manipulations with database
from typing import Optional

from .models import Base, Users, WeatherReports
from settings.db_config import engine, Session


Base.metadata.create_all(engine)
SESSION = Session()


def get_user(tg_id: int) -> Users | None:
    return SESSION.query(Users).filter(Users.tg_id == tg_id).first()


def add_user(tg_id: int) -> None:
    """
    Записывает нового пользователя в БД, если его id отсутствует.
    Args:
        tg_id (int): id telegram user
    """
    user: Optional[Users] = get_user(tg_id)
    if user is None:
        new_user: Users = Users(tg_id=tg_id)
        SESSION.add(new_user)
        SESSION.commit()


def set_user_city(tg_id: int, location: str):
    """
    Запись и обработка ввода родного города для пользователя
    Args:
        tg_id (int): id пользователя
        location (str): введенный город проживания пользователя
    """
    user: Optional[Users] = get_user(tg_id)
    user.city = location
    SESSION.commit()


def get_user_location(tg_id: int) -> str:
    """
    Получаем город пользователя, установленный как "свой"
    """
    user: Optional[Users] = get_user(tg_id)
    return user.city


def create_report(tg_id: int, temp: int, feels_like: int,
                  wind_speed: int, pressure_mm: int, location: str):
    """
    Запись отчета в БД
    """
    user: Optional[Users] = get_user(tg_id)
    new_report: Optional[WeatherReports] = WeatherReports(
        temp=temp, feels_like=feels_like, wind_speed=wind_speed,
        pressure_mm=pressure_mm, city=location, owner=user.id)
    SESSION.add(new_report)
    SESSION.commit()


def get_reports(tg_id: int):
    """
    Получаем все запрошенные отчеты по погоде пользователя
    """
    return get_user(tg_id).reports
