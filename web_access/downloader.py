import aiohttp
import asyncio
from os.path import join
from constants import IMAGES_BASE_URL
from id_conversor import convert_id
import os

async def download_image(session, card, progress, total_cards, lock) -> bool:
    """
    Downloads the card image asynchronously and saves it.
    Updates the progress counter after each download.
    """
    url = IMAGES_BASE_URL
    store_at = "./pics/field/" if card.artwork else "./pics/"

    url += "_cropped" if card.artwork else ""
    url += f"/{card.card_id}.jpg"
    file_path = join(store_at, f"{convert_id(card.card_id)}.jpg")

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            await save_image(file_path, content)

            async with lock:
                progress['count'] += 1
                percentage = f"{(progress['count'] * 100 / total_cards):.2f}%"
                print(f"Downloaded {progress['count']}/{total_cards} - {percentage}", end="\r")

        return True
    except Exception as e:
        print(f"Error downloading '{card.card_id}': {e}")
        return False

async def download_images(cards):
    """
    Concurrently downloads all images using asyncio.
    Updates progress for each downloaded image.
    """
    total_cards = len(cards)
    progress = {'count': 0}
    lock = asyncio.Lock()

    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, card, progress, total_cards, lock) for card in cards]
        await asyncio.gather(*tasks)

async def save_image(file_path, content):
    """
    Saves the image file asynchronously.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    loop = asyncio.get_event_loop()
    with open(file_path, 'wb') as f:
        await loop.run_in_executor(None, f.write, content)
