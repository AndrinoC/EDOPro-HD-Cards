import requests
from os.path import join
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from commands.typing import DownloadCard
from constants import IMAGES_BASE_URL
from id_conversor import convert_id

# Session with retry mechanism for better stability
session = requests.Session()

# Retry mechanism with exponential backoff
retry_strategy = Retry(
    total=3,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=frozenset(["GET", "HEAD", "OPTIONS"]),
    backoff_factor=1  # Exponential backoff factor
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

def download_image(card: DownloadCard) -> bool:
    """
    Downloads the card image or artwork and saves it in the specified folder.

    Returns `True` if download is successful, otherwise returns `False`.
    """
    url = IMAGES_BASE_URL

    if card.artwork:
        url += "_cropped"
        store_at = "./pics/field/"
    else:
        store_at = "./pics/"

    url += f"/{card.card_id}.jpg"
    file_path = join(store_at, f"{convert_id(card.card_id)}.jpg")

    try:
        with session.get(url, stream=True) as res:
            res.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading '{card.card_id}': {type(e).__name__}\n{e}")
        return False
    except Exception as e:
        print(f"Error: {type(e).__name__}\n{e}")
        return False
