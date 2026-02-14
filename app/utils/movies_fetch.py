import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote
from difflib import get_close_matches
import asyncio


# ==================== CONFIGURATION ====================

# Default settings - change these if needed
ARABSEED_BASE_URL = "https://a.asd.homes"
AKWAM_BASE_URL = "https://ak.sv"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DEFAULT_TIMEOUT = 30.0
DEFAULT_FUZZY_CUTOFF = 0.5


# ==================== HELPER FUNCTIONS ====================

def get_best_match(movie_name, movies_list, cutoff=DEFAULT_FUZZY_CUTOFF):
    """Find best matching movie from search results using fuzzy matching."""
    if not movies_list:
        return None

    titles = [m["name"] for m in movies_list]
    best_title = get_close_matches(movie_name, titles, n=1, cutoff=cutoff)

    if best_title:
        for m in movies_list:
            if m["name"] == best_title[0]:
                return m["link"]
    return None


def _get_client(user_agent=None, timeout=None):
    """Create configured httpx AsyncClient."""
    headers = {"User-Agent": user_agent or DEFAULT_USER_AGENT}
    return httpx.AsyncClient(
        headers=headers,
        timeout=timeout or DEFAULT_TIMEOUT,
        follow_redirects=True
    )


# ==================== ARABSEED SCRAPER ====================

async def _scrape_arabseed_movies(movie_name, client):
    """Internal: Search for movies on ArabSeed."""
    encoded_name = quote(movie_name)
    url = f"{ARABSEED_BASE_URL}/find/?word={encoded_name}&type=movies"
    
    response = await client.get(url)
    response.raise_for_status()
        
    soup = BeautifulSoup(response.text, "html.parser")
    containers = soup.select("div.series__list ul")

    movies_info = []
    for ul in containers:
        for tag in ul.select("a.movie__block"):
            title = tag.get("title")
            link = tag.get("href")
            if title and link:
                full_url = link if link.startswith("http") else ARABSEED_BASE_URL + link
                movies_info.append({"name": title, "link": full_url})

    return movies_info


async def _get_arabseed_watch_page(movie_link, client):
    """Internal: Get the watch page URL from a movie link."""
    await asyncio.sleep(0.3)  # Rate limiting
    
    response = await client.get(movie_link)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    watch_button = soup.select_one("a.watch__btn")

    if not watch_button:
        return None

    watch_page_link = watch_button.get("href")
    return (
        watch_page_link if watch_page_link.startswith("http")
        else ARABSEED_BASE_URL + watch_page_link
    )


async def search_arabseed(movie_name, cutoff=None, user_agent=None, timeout=None):

    try:
        async with _get_client(user_agent, timeout) as client:
            # Search for movies
            movies_list = await _scrape_arabseed_movies(movie_name, client)
            
            # Find best match
            best_match_link = get_best_match(movie_name, movies_list, cutoff or DEFAULT_FUZZY_CUTOFF)
            
            if not best_match_link:
                return None
            
            # Get watch page
            return await _get_arabseed_watch_page(best_match_link, client)
    except Exception:
        # Return None for any error (network, timeout, parsing, etc.)
        return None


# ==================== AKWAM SCRAPER ====================

async def _scrape_akwam_movies(movie_name, year, client):
    """Internal: Search for movies on Akwam."""
    encoded_name = quote(movie_name)
    url = f"{AKWAM_BASE_URL}/search?q={encoded_name}&section=movie&year={year}&rating=0&formats=0&quality=0"

    response = await client.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    containers = soup.select("div.col-lg-auto.col-md-4.col-6.mb-12")

    if not containers:
        return []

    movies_info = []
    for div in containers:
        tag = div.select_one("h3.entry-title a")
        if not tag:
            continue

        title = tag.text.strip()
        link = tag.get("href", "")

        if link.startswith("/"):
            link = AKWAM_BASE_URL + link

        movies_info.append({"name": title, "link": link})

    return movies_info


async def search_akwam(movie_name, year=0, cutoff=None, user_agent=None, timeout=None):

    try:
        async with _get_client(user_agent, timeout) as client:
            # Search for movies
            movies_list = await _scrape_akwam_movies(movie_name, int(year), client)
            
            # Find best match
            return get_best_match(movie_name, movies_list, cutoff or DEFAULT_FUZZY_CUTOFF)
    except Exception:
        # Return None for any error (network, timeout, parsing, etc.)
        return None

