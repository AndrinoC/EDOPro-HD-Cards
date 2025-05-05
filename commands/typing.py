from typing import NamedTuple

class DownloadCard(NamedTuple):
    """Represents a card to be downloaded"""

    card_id: int
    artwork: bool

