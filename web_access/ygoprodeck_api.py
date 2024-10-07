from typing import List
from requests import Response
from constants import YGOPRODECK_CARDS_URL
from web_access.request_helper import make_request

def _get_ids_from_response(response: Response) -> List[int]:
    """Returns only the ids of the cards from a JSON response."""
    data = response.json().get("data", [])
    return [img.get("id") for c in data for img in c.get("card_images", [])]

def _fetch_card_ids(url: str, params: dict = None) -> List[int]:
    """Fetches card IDs from the specified URL with optional parameters."""
    try:
        response = make_request(url, params=params)
        response.raise_for_status()
        return _get_ids_from_response(response)
    except Exception as e:
        print(f"Error fetching {url}: {type(e).__name__}\n{e}")
        return []

def get_all_cards() -> List[int]:
    """Returns the ids of all Yu-Gi-Oh! cards in `db.ygoprodeck.com` database."""
    return _fetch_card_ids(YGOPRODECK_CARDS_URL)

def get_all_fields() -> List[int]:
    """
    Returns the ids of all Yu-Gi-Oh! Field Spell cards in
    `db.ygoprodeck.com` database.
    """
    return _fetch_card_ids(YGOPRODECK_CARDS_URL, params={"type": "spell card", "race": "field"})

def get_all_tokens() -> List[int]:
    """
    Returns the ids of all Tokens in the `db.ygoprodeck.com` database.
    """
    return _fetch_card_ids(YGOPRODECK_CARDS_URL, params={"type": "token"})
