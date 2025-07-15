from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
        [InlineKeyboardButton(text='🔍 Поиск', callback_data='search')],
        [InlineKeyboardButton(text='📦 Подборки', callback_data='collections')]
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


def get_genres_keyboard():
    builder = InlineKeyboardBuilder()

    genres = [
        ("Фантастика", "фантастика"),
        ("Боевик", "боевик"),
        ("Фэнтези", "фэнтези"),
        ("Ужасы", "ужасы"),
        ("Комедия", "комедия"),
        ("Драма", "драма"),
        ("Триллер", "триллер"),
        ("Криминал", "криминал"),
        ("Спорт", "спорт"),
        ("Мелодрама", "мелодрама"),
        ("Детектив", "детектив"),
        ("Военный", "военный")
    ]

    for display_name, callback_data in genres:
        builder.button(
            text=display_name,
            callback_data=f"genre_{callback_data}"
        )

    builder.button(text='🏠 Меню', callback_data='user_menu_delete')
    builder.adjust(2)
    return builder.as_markup()