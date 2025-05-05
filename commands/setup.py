from constants import SETUP_CREATION_FILES, SETUP_CREATION_FOLDERS
from os.path import exists
from os import makedirs

def setup_files():
    """Creates tracker files if they do not exist."""
    for f in SETUP_CREATION_FILES:
        if not exists(f):
            try:
                with open(f, "w", encoding="utf8") as new_file:
                    pass
            except OSError as e:
                print(f"Error creating file {f}: {e}")


def setup_folders():
    """Creates necessary folders if they do not exist."""
    for f in SETUP_CREATION_FOLDERS:
        if not exists(f):
            try:
                makedirs(f)
                print(f"Created missing folder: {f}")
            except OSError as e:
                print(f"Error creating folder {f}: {e}")