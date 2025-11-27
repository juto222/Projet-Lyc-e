from colorama import Fore, Style
import time
import os

def fichier():
    print(f"""

    {Fore.MAGENTA} Création d'un vrai fichier binaire (octets aléatoires)
    {Style.RESET_ALL}

    """)

    size_mb = int(input("Taille du fichier que vous voulez créer (en Mo) : "))
    path = input("Chemin du fichier (ex: C:/mon/chemin/test.bin) : ")

    if os.makedirs(os.path.dirname(path), exist_ok=True):
        pass

    size_bytes = size_mb * 1024 * 1024
    chunk_size = 1024 * 1024  # 1 Mo à la fois (évite de tuer la RAM)

    print(f"\n{Fore.YELLOW}Création du fichier... Ça peut prendre du temps pour les gros fichiers.{Style.RESET_ALL}\n")

    with open(path, "wb") as f:
        for _ in range(size_mb):
            f.write(os.urandom(chunk_size))  # Octets totalement aléatoires

    print(f"{Fore.GREEN}Fichier binaire de {size_mb} Mo créé : {path}{Style.RESET_ALL}\n")

    # Logs
    with open("logs.txt", "a", encoding="utf-8") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Fichier binaire aléatoire de {size_mb} Mo → {path}\n"
            f"------------------------------------\n\n"
        )
