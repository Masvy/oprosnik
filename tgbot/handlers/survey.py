from random import randint

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from lexicon.user_lexicon import TEST1
from keyboards.inline_user import question1, question2, question3, \
                                  question4, question5, question6, \
                                  question7, question8, question9, \
                                  question10

survey_router: Router = Router()


@survey_router.message(CommandStart())
async def start_bot(message: Message):
    '''Хэндлер реагирует на команду /start для юзеров.'''
    await message.answer(text=TEST1['name'])
    await message.answer(text=TEST1['question1'],
                         reply_markup=question1)


@survey_router.callback_query(F.data == 'question1_pressed1')
async def question_1(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question2'],
                                     reply_markup=question2)


@survey_router.callback_query(F.data == 'question2_pressed1')
async def question_2(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question3'],
                                     reply_markup=question3)


@survey_router.callback_query(F.data == 'question3_pressed1')
async def question_3(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question4'],
                                     reply_markup=question4)


@survey_router.callback_query(F.data == 'question4_pressed1')
async def question_4(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question5'],
                                     reply_markup=question5)


@survey_router.callback_query(F.data == 'question5_pressed1')
async def question_5(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question6'],
                                     reply_markup=question6)


@survey_router.callback_query(F.data == 'question6_pressed1')
async def question_6(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question7'],
                                     reply_markup=question7)


@survey_router.callback_query(F.data == 'question7_pressed1')
async def question_7(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question8'],
                                     reply_markup=question8)


@survey_router.callback_query(F.data == 'question8_pressed1')
async def question_8(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question9'],
                                     reply_markup=question9)


@survey_router.callback_query(F.data == 'question9_pressed1')
async def question_9(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    await callback.message.edit_text(text=TEST1['question10'],
                                     reply_markup=question10)


@survey_router.callback_query(F.data == 'question10_pressed1')
async def question_10(callback: CallbackQuery):
    '''Хэндлер реагирует на любую кнопку'''
    result = randint(1, 2)
    await callback.message.edit_text(text=TEST1[result])
