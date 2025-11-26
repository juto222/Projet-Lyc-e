@echo off
REM Vérifie si Python est installé
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé. Veuillez installer python.3.11.  avec le PATH.exe !!
    pause
    exit /b
)

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
py -3.11 -m pip install PIL
py -3.11 -m pip install shutil
py -3.11 -m pip install tkinter
py -3.11 -m pip install psutil
py -3.11 -m pip install getpass



echo Toutes les librairies ont été installées.
pause
