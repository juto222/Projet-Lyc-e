@echo off


REM Mettre à jour pip
echo Mise à jour de pip...
echo 

python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...

py -3.11 -m pip install flet
py -3.11 -m pip install hashlib
py -3.11 -m pip install cryptography pyperclip
py -3.11 -m pip install requests
py -3.11 -m pip install time
py -3.11 -m pip install bs4


echo Toutes les librairies ont été installées.
pause
