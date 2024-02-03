# Functions for manipulations with database
from .models import Base, Users
from settings.db_config import engine, session


Base.metadata.create_all(engine)


def add_user(tg_id):
    user = session.query(Users).filter(Users.tg_id == tg_id).first()
