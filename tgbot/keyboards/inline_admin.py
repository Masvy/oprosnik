from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.admin_lexicon import ADMIN_MENU

admin_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=ADMIN_MENU['mailing_list'],
                                 callback_data='mailing_list_pressed'),
            InlineKeyboardButton(text=ADMIN_MENU['change_survey'],
                                 callback_data='change_survey_pressed')
        ]
    ]
)
