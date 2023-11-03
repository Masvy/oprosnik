import os
import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, and_f, StateFilter, Command
from aiogram.fsm.context import FSMContext
from environs import Env
from sqlalchemy.orm import sessionmaker
from aiogram.fsm.state import default_state

from filters.admin_filters import IsAdmin
from keyboards.inline_admin import admin_kb
from states.admin_states import InputNews
from database.users import count_user_ids, number_registered, show_user_ids, \
                           show_user_names, show_first_names
from lexicon.admin_lexicon import ADMIN_MENU
from utils.exсel_file import generate_excel_file

admin_router: Router = Router()

env = Env()
env.read_env()


@admin_router.message(and_f(CommandStart(), IsAdmin(env('ADMIN_IDS'))))
async def start_admin(message: Message):
    '''Хэндлер срабатывает при вводе команды /start у админов.'''
    await message.answer('Выбери действие:',
                         reply_markup=admin_kb)


@admin_router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=ADMIN_MENU['cancel'])
    await state.clear()


@admin_router.callback_query(F.data == 'mailing_list_pressed')
async def request_mailing(callback: CallbackQuery, state: FSMContext):
    '''
    Хэндлер для кнопки «Рассылка».

    Переводит ввода контента.
    '''
    await callback.message.answer(text=ADMIN_MENU['input_content'])
    await state.set_state(InputNews.news)


@admin_router.message(StateFilter(InputNews.news))
async def input_news(message: Message, state: FSMContext,
                     session_maker: sessionmaker):
    '''
    Хэндлер срабатывает на введение контента.

    Начинает рассылку по пользователям.
    '''
    await state.update_data(news=message.text)
    count_user_ids_ = await count_user_ids(session_maker=session_maker)
    await state.clear()
    users = 0
    for count_user_id in count_user_ids_:
        try:
            await message.copy_to(count_user_id)
            users += 1
        except Exception:
            pass
        await asyncio.sleep(0.1)
    await message.answer('Рассылка завершена. Пользователи, '
                         f'которым пришла рассылка: {users}')


@admin_router.callback_query(F.data == 'statistics_pressed')
async def show_statistics(callback: CallbackQuery,
                          session_maker: sessionmaker):
    registered = await number_registered(session_maker=session_maker)
    await callback.message.answer(text='Количество зерегистрированных '
                                  f'пользователей: {registered}')


@admin_router.callback_query(F.data == 'show_users_pressed')
async def show_users(callback: CallbackQuery,
                     session_maker: sessionmaker,
                     bot: Bot):
    show_user_ids_ = await show_user_ids(session_maker=session_maker)
    show_first_names_ = await show_first_names(session_maker=session_maker)
    show_user_names_ = await show_user_names(session_maker=session_maker)
    excel_file = await generate_excel_file(show_user_ids_, show_first_names_,
                                           show_user_names_)

    temp_file_path = "temp_user_database.xlsx"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(excel_file.read())

    await bot.send_document(callback.from_user.id,
                            document=FSInputFile(temp_file_path))
    os.remove(temp_file_path)
