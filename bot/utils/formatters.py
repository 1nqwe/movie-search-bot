def format_movie(movie):
    text = (f"🎬 <b>{movie.get('title', 'Без названия')}</b> ({movie.get('year', '????')})\n"
            f"⭐ <b>Рейтинг:</b> {movie.get('rating', '?/10')}\n")

    if movie.get('trailer_url'):
        text += f"🎥 <a href='{movie['trailer_url']}'>Смотреть трейлер</a>\n\n"

    text += f"📝 <b>Описание:</b> {movie.get('overview', 'Описание отсутствует')[:450]}..."

    return text


def format_series(series):
    text = (f"📺 <b>{series.get('title', 'Без названия')}</b>\n"
            f"📅 <b>Годы:</b> {series.get('year', '????')}")

    if series.get('last_air_date') and series['last_air_date'] != series.get('year', '????'):
        text += f"-{series['last_air_date']}\n"
    else:
        text += "\n"

    text += (f"⭐ <b>Рейтинг:</b> {series.get('rating', '?/10')}\n"
            f"🖼️ <b>Сезонов:</b> {series.get('seasons', '?')}\n"
            f"🎞️ <b>Эпизодов:</b> {series.get('episodes', '?')}\n")

    if series.get('trailer_url'):
        text += f"\n🎥 <b>Трейлер:</b> <a href='{series['trailer_url']}'>Смотреть на YouTube</a>\n"
    text += f"\n📝 <b>Описание:</b> {series.get('overview', '<b>Нет описания</b>')[:450]}"
    return text


def format_anime(anime):
    text = (f"🌸 <b>{anime.get('title', '?')}</b>\n"
            f"📅 <b>Год:</b> {anime.get('year', '????')}\n"
            f"⭐ <b>Рейтинг:</b> {anime.get('score', '?')}/10\n"
            f"📊 <b>Эпизодов:</b> {anime.get('episodes', '?')}\n")

    if anime.get('url'):
        text += f"\n🔗 <a href='{anime['url']}'>Страница на Shikimori</a>\n"

    description = anime.get('description', '')
    text += f"\n📝 {description[:300]}..." if len(description) > 300 else f"\n📝 {description}"
    return text