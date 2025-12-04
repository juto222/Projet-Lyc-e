@echo off


REM Mettre à jour pip
echo Mise à jour de pip...
echo 

python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...
python3 -m pip install requests
python3 -m pip install pynput
python3 -m pip install customtkinter
python3 -m pip install colorama
python3 -m pip install psutil
python3 -m pip install speedtest-cli
python3 -m pip install cx-Freeze
python3 -m pip install clipboard
python3 -m pip install Pillow
python3 -m pip install shutil
python3 -m pip install tkinter
python3 -m pip install psutil
python3 -m pip install getpass
python3 -m pip install dnspython
python3 -m pip install bs4
python3 -m pip install aiohttp



echo Toutes les librairies ont été installées.
pause


