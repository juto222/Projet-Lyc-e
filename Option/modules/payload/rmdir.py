import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "[*] === Configuration Remove Directory ===\n" + Style.RESET_ALL)
    print(f"""
          {Fore.YELLOW}Options :
{Fore.WHITE}
    1. Chemin du répertoire à supprimer
    2. Suppression récursive
    3. Délai avant suppression (en secondes)

{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
{Style.RESET_ALL}
    """)

def rmdir_module():
    clear()
    print("[*] === Remove Directory Configuration ===\n")

    choix = {
        "Chemin du répertoire": None,
        "Suppression récursive": False,
        "Délai avant suppression": 0,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def chemin_option():
        clear()
        chemin = input("Entrez le chemin du répertoire à supprimer : ").strip()
        if chemin == "":
            print(Fore.RED + "Le chemin ne peut pas être vide." + Style.RESET_ALL)
            time.sleep(1)
        else:
            choix["Chemin du répertoire"] = chemin
            print(f"Chemin défini sur : {chemin}")
            time.sleep(1)
        affichage()

    def recursive_option():
        clear()
        reponse = input("Suppression récursive ? (y/n) : ").strip().lower()
        if reponse == "y":
            choix["Suppression récursive"] = True
            print("Suppression récursive activée.")
        elif reponse == "n":
            choix["Suppression récursive"] = False
            print("Suppression récursive désactivée.")
        else:
            print(Fore.RED + "Répondez par 'y' ou 'n'." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def delai_option():
        clear()
        delai = input("Délai avant suppression (en secondes, 0 = immédiat) : ").strip()
        try:
            delai = int(delai)
            if delai < 0:
                raise ValueError
            choix["Délai avant suppression"] = delai
            print(f"Délai défini sur {delai} seconde(s).")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre entier positif." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    # -----------------------------------------------
    # Liste des options
    # -----------------------------------------------
    options = [
        ("Chemin du répertoire",     chemin_option),    # 1
        ("Suppression récursive",    recursive_option), # 2
        ("Délai avant suppression",  delai_option),     # 3
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        if choix["Chemin du répertoire"] is None:
            print(Fore.RED + "Erreur : définissez d'abord un chemin (option 1)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "rmdir_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:

            f.write("import os\n")
            f.write("import time\n")
            f.write("import shutil\n")
            # shutil.rmtree : supprime un dossier et tout son contenu (récursif)
            # os.rmdir      : supprime uniquement un dossier VIDE
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"CHEMIN    = {repr(choix['Chemin du répertoire'])}\n")
            f.write(f"RECURSIF  = {choix['Suppression récursive']}\n")
            f.write(f"DELAI     = {choix['Délai avant suppression']}\n")
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Suppression\n")
            f.write("# ============================================================\n\n")

            f.write("def remove_directory():\n\n")

            # Vérification que le chemin existe
            f.write("    # Vérifie que le chemin existe avant de tenter de supprimer\n")
            f.write("    if not os.path.exists(CHEMIN):\n")
            f.write("        print(f'Erreur : le chemin \"{CHEMIN}\" n\\'existe pas.')\n")
            f.write("        return\n\n")

            f.write("    if not os.path.isdir(CHEMIN):\n")
            f.write("        print(f'Erreur : \"{CHEMIN}\" n\\'est pas un répertoire.')\n")
            f.write("        return\n\n")

            # Délai
            f.write("    if DELAI > 0:\n")
            f.write("        print(f'Suppression dans {DELAI} seconde(s)...')\n")
            f.write("        time.sleep(DELAI)\n\n")

            # Suppression
            f.write("    try:\n")
            f.write("        if RECURSIF:\n")
            f.write("            # shutil.rmtree supprime le dossier ET tout ce qu'il contient\n")
            f.write("            shutil.rmtree(CHEMIN)\n")
            f.write("        else:\n")
            f.write("            # os.rmdir ne fonctionne que si le dossier est VIDE\n")
            f.write("            os.rmdir(CHEMIN)\n")
            f.write("        print(f'Répertoire \"{CHEMIN}\" supprimé avec succès.')\n")
            f.write("    except OSError as e:\n")
            f.write("        # OSError est levée si le dossier n'est pas vide (sans récursif)\n")
            f.write("        # ou si les permissions sont refusées\n")
            f.write("        print(f'Erreur lors de la suppression : {e}')\n")
            f.write("        if not RECURSIF:\n")
            f.write("            print('Astuce : activez la suppression récursive si le dossier n\\'est pas vide.')\n\n")

            f.write("if __name__ == '__main__':\n")
            f.write("    remove_directory()\n")

        print(Fore.GREEN + f"Payload généré dans {payload_path}" + Style.RESET_ALL)
        input("\nAppuyez sur Entrée pour continuer...")

    # -----------------------------------------------
    # Boucle principale
    # -----------------------------------------------
    while True:
        affichage()
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL).strip()

        if cmd.lower() == "exit":
            break

        elif cmd.lower().startswith("set "):
            try:
                option_choix = int(cmd.split()[1]) - 1
                if 0 <= option_choix < len(options):
                    options[option_choix][1]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
                    time.sleep(1)
            except (ValueError, IndexError):
                print(Fore.RED + "Veuillez saisir 'set <num>'" + Style.RESET_ALL)
                time.sleep(1)

        elif cmd.lower() == "show":
            clear()
            print(Fore.CYAN + "\nConfiguration actuelle :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value not in (None, False, 0) else Fore.RED
                print(f"  {option:35s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)
