@echo off


REM Mettre à jour pip
echo Mise à jour de pip...
echo 

python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...

pip install flet
pip install hashlib
pip install cryptography pyperclip
pip install requests
pip install time
pip install bs4
pip install aiohttp
pip install asyncio

echo Toutes les librairies ont été installées.
pause
