from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_invitation_keyboard(yes_button, no_button):
    buttons = [
        [
            KeyboardButton(text=yes_button),
            KeyboardButton(text=no_button)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
