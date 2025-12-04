@echo off


REM Mettre à jour pip
echo Mise à jour de pip...
echo 

python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...

python3 -m pip install flet
python3 -m pip install hashlib
python3 -m pip install cryptography pyperclip
python3 -m pip install requests
python3 -m pip install time
python3 -m pip install bs4
python3 -m pip install aiohttp
python3 -m pip install asyncio

echo Toutes les librairies ont été installées.
pause
