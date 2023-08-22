from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, and_f
from environs import Env

from filters.admin_filters import IsAdmin
from keyboards.inline_admin import admin_kb

admin_router: Router = Router()

env = Env()
env.read_env()


@admin_router.message(and_f(CommandStart(), IsAdmin(env('ADMIN_IDS'))))
async def start_admin(message: Message):
    await message.answer('Выбери действие:',
                         reply_markup=admin_kb)
