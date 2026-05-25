"""Fetch real attraction images from Wikipedia/Wikimedia Commons."""
import json
import os
import time
import urllib.request
import urllib.parse
import ssl

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "attractions.json")
CACHE_FILE = os.path.join(os.path.dirname(__file__), "data", "image_cache.json")

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


def wiki_api(params):
    """Call Wikipedia API with caching."""
    base = "https://zh.wikipedia.org/w/api.php"
    qs = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = f"{base}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "TravelPlan/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
            else:
                print(f"  API error: {e}")
                return None


def get_wiki_image(name):
    """Get main page image from Chinese Wikipedia for an attraction."""
    # Search for the page
    result = wiki_api({
        "action": "query", "list": "search",
        "srsearch": name, "srlimit": 3,
        "format": "json",
    })
    if not result or not result.get("query", {}).get("search"):
        return None

    titles = [r["title"] for r in result["query"]["search"]]
    if not titles:
        return None

    # Get page image for best match
    for title in titles[:2]:
        r2 = wiki_api({
            "action": "query", "prop": "pageimages",
            "titles": title, "pithumbsize": 600,
            "format": "json",
        })
        if not r2 or "query" not in r2:
            continue
        pages = r2["query"].get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                continue
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                return thumb.replace("https://", "http://")  # consistent http

    return None


def get_commons_image(name):
    """Search Wikimedia Commons for an image."""
    result = wiki_api({
        "action": "query", "list": "search",
        "srsearch": f"{name} site", "srnamespace": 6,
        "srlimit": 5, "format": "json",
    })
    if not result or not result.get("query", {}).get("search"):
        return None

    for r in result["query"]["search"]:
        filename = r["title"].replace("File:", "").replace(" ", "_")
        # Use Wikimedia's thumbnail URL
        encoded = urllib.parse.quote(filename)
        return f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width=600"

    return None


def fallback_image(name, category):
    """Generate a relevant default image URL."""
    # Using picsum with a deterministic seed for consistency
    import hashlib
    seed = int(hashlib.md5(name.encode()).hexdigest()[:8], 16) % 1000
    return f"https://picsum.photos/seed/{seed}/600/400"


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        attractions = json.load(f)

    # Load cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)

    updated = 0
    for i, a in enumerate(attractions):
        name = a["name"]
        if name in cache:
            a["image_url"] = cache[name]
            updated += 1
            continue

        # Skip if already has a non-unsplash URL
        current = a.get("image_url", "")
        if "unsplash.com" not in current and "picsum.photos" not in current and "placehold.co" not in current:
            cache[name] = current
            continue

        print(f"[{i+1}/{len(attractions)}] {name}...", end=" ", flush=True)

        # Try Wikipedia first, then Commons, then fallback
        img = None
        for fetcher in [get_wiki_image, get_commons_image]:
            img = fetcher(name)
            if img:
                break
            time.sleep(0.3)

        if not img:
            img = fallback_image(name, a.get("category", ""))
            print(f"fallback")
        else:
            print("OK")

        a["image_url"] = img
        cache[name] = img
        updated += 1

        # Save progress every 20
        if updated % 20 == 0:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(attractions, f, ensure_ascii=False, indent=2)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False)

        time.sleep(0.15)  # Rate limit

    # Final save
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(attractions, f, ensure_ascii=False, indent=2)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)

    print(f"\nDone! Updated {updated}/{len(attractions)} images.")


if __name__ == "__main__":
    main()
