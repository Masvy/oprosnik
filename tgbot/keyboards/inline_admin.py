from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.admin_lexicon import ADMIN_MENU

# Создал объект клавиатуры
admin_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=ADMIN_MENU['mailing_list'],
                                 callback_data='mailing_list_pressed'),
            InlineKeyboardButton(text=ADMIN_MENU['start_survay'],
                                 callback_data='start_survay_pressed')
        ],
        [
            InlineKeyboardButton(text=ADMIN_MENU['statistics'],
                                 callback_data='statistics_pressed'),
            InlineKeyboardButton(text=ADMIN_MENU['show_users'],
                                 callback_data='show_users_pressed')
        ]
    ]
)
