from os.path import exists as file_exists, join as path_join
from typing import List, Optional
from commands.typing import CommandReturn, DownloadCard

deck_folder_path = "./deck/"

def filter_card_id(cards: List[str]) -> List[int]:
    """Filters a list of card IDs to remove repeating ones and non-IDs."""
    ids = set()
    for card in cards:
        try:
            card_id = int(card)
            ids.add(card_id)
        except ValueError:
            continue
    return list(ids)

def get_deck(deck_name: str) -> Optional[CommandReturn]:
    """Reads a deck file and returns the IDs of the cards in it."""
    deck_path = path_join(deck_folder_path, f"{deck_name}.ydk")
    if not file_exists(deck_path):
        return None

    with open(deck_path, mode="r", encoding="utf8") as deck:
        cards = filter_card_id([line.strip() for line in deck.readlines()])

    return [DownloadCard(card_id, False) for card_id in cards]
