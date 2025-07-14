def format_movie(movie: dict):
    return (
        f"🎬 <b>{movie.get('title', 'Без названия')}</b> ({movie.get('year', '????')})\n"
        f"⭐ <b>Рейтинг:</b> {movie.get('rating', '?/10')}\n"
        f"📝 <b>Описание:</b> {movie.get('overview', 'Описание отсутствует')[:500]}..."
    )