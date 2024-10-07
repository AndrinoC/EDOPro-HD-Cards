import asyncio
from commands.setup import setup_commands, setup_files, setup_folders
from constants import INPUT_STRING, INTRO_STRING
from input_handler import handle_input
from web_access.downloader import download_images
from tracker import already_downloaded, load_cached_ids

def initialize():
    """Creates tracker files if they do not exist, sets up commands, and introduces the program."""
    setup_files()
    setup_folders()
    setup_commands()
    load_cached_ids()
    print(INTRO_STRING)

def remove_downloaded(cards):
    """Filters out already downloaded cards unless they are forced to be re-downloaded."""
    return [card for card in cards if card.force or not already_downloaded(card)]

def main():
    initialize()

    try:
        while True:
            cards = handle_input(input(INPUT_STRING))
            if cards is None:
                print("Deck or command not found.")
                continue

            cards = remove_downloaded(cards)
            asyncio.run(download_images(cards))

            print("\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
