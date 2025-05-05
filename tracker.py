from commands.typing import DownloadCard
from constants import CARD_CACHE_PATH, FIELD_CACHE_PATH
import os

downloaded_cards = set()
downloaded_artworks = set()

def load_cached_ids():
    """Loads all cached ids into memory"""
    global downloaded_cards, downloaded_artworks
    for cache_path, target_set in [(CARD_CACHE_PATH, downloaded_cards), (FIELD_CACHE_PATH, downloaded_artworks)]:
        temp_set = set()
        if os.path.exists(cache_path):
            try:
                with open(cache_path, mode="r", encoding="utf8") as cache_file:
                    temp_set = {c.strip() for c in cache_file.readlines()}
            except Exception as e:
                print(f"Error reading cache file {cache_path}: {e}. Assuming empty.")
        else:
            print(f"Cache file not found: {cache_path}. Will be created if downloads occur.")

        if target_set is downloaded_cards:
            downloaded_cards = temp_set
        else:
            downloaded_artworks = temp_set


def already_downloaded(card: DownloadCard):
    """Returns True if card with id 'card.card_id' was already downloaded"""
    if card.artwork:
        return str(card.card_id) in downloaded_artworks
    else:
        return str(card.card_id) in downloaded_cards

def update_cache_files(newly_downloaded_cards: list[DownloadCard]):
    """Appends successfully downloaded card IDs to the cache files in batches."""
    global downloaded_cards, downloaded_artworks

    cards_to_add = set()
    artworks_to_add = set()

    for card in newly_downloaded_cards:
        card_id_str = str(card.card_id)
        if card.artwork:
            if card_id_str not in downloaded_artworks:
                artworks_to_add.add(card_id_str)
        else:
            if card_id_str not in downloaded_cards:
                cards_to_add.add(card_id_str)

    if cards_to_add:
        try:
            with open(CARD_CACHE_PATH, mode="a", encoding="utf8") as cache_file:
                for card_id_str in cards_to_add:
                    cache_file.write(f"{card_id_str}\n")
            downloaded_cards.update(cards_to_add)
            print(f"Updated card cache with {len(cards_to_add)} new IDs.")
        except Exception as e:
            print(f"\nError writing to card cache file {CARD_CACHE_PATH}: {e}")

    if artworks_to_add:
        try:
            with open(FIELD_CACHE_PATH, mode="a", encoding="utf8") as cache_file:
                 for card_id_str in artworks_to_add:
                    cache_file.write(f"{card_id_str}\n")
            downloaded_artworks.update(artworks_to_add)
            print(f"Updated artwork cache with {len(artworks_to_add)} new IDs.")
        except Exception as e:
             print(f"\nError writing to artwork cache file {FIELD_CACHE_PATH}: {e}")

