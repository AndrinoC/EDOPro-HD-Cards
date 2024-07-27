# EDOPro HD Downloader Fast ⚡

# Installation

## Windows 

*Regular version (command)*
Download the [Latest Release](https://github.com/AndrinoC/EDOPro-Hd-Downloader-FAST/releases) and unzip it at your EDOPro folder (Default should be something like `C:/ProjectIgnis/`).

*Interface version*
Download the [Interface Beta](https://github.com/AndrinoC/EDOPro-Hd-Downloader-FAST/releases/tag/UI-Beta). Same installation as command version. (still working on this version)

## Non-Windows 

Since I can't test non-windows compilations you will need to download the source code and compile it yourself. Then put the compiled file at your EDOPro folder.


# Usage

If you run the program and read the instructions you should be fine.

But for short:

- Select the amount of workers to be used based on your CPU cores. 

- Insert the name of your deck (without the `.ydk` extension) when asked to download all the images of the cards in it.

- Insert `/allcards` to download images for all cards. Will probably take a while.

- Insert `/allfields` to download artwork of all Field Spell Cards.

- Insert `/help` if you want to know anything else.

# Issues

- If no images are downloaded at all or the quality still bad please delete "hd_cards_downloader_tracker" and "hd_fields_downloader_tracker" and try again.
- Requirements.txt might not include all requirements, please check the terminal output and install accordingly or use the compiled version.
- Last few % is a bit slower than the rest due to finishing partial images.

Any new issue or feedback can be shared at the [Issues Tab](https://github.com/AndrinoC/EDOPro-Hd-Downloader-FAST/issues)

# License

Original branch:
[MIT](https://douglas-sebastian.mit-license.org)

My fork:
https://github.com/AndrinoC/EDOPro-Hd-Downloader-FAST/blob/main/LICENSE
