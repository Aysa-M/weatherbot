import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.user_handlers import usrouter
from settings.bot_config import Config, load_credentials


logger = logging.getLogger(__name__)


async def main():
    """
    Точка входа в бот.
    """
    # Конфигурация логирования
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s')
    logging.info('Starting bot')

    config: Config = load_credentials('env')  # type: ignore
    bot: Bot = Bot(token=config.tg_bot.token,  # type: ignore
                   parse_mode='HTML')  # type: ignore
    storage: MemoryStorage = MemoryStorage()  # type: ignore

    # Регистриуем роутер пользовательских хэндлеров в диспетчере
    dispatcher: Dispatcher = Dispatcher(storage=storage)  # type: ignore
    dispatcher.include_router(usrouter)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
