from commands.typing import DownloadCard
from constants import CARD_CACHE_PATH, FIELD_CACHE_PATH

downloaded_cards = set()
downloaded_artworks = set()

def load_cached_ids():
    """Loads all cached ids into memory"""
    global downloaded_cards, downloaded_artworks
    with open(CARD_CACHE_PATH, mode="r+", encoding="utf8") as card_cache_file:
        downloaded_cards = {c.strip() for c in card_cache_file.readlines()}
    with open(FIELD_CACHE_PATH, mode="r+", encoding="utf8") as artwork_cache_file:
        downloaded_artworks = {c.strip() for c in artwork_cache_file.readlines()}

def already_downloaded(card: DownloadCard):
    """Returns True if card with id 'card.card_id' was already downloaded"""
    if card.artwork:
        return str(card.card_id) in downloaded_artworks
    else:
        return str(card.card_id) in downloaded_cards

def mark_as_downloaded(card: DownloadCard):
    """Opens tracker file to add an id to the downloaded list"""
    cache = FIELD_CACHE_PATH if card.artwork else CARD_CACHE_PATH

    with open(cache, mode="a+", encoding="utf8") as cache_file:
        cache_file.write(f"{card.card_id}\n")
    
    if card.artwork:
        downloaded_artworks.add(str(card.card_id))
    else:
        downloaded_cards.add(str(card.card_id))
