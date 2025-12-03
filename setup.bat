@echo off


REM Mettre à jour pip
echo Mise à jour de pip...
echo 

python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...
py -3.11 -m pip install requests
py -3.11 -m pip install pynput
py -3.11 -m pip install customtkinter
py -3.11 -m pip install colorama
py -3.11 -m pip install psutil
py -3.11 -m pip install speedtest-cli
py -3.11 -m pip install cx-Freeze
py -3.11 -m pip install clipboard
py -3.11 -m pip install Pillow
py -3.11 -m pip install shutil
py -3.11 -m pip install tkinter
py -3.11 -m pip install psutil
py -3.11 -m pip install getpass
py -3.11 -m pip install dnspython
py -3.11 -m pip install bs4
py -3.11 -m pip install aiohttp



echo Toutes les librairies ont été installées.
pause

