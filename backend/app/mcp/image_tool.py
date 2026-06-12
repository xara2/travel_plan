"""Image search tool — Unsplash API with local image_cache.json fallback."""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGE_CACHE_PATH = os.path.join(BASE_DIR, "data", "image_cache.json")


def _load_cache() -> dict[str, str]:
    if not os.path.exists(IMAGE_CACHE_PATH):
        return {}
    with open(IMAGE_CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


async def search_images(query: str, destination: str = "", count: int = 5) -> list[dict]:
    """Search images via Unsplash, falling back to local cache."""
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")

    if access_key:
        results = await _search_unsplash(query, destination, count, access_key)
        if results:
            return results

    return _search_cache(query, destination, count)


async def _search_unsplash(query: str, destination: str, count: int, access_key: str) -> list[dict]:
    import httpx

    search_terms = f"{destination} {query}".strip()
    url = "https://api.unsplash.com/search/photos"
    params = {"query": search_terms, "per_page": count, "orientation": "landscape"}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params, headers={"Authorization": f"Client-ID {access_key}"})
            resp.raise_for_status()
            data = resp.json()

            results = []
            for img in data.get("results", []):
                results.append({
                    "url": img["urls"]["regular"],
                    "thumbnail_url": img["urls"]["thumb"],
                    "alt_text": img.get("alt_description", search_terms),
                    "source": f"Unsplash @{img['user']['username']}",
                })
            return results
    except Exception:
        return []


def _search_cache(query: str, destination: str, count: int) -> list[dict]:
    """Fallback: fuzzy match against local image_cache.json."""
    cache = _load_cache()
    if not cache:
        return []

    results = []
    for name, url in cache.items():
        if destination and destination not in name:
            continue
        if query and query not in name:
            continue
        results.append({
            "url": url,
            "thumbnail_url": url,
            "alt_text": name,
            "source": "本地图库",
        })
        if len(results) >= count:
            break

    if not results:
        for name, url in list(cache.items())[:count]:
            results.append({
                "url": url,
                "thumbnail_url": url,
                "alt_text": name,
                "source": "本地图库",
            })

    return results
