@echo off
echo Installing Requirements...

pip install -r requirements.txt

echo Building the executable (EDOProHDDownloader.exe)...

pyinstaller --onefile --name EDOProHDDownloader main.py

set "EXE_SOURCE=dist\EDOProHDDownloader.exe"
set "EXE_DEST=EDOProHDDownloader.exe"

move /Y "%EXE_SOURCE%" "%EXE_DEST%" > nul

echo The executable file (EDOProHDDownloader.exe) is now located in the project root folder (this folder).
pause