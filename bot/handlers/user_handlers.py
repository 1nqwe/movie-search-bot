from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user_keyboards import user_to_menu_kb, user_menu_kb, user_search_menu_kb

user_router = Router()

@user_router.message()
async def cmd_start(message: Message):
    await message.answer('привет я помогу найти тебе фильмы, аниме и сериалы', reply_markup=user_to_menu_kb())

@user_router.callback_query(F.data == 'user_menu')
async def user_menu(call: CallbackQuery):
    await call.message.edit_text('Меню', reply_markup=user_menu_kb())

@user_router.callback_query(F.data == 'search')
async def search_menu(call: CallbackQuery):
    await call.message.edit_text('Выберите что будете искать', reply_markup=user_search_menu_kb())

