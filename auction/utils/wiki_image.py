import requests

def fetch_wikipedia_image(player_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": player_name.title(),
        "pithumbsize": 500
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():
            return page.get("thumbnail", {}).get("source")

    except Exception:
        return None
