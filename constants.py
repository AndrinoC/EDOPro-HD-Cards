DOWNLOADER_VERSION = "1.2.0-Forked"
"""Program version"""

REQUEST_HEADERS    = {
	"User-Agent": f"AndrinoC-EDOPro-Hd-Downloader-FAST/{DOWNLOADER_VERSION}"
}
"""Header to be used in an HTTP request"""

INTRO_STRING = f"""EDOPro HD Downloader v{DOWNLOADER_VERSION}
Fork by Andrino
Automatically downloading all missing cards and fields..."""
"""String to be used when starting the program"""

YGOPRODECK_CARDS_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
"""Base API URL for YGOProDeck"""

IMAGES_BASE_URL = "https://images.ygoprodeck.com/images/cards"
"""Base URL for images"""

CARD_CACHE_PATH = "./hd_cards_downloader_tracker"
"""Path to the cards cache file"""

FIELD_CACHE_PATH = "./hd_fields_downloader_tracker"
"""Path to the fields cache file"""

SETUP_CREATION_FILES = (CARD_CACHE_PATH, FIELD_CACHE_PATH)
"""Files needed on setup"""

SETUP_CREATION_FOLDERS = ("pics/field",)
"""Folders needed on setup"""

ID_CONVERSION: dict[int, int] = {
	904186: 31533705
}