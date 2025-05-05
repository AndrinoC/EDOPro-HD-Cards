import asyncio
import os
import traceback
from commands.setup import setup_files, setup_folders
from constants import INTRO_STRING, CARD_CACHE_PATH, FIELD_CACHE_PATH
from web_access.downloader import download_images
from tracker import already_downloaded, load_cached_ids, update_cache_files
from web_access.ygoprodeck_api import get_all_cards, get_all_fields
from commands.typing import DownloadCard

def initialize():
    """Creates tracker files/folders if they do not exist and loads cache."""
    print("Initializing...")
    setup_files()
    setup_folders()
    load_cached_ids()
    print(INTRO_STRING)

def get_all_cards_to_download() -> list[DownloadCard]:
    """Fetches all card and field IDs from the API."""
    print("Fetching card lists from API...")
    all_card_ids = get_all_cards()
    all_field_ids = get_all_fields()
    print(f"Found {len(all_card_ids)} cards and {len(all_field_ids)} fields.")

    cards_to_download = []
    for card_id in all_card_ids:
        if card_id:
            cards_to_download.append(DownloadCard(card_id=card_id, artwork=False))
    for card_id in all_field_ids:
         if card_id:
            cards_to_download.append(DownloadCard(card_id=card_id, artwork=True))
    return cards_to_download

def remove_downloaded(cards: list[DownloadCard]) -> list[DownloadCard]:
    """Filters out cards that are already present in the cache."""
    print("Filtering already downloaded images...")
    filtered_cards = [card for card in cards if not already_downloaded(card)]
    print(f"Found {len(filtered_cards)} new images to download.")
    return filtered_cards

def cleanup_tracker_files():
    """Removes the temporary tracking files."""
    print("\nCleaning up temporary tracking files...")
    files_to_remove = [CARD_CACHE_PATH, FIELD_CACHE_PATH]
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
            else:
                print(f"File not found (already removed or not created): {file_path}")
        except OSError as e:
            print(f"Error removing file {file_path}: {e}")

def main():
    initialize()
    process_completed = False
    final_http_error_count = 0

    try:
        all_potential_downloads = get_all_cards_to_download()
        cards_to_actually_download = remove_downloaded(all_potential_downloads)
        total_to_attempt = len(cards_to_actually_download)

        if cards_to_actually_download:
            print(f"\nStarting download of {total_to_attempt} images...")
            successful_cards, http_errors = asyncio.run(download_images(cards_to_actually_download))
            final_http_error_count = http_errors
            successful_count = len(successful_cards)

            if successful_cards:
                update_cache_files(successful_cards)

            print(f"\nDownload finished. Success: {successful_count}/{total_to_attempt}. HTTP errors: {final_http_error_count}.")
            process_completed = True
        else:
            print("\nNo new images to download. Everything is up to date!")
            process_completed = True

    except Exception as e:
        print(f"\nAn error occurred during the process: {type(e).__name__} - {e}")
        traceback.print_exc()
    finally:
        if process_completed:
            cleanup_tracker_files()
        else:
            print("\nTracking files kept due to an error or interruption during the process.")

        print("\nProcess finished.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()