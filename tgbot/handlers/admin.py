import asyncio

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, and_f, StateFilter
from aiogram.fsm.context import FSMContext
from environs import Env

from filters.admin_filters import IsAdmin
from keyboards.inline_admin import admin_kb
from states.admin_states import InputNews

admin_router: Router = Router()

env = Env()
env.read_env()


@admin_router.message(and_f(CommandStart(), IsAdmin(env('ADMIN_IDS'))))
async def start_admin(message: Message):
    '''Хэндлер срабатывает при вводе команды /start у админов.'''
    await message.answer('Выбери действие:',
                         reply_markup=admin_kb)


@admin_router.callback_query(F.data == 'mailing_list_pressed')
async def request_mailing(callback: CallbackQuery, state: FSMContext):
    '''
    Хэндлер для кнопки «Рассылка».

    Переводит ввода контента.
    '''
    await callback.message.answer(text='Отправьте контент для рассылки:')
    await state.set_state(InputNews.news)


@admin_router.message(StateFilter(InputNews.news))
async def input_news(message: Message, state: FSMContext):
    '''
    Хэндлер срабатывает на введение контента.

    Начинает рассылку по пользователям.
    '''
    await state.update_data(news=message.text)
    count_user_ids_ = [707637895]
    for count_user_id in count_user_ids_:
        await message.copy_to(count_user_id)
        await asyncio.sleep(.05)


#382712245
#519789698