import aiohttp
from config import SHIKIMORI_API


async def get_anime(query):
    url = f"{SHIKIMORI_API}/animes?search={query}&limit=1"

    headers = {
        "User-Agent": "AnimeSearchBot/1.0 (your@email.com)"
    }

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                if not data or not isinstance(data, list):
                    return None

                anime = data[0]
                return {
                    "id": anime.get("id"),
                    "title": anime.get("russian") or anime.get("name"),
                    "original_title": anime.get("name"),
                    "year": anime.get("aired_on", "").split("-")[0] if anime.get("aired_on") else "?",
                    "score": anime.get("score"),
                    "episodes": anime.get("episodes"),
                    "status": anime.get("status"),
                    "description": anime.get("description") or "Нет описания",
                    "image_url": f"https://shikimori.one{anime['image']['original']}" if anime.get("image") else None,
                    "url": f"https://shikimori.one{anime.get('url')}",
                    "genres": ", ".join(genre["name"] for genre in anime.get("genres", []))
                }

    except:
        return None
