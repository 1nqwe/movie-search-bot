import asyncio
from time import sleep

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user_keyboards import user_to_menu_kb, user_menu_kb, user_search_menu_kb, user_to_menu_kb_delete
from bot.states.user_states import UserState
from bot.services.tmdb import get_movies
from bot.utils.formatters import format_movie

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('привет я помогу найти тебе фильмы, аниме и сериалы', reply_markup=user_to_menu_kb())

@user_router.callback_query(F.data == 'user_menu')
async def user_menu(call: CallbackQuery):
    await call.message.edit_text('Меню', reply_markup=user_menu_kb())

@user_router.callback_query(F.data == 'search')
async def search_menu(call: CallbackQuery):
    await call.message.edit_text('Выберите что будете искать', reply_markup=user_search_menu_kb())

@user_router.callback_query(F.data == 'search_movies')
async def search_movies(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.movies)
    await call.message.edit_text('🔍 Введите название фильма:\n\n'
                                 '<i>Через 5 секунд это сообщение удалится</i>', parse_mode='HTML',
                                input_field_placeholder="Введите название фильма: ")
    await asyncio.sleep(5)
    await call.message.delete()

@user_router.message(UserState.movies)
async def search_movies_step_2(message: Message, state: FSMContext):
    await message.delete()
    query = message.text.strip()
    await state.update_data(movies=query)
    movie_data = await get_movies(query)
    await state.clear()
    if not movie_data:
            await message.answer("😢 Фильм не найден. Попробуйте другое название.", reply_markup=user_to_menu_kb())
            return

    response_text = format_movie(movie_data)
    await message.answer_photo(photo=movie_data["poster_url"], caption=response_text,
                               parse_mode="HTML", reply_markup=user_to_menu_kb_delete())
    
@user_router.callback_query(F.data == 'user_menu_delete')
async def menu_number_2(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Меню', reply_markup=user_menu_kb())
