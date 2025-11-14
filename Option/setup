@echo off
REM Vérifie si Python est installé
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b
)

REM Mettre à jour pip
echo Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les librairies nécessaires
echo Installation des librairies...
python -m pip install requests
python -m pip install pynput
python -m pip install customtkinter

echo Toutes les librairies ont été installées.
pause
