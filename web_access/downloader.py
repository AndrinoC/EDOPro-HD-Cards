import aiohttp
import asyncio
from os.path import join, dirname
from constants import IMAGES_BASE_URL, REQUEST_HEADERS
from id_conversor import convert_id
from commands.typing import DownloadCard
import os

DOWNLOAD_TIMEOUT = 30

DOWNLOAD_SUCCESS = 1
DOWNLOAD_HTTP_ERROR = 0
DOWNLOAD_OTHER_ERROR = -1

async def download_image(session, card: DownloadCard, progress, total_cards, lock) -> tuple[int, DownloadCard | None]:
    """
    Downloads the card image asynchronously and saves it.
    Updates the progress counter.
    Returns a status code (DOWNLOAD_SUCCESS, DOWNLOAD_HTTP_ERROR, DOWNLOAD_OTHER_ERROR)
    and the card object on success, otherwise None.
    """
    url = IMAGES_BASE_URL
    store_at = "./pics/field/" if card.artwork else "./pics/"
    url += "_cropped" if card.artwork else ""
    url += f"/{card.card_id}.jpg"
    converted_id = convert_id(card.card_id)
    file_path = join(store_at, f"{converted_id}.jpg")
    os.makedirs(dirname(file_path), exist_ok=True)

    status = DOWNLOAD_OTHER_ERROR
    downloaded_card_obj = None

    try:
        async with session.get(url, timeout=DOWNLOAD_TIMEOUT) as response:
            response.raise_for_status()
            content = await response.read()

            loop = asyncio.get_event_loop()
            with open(file_path, 'wb') as f:
                await loop.run_in_executor(None, f.write, content)

            status = DOWNLOAD_SUCCESS
            downloaded_card_obj = card

    except asyncio.TimeoutError:
        print(f"\nTimeout error downloading '{card.card_id}' from {url}")
        status = DOWNLOAD_OTHER_ERROR
    except aiohttp.ClientResponseError as http_err:
        status = DOWNLOAD_HTTP_ERROR
    except aiohttp.ClientError as client_err:
        print(f"\nClient error downloading '{card.card_id}': {client_err} from {url}")
        status = DOWNLOAD_OTHER_ERROR
    except Exception as e:
        print(f"\nUnexpected error processing '{card.card_id}': {type(e).__name__} - {e}")
        status = DOWNLOAD_OTHER_ERROR
    finally:
        async with lock:
            progress['count'] += 1
            percentage = f"{(progress['count'] * 100 / total_cards):.2f}%"
            print(f"Processed {progress['count']}/{total_cards} - {percentage}".ljust(50), end="\r")

    return status, downloaded_card_obj


async def download_images(cards: list[DownloadCard]) -> tuple[list[DownloadCard], int]:
    """
    Concurrently downloads all images using asyncio.
    Updates progress for each image.
    Returns a list of successfully downloaded DownloadCard objects and the count of HTTP errors.
    """
    total_cards_to_attempt = len(cards)
    if total_cards_to_attempt == 0:
        print("No new images to download.")
        return [], 0

    progress = {'count': 0}
    lock = asyncio.Lock()
    successfully_downloaded_cards: list[DownloadCard] = []
    http_error_count = 0

    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(connector=connector, headers=REQUEST_HEADERS) as session:
        tasks = [download_image(session, card, progress, total_cards_to_attempt, lock) for card in cards]
        results = await asyncio.gather(*tasks)

    for status, card_obj in results:
        if status == DOWNLOAD_SUCCESS and card_obj:
            successfully_downloaded_cards.append(card_obj)
        elif status == DOWNLOAD_HTTP_ERROR:
            http_error_count += 1

    print(f"\nFinished processing {total_cards_to_attempt} cards.")
    return successfully_downloaded_cards, http_error_count