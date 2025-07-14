import aiohttp

from config import TMDB_API_KEY

async def get_movies(query: str):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}&language=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if not data.get("results"):
                    return None

                movie = data["results"][0]

                rating = movie.get("vote_average")
                rating_str = f"{round(rating, 1)}/10" if isinstance(rating, (int, float)) else "?/10"

                return {
                    "title": movie.get("title", "Без названия"),
                    "year": movie.get("release_date", "????")[:4],
                    "rating": rating_str,
                    "overview": movie.get("overview", "Описание отсутствует"),
                    "poster_url": f"https://image.tmdb.org/t/p/original{movie['poster_path']}" if movie.get(
                        "poster_path") else None
                }
    except Exception:
        pass