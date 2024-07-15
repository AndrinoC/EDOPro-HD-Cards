import sys
import os
from time import sleep
from traceback import print_exc
from commands.setup import setup_commands, setup_files, setup_folders
from constants import DOWNLOADER_VERSION, INPUT_STRING, INTRO_STRING, SLEEP_TIME_BETWEEN_DOWNLOADS

from input_handler import handle_input
from commands.typing import DownloadCard
from web_access.downloader import download_image
from tracker import already_downloaded, mark_as_downloaded, load_cached_ids

from threading import Lock, Event
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pprint

def initialize():
    """Creates tracker files if they do not exist, setups all commands and
    introduces the program
    """
    setup_files()
    setup_folders()
    setup_commands()
    load_cached_ids()  # Load cached IDs here
    print(INTRO_STRING)

def to_download(card: DownloadCard):
    """Handles if a card should be downloaded and downloads it."""
    if (card.force) or (not already_downloaded(card)):
        success = download_image(card)
        if success: mark_as_downloaded(card)

def down_loop(card, total_cards, progress, lock, stopper):
    if stopper.is_set():
        return
    to_download(card)
    with lock:
        if stopper.is_set():
            return
        progress['count'] += 1
        percentage = f"{((progress['count'] * 100) / total_cards):.2f}%"
        print(f"Downloaded {progress['count']}/{total_cards} - {percentage}", end="\r")

def remove_downloaded(cards):
    return [card for card in cards if card.force or not already_downloaded(card)]

def get_num_workers():
    """Prompt user for number of worker threads based on CPU cores."""
    num_cores = os.cpu_count() or 1  # Fallback to 1 if os.cpu_count() returns None
    print(f"Detected {num_cores} CPU cores.")
    try:
        num_workers = int(input(f"Enter number of worker threads (1-{num_cores}): "))
        if num_workers < 1 or num_workers > num_cores:
            raise ValueError("Number of workers must be between 1 and the number of CPU cores.")
        return num_workers
    except ValueError as e:
        print(f"Invalid input: {e}")
        return get_num_workers()

def main():
    initialize()
    stopper = Event()
    lock = Lock()

    try:
        num_workers = get_num_workers()

        while True:
            cards = handle_input(input(INPUT_STRING))
            if cards is None:
                print("Deck or command not found.")
                continue

            total_cards = len(cards)
            cards = remove_downloaded(cards)

            progress = {'count': total_cards - len(cards)}

            # Create a thread pool executor with specified number of workers
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = [executor.submit(down_loop, card, total_cards, progress, lock, stopper) for card in cards]

                # Check for KeyboardInterrupt while waiting for futures to complete
                try:
                    for future in as_completed(futures):
                        if stopper.is_set():
                            break
                except KeyboardInterrupt:
                    print("\n\nForcing program interruption...")
                    stopper.set()
                    # Cancel all running futures
                    for future in futures:
                        future.cancel()
                    break

            print("\n")

    except Exception:
        print_exc()

    finally:
        stopper.set()  # Ensure stopper is set to exit any running threads

if __name__ == "__main__":
    main()
