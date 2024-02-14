from dataclasses import dataclass

from environs import Env


CONST_1: int = 1
CONST_2: int = 2
CONV_DISPLAY: int = 4


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_credentials(path: str | None = None) -> Config:
    """
    Создаем функцию, которая будет читать файл .env и возвращать экземпляр
    класса Config с заполненными полями token
    Args:
        path (str | None): _description_
    """
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')))
