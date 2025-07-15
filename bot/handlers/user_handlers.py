import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.user_keyboards import user_to_menu_kb, user_menu_kb, user_search_menu_kb, user_to_menu_kb_delete
from bot.services.shikimori import get_anime
from bot.services.tmdb import get_movies, get_tv_series
from bot.states.user_states import UserState
from bot.utils.formatters import format_movie, format_anime

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
                                 reply_markup=user_to_menu_kb_delete())
    await asyncio.sleep(5)
    await call.message.delete()

@user_router.callback_query(F.data == 'search_series')
async def search_movies(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.series)
    await call.message.edit_text('🔍 Введите название сериала:\n\n'
                                 '<i>Через 5 секунд это сообщение удалится</i>', parse_mode='HTML',
                                 reply_markup=user_to_menu_kb_delete())
    await asyncio.sleep(5)
    await call.message.delete()


@user_router.message(UserState.movies)
async def search_movies_step_2(message: Message, state: FSMContext):
    try:
        query = message.text.strip()
        search_msg = await message.answer("⏳ Ищем фильм...")
        movie_data = await get_movies(query)
        await message.delete()
        if not movie_data:
            await search_msg.edit_text("😢 Фильм не найден. Попробуйте другое название")
            return

        await search_msg.delete()

        await message.answer_photo(
            photo=movie_data.get("poster_url", "https://via.placeholder.com/500x750?text=No+Poster"),
            caption=format_movie(movie_data),
            parse_mode="HTML",
            reply_markup=user_to_menu_kb_delete()
        )

    except:
        await message.answer("⚠️ При запросе произошла ошибка, попробуйте позже...")
    finally:
        await state.clear()
    
@user_router.callback_query(F.data == 'user_menu_delete')
async def menu_number_2(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Меню', reply_markup=user_menu_kb())


@user_router.message(UserState.series)
async def process_series_search(message: Message, state: FSMContext):
    try:
        query = message.text.strip()
        try:
            await message.delete()
        except:
            pass

        search_msg = await message.answer("⌛ Ищем сериал...")
        series_data = await get_tv_series(query)

        if not series_data:
            await search_msg.edit_text("😔 Ничего не найдено. Попробуйте другой запрос")
            return

        response_text = (
            f"🎬 <b>{series_data.get('title', 'Без названия')}</b>\n"
            f"⭐ <b>Рейтинг:</b> {series_data.get('rating', '?/10')}\n"
            f"📅 <b>Годы:</b> {series_data.get('year', '????')}"
            f"{'-' + series_data['last_air_date'][:4] if series_data.get('last_air_date') else ''}\n"
            f"📊 <b>Сезонов:</b> {series_data.get('seasons', '?')}\n"
            f"🎞️ <b>Эпизодов:</b> {series_data.get('episodes', '?')}\n"
        )

        if series_data.get('trailer_url'):
            response_text += f"\n🎥 <a href='{series_data['trailer_url']}'>Смотреть трейлер</a>\n"

        response_text += f"\n📝 <b>Описание:</b> {series_data.get('overview', 'Нет описания')[:300]}..."

        await search_msg.delete()
        await message.answer_photo(
            photo=series_data.get("poster_url", "https://via.placeholder.com/500x750?text=No+Poster"),
            caption=response_text, parse_mode="HTML", reply_markup=user_to_menu_kb_delete())

    except:
        await message.answer("⚠️ При запросе произошла ошибка, попробуйте позже...")

    finally:
        await state.clear()


@user_router.callback_query(F.data == 'search_anime')
async def search_anime(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.anime)
    await state.update_data(search_message=call.message)
    await call.message.edit_text('🔍 Введите название аниме: ', parse_mode='HTML',
                                 reply_markup=user_to_menu_kb_delete())


@user_router.message(StateFilter(UserState.anime))
async def handle_anime_search(message: Message, state: FSMContext):
    data = await state.get_data()
    search_message = data.get('search_message')
    if search_message:
        try:
            await search_message.delete()
        except:
            pass

    query = message.text.strip()
    search_msg = await message.answer("🔍 Ищем на Shikimori...")

    await message.delete()
    try:
        anime = await get_anime(query)

        if not anime:
            await search_msg.edit_text("Аниме не найдено. Попробуйте:\n"
                                            "• Английское название - Атака Титанов -> Attack on Titan",
                                            reply_markup=user_to_menu_kb_delete())

        response = format_anime(anime)

        await search_msg.delete()

        if anime.get('image_url'):
            await message.answer_photo(
                photo=anime['image_url'],
                caption=response,
                parse_mode="HTML",
                reply_markup=user_to_menu_kb_delete()
            )
        else:
            await message.answer(response, parse_mode="HTML")

    except:
        await search_msg.edit_text("⚠️ При запросе произошла ошибка, попробуйте позже...", reply_markup=user_to_menu_kb_delete())
    finally:
        await state.clear()