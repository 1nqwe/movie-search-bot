from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_to_menu_kb():
    kb = [
        [InlineKeyboardButton(text='🏠 Меню', callback_data='user_menu')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def user_to_menu_kb_delete():
    kb = [
        [InlineKeyboardButton(text='🏠 Меню', callback_data='user_menu_delete')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def user_menu_kb():
    kb = [
        [InlineKeyboardButton(text='👤 Профиль', callback_data='profile')],
        [InlineKeyboardButton(text='🔍 Поиск', callback_data='search')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def user_search_menu_kb():
    kb = [
        [InlineKeyboardButton(text='🎥 Фильмы', callback_data='search_movies')],
        [InlineKeyboardButton(text='🎞️ Сериалы', callback_data='search_series')],
        [InlineKeyboardButton(text='📼 Аниме', callback_data='search_anime')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='user_menu')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)