import aiohttp

from config import TMDB_API_KEY


async def get_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if not data.get("results"):
                    return None

                movie = data["results"][0]

                movie_id = movie.get("id")

                videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}&language=ru"
                async with session.get(videos_url) as videos_resp:
                    videos_data = await videos_resp.json()
                    trailer_url = None
                    if videos_data.get("results"):
                        for video in videos_data["results"]:
                            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                                trailer_url = f"https://youtu.be/{video['key']}"
                                break

                return {
                    "title": movie.get("title", "Без названия"),
                    "year": movie.get("release_date", "????")[:4],
                    "rating": str(round(movie.get("vote_average", 0), 1)) + "/10",
                    "overview": movie.get("overview", "Описание отсутствует"),
                    "poster_url": f"https://image.tmdb.org/t/p/original{movie['poster_path']}" if movie.get(
                        "poster_path") else None,
                    "trailer_url": trailer_url
                }
    except Exception as e:
        print(f"Ошибка при запросе к TMDb API: {e}")
        return None


async def get_tv_series(query):
    url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={query}&language=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if not data.get("results"):
                    return None

                series = data["results"][0]

                details_url = f"https://api.themoviedb.org/3/tv/{series['id']}?api_key={TMDB_API_KEY}&language=ru"
                async with session.get(details_url) as details_resp:
                    details = await details_resp.json()

                videos_url = f"https://api.themoviedb.org/3/tv/{series['id']}/videos?api_key={TMDB_API_KEY}&language=ru"
                async with session.get(videos_url) as videos_resp:
                    videos_data = await videos_resp.json()
                    trailer_url = None
                    if videos_data.get("results"):
                        for video in videos_data["results"]:
                            if video.get("site") == "YouTube" and video.get("type") == "Trailer":
                                trailer_url = f"https://youtu.be/{video['key']}"
                                break

                return {
                    "title": series.get("name", "Без названия"),
                    "year": series.get("first_air_date", "????")[:4],
                    "rating": str(round(series.get("vote_average", 0), 1)) + "/10",
                    "overview": series.get("overview", "Описание отсутствует"),
                    "poster_url": f"https://image.tmdb.org/t/p/original{series['poster_path']}" if series.get(
                        "poster_path") else None,
                    "trailer_url": trailer_url,
                    "seasons": details.get("number_of_seasons", "?"),
                    "episodes": details.get("number_of_episodes", "?"),
                    "status": details.get("status", "Статус неизвестен"),
                    "last_air_date": details.get("last_air_date", "????")[:4] if details.get("last_air_date") else None
                }
    except Exception:
        return None


async def get_movies_by_genre(genre_name: str) -> tuple:
    """Возвращает (статус, данные или сообщение об ошибке)"""
    genre_map = {
        'фантастика': (878, 'Sci-Fi'),
        'боевик': (28, 'Action'),
        'фэнтези': (14, 'Fantasy'),
        'ужасы': (27, 'Horror'),
        'комедия': (35, 'Comedy'),
        'драма': (18, 'Drama'),
        'триллер': (53, 'Thriller'),
        'криминал': (80, 'Crime'),
        'спорт': (99, 'Sport'),
        'история': (36, 'History'),
        'мелодрама': (10749, 'Romance'),
        'детектив': (9648, 'Mystery'),
        'военный': (10752, 'War')
    }

    if genre_name.lower() not in genre_map:
        return False, "Неизвестный жанр"

    genre_id, en_name = genre_map[genre_name.lower()]

    try:
        url = f"https://api.themoviedb.org/3/discover/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'with_genres': genre_id,
            'language': 'ru-RU',
            'sort_by': 'popularity.desc',
            'page': 1
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    return False, "Ошибка подключения к TMDB"

                data = await response.json()
                if not data.get('results'):
                    return False, f"По жанру '{genre_name}' ничего не найдено\nПопробуйте другой жанр"

                movies = []
                for item in data['results'][:5]:  # Берем топ-5
                    movies.append({
                        'title': item.get('title', 'Без названия'),
                        'year': item.get('release_date', '')[:4] if item.get('release_date') else '????',
                        'rating': round(item.get('vote_average', 0), 1),
                        'overview': item.get('overview', 'Описание отсутствует'),
                        'poster': f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get(
                            'poster_path') else None
                    })

                return True, movies

    except Exception as e:
        print(f"TMDB API Error: {e}")
        return False, "Ошибка при получении данных"