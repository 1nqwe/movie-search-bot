import asyncio

from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.user_keyboards import user_to_menu_kb, user_menu_kb, user_search_menu_kb, user_to_menu_kb_delete, \
    get_genres_keyboard
from bot.services.shikimori import get_anime
from bot.services.tmdb import get_movies, get_tv_series, get_movies_by_genre
from bot.states.user_states import UserState
from bot.utils.formatters import format_movie, format_anime

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = """
    🎬 <b>Добро пожаловать!</b> 🍿

    Я твой персональный гид по миру кино!
    
    Здесь ты можешь:
    • Найти любимые фильмы
    • Найти лучшие фильмы по жанрам
    • Посмотреть трейлеры фильмов
    • Узнать о новинах

    Жми на кнопку снизу!
    """
    await message.answer(welcome_text, reply_markup=user_to_menu_kb(), parse_mode="HTML")

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
    await call.message.answer('🏠 Меню: ', reply_markup=user_menu_kb())


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

@user_router.callback_query(F.data == 'collections')
async def movies_command(call: CallbackQuery):
    await call.message.edit_text('🎭 Выберите жанр: ', reply_markup=get_genres_keyboard())


@user_router.callback_query(lambda c: c.data.startswith('genre_'))
async def handle_genre_selection(callback: CallbackQuery):
    genre = callback.data.replace('genre_', '')
    await callback.message.delete()
    await callback.answer(f"Ищем {genre}...", show_alert=False)

    status, result = await get_movies_by_genre(genre)

    if not status:
        builder = InlineKeyboardBuilder()
        builder.button(
            text="🔄 Выбрать другой жанр",
            callback_data="change_genre"
        )

        try:
            await callback.message.edit_text(
                result,
                reply_markup=builder.as_markup()
            )
        except:
            await callback.message.answer(
                result,
                reply_markup=builder.as_markup()
            )
        return

    await show_movie_page(
        callback.message,
        result,
        genre_name=genre,
        page=0
    )


async def show_movie_page(message: Message, movies: list, genre_name: str, page: int):
    movie = movies[page]

    text = (
        f"🎬 <b>{movie['title']}</b> ({movie['year']})\n"
        f"⭐ Рейтинг: <b>{movie['rating']}/10</b>\n\n"
        f"📝 {movie['overview']}\n\n"
        f"🍿 Жанр: {genre_name}"
    )

    builder = InlineKeyboardBuilder()

    if page > 0:
        builder.button(text="⬅️ Назад", callback_data=f"movie_{genre_name}_{page - 1}")
    if page < len(movies) - 1:
        builder.button(text="Далее ➡️", callback_data=f"movie_{genre_name}_{page + 1}")

    builder.button(text="🔁 Другой жанр", callback_data="change_genre")
    builder.adjust(2)

    try:
        if movie['poster']:
            await message.answer_photo(
                photo=movie['poster'],
                caption=text,
                parse_mode="HTML",
                reply_markup=builder.as_markup()
            )
        else:
            await message.answer(
                text,
                parse_mode="HTML",
                reply_markup=builder.as_markup(),
                disable_web_page_preview=True
            )
    except:
        await message.answer(
            "⚠️ Ошибка при отображении фильма",
            reply_markup=builder.as_markup()
        )


@user_router.callback_query(lambda c: c.data.startswith('movie_'))
async def handle_movie_nav(callback: CallbackQuery):
    _, genre, page = callback.data.split('_')
    page = int(page)

    status, result = await get_movies_by_genre(genre)

    if status:
        await callback.message.delete()
        await show_movie_page(
            callback.message,
            result,
            genre_name=genre,
            page=page
        )
    else:
        await callback.answer(result, show_alert=True)


@user_router.callback_query(F.data == 'change_genre')
async def handle_genre_change(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "🎭 Выберите жанр:",
        reply_markup=get_genres_keyboard()
    )

@user_router.callback_query(F.data == 'profile')
async def profile(call: CallbackQuery):
    await call.message.edit_text(f'Ваш профиль:\n\n'
                                 f'Ваше имя: {call.message.from_user.full_name}',
                                 reply_markup=user_to_menu_kb_delete())