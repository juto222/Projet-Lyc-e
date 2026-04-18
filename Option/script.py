import os
import time
from Option.utils.display import ask, success, error, info, result, log

def fichier():


    print(r"""
     _____ ___ _     _____
    |  ___|_ _| |   | ____|
    | |_   | || |   |  _|
    |  _|  | || |___| |___
    |_|   |___|_____|_____|
""")

    try:
        size_mb = int(ask("Taille du fichier à créer (en Mo)"))
    except ValueError:
        error("Entrez un nombre valide.")
        return

    if size_mb <= 0:
        error("La taille doit être supérieure à 0.")
        return

    path = ask("Chemin de destination (ex: C:/test.bin)")

    dossier = os.path.dirname(path)
    if dossier:
        os.makedirs(dossier, exist_ok=True)

    size_bytes = size_mb * 1024 * 1024
    chunk_size = 1024 * 1024  # 1 Mo par chunk

    info(f"Création d'un fichier de {size_mb} Mo en cours...")

    try:
        with open(path, "wb") as f:
            for i in range(size_mb):
                f.write(os.urandom(chunk_size))
                print(f"\r  Progression : {i + 1}/{size_mb} Mo", end="", flush=True)

        print()
        success(f"Fichier de {size_mb} Mo créé : {path}")
        result("Taille réelle", f"{os.path.getsize(path) / (1024**2):.2f} Mo")
        log(f"Fichier binaire aléatoire de {size_mb} Mo créé → {path}")

    except PermissionError:
        error(f"Permission refusée pour écrire dans : {path}")
    except Exception as e:
        error(f"Erreur lors de la création : {e}")
