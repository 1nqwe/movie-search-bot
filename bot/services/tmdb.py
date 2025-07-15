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

