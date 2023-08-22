import logging
import asyncio

from environs import Env
import betterlogging as bl
from aiogram import Bot, Dispatcher
from sqlalchemy import URL

from handlers import admin
from database.create_table import BaseModel
from database.engine import proceed_schemas
from database.engine import create_async_engine, get_session_maker
from middlewares.register_check import RegisterCheck


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s'
               ' [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')


async def main():
    setup_logging()

    env = Env()
    env.read_env()

    bot: Bot = Bot(token=env('BOT_TOKEN'),
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    dp.include_router(admin.admin_router)

    postgres_url = URL.create(
        'postgresql+asyncpg',
        username=env('PGUSER'),
        password=env('PGPASSWORD'),
        database=env('DB_NAME'),
        host='localhost',
        port='5432'
    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    await proceed_schemas(async_engine, BaseModel.metadata)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Stopping bot')
