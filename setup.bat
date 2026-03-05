@echo off
REM Mise à jour de pip
echo Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...
pip install --upgrade requests pynput customtkinter colorama psutil speedtest-cli clipboard Pillow dnspython bs4 aiohttp
py -3.11 -m pip install cx_Freeze
pip install pyarmor==8.5.7
pip install nuitka

echo Toutes les librairies ont été installées.
pause

