import logging
import asyncio

from environs import Env
from aiogram import Bot, Dispatcher
from sqlalchemy import URL
import betterlogging as bl

from handlers import admin, survey
from database.create_table import BaseModel
from database.engine import proceed_schemas
from database.engine import create_async_engine, get_session_maker
from middlewares.register_check import RegisterCheck
from keyboards.set_menu import set_main_menu


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


def setup_logging():
    '''Функция конфигурации логирования'''
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
    '''
    Функция конфигурирования и запуска бота

    Создал объекты бота и диспетчера
    Зарегистрировал роутеры в диспетчере
    Создал url для соединения с базой
    Пропускаем накопившиеся апдейты и запускаем polling
    '''
    setup_logging()

    env = Env()
    env.read_env()

    bot: Bot = Bot(token=env('BOT_TOKEN'),
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    dp.include_router(admin.admin_router)
    dp.include_router(survey.survey_router)

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
