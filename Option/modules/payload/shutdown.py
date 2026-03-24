import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Shutdown Payload ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Délai avant extinction (en secondes)
    2. Message d'avertissement à afficher
    3. Forcer la fermeture des applications
    4. Afficher un compte à rebours
        
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

def shutdown_module():
    clear()
    print("=== Shutdown Configuration ===\n\n")

    choix = {
        "Délai avant extinction": None,
        "Message d'avertissement": None,
        "Forcer la fermeture": None,
        "Compte à rebours": None,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def delai_option():
        clear()
        delai = input("Délai avant extinction (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Délai avant extinction"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def message_option():
        clear()
        reponse = input("Afficher un message d'avertissement ? (y/n) : ").lower()
        if reponse == 'y':
            message = input("Entrez le message : ").strip()
            if message == "":
                print(Fore.RED + "Le message ne peut pas être vide." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Message d'avertissement"] = message
            print(f"Message défini : '{message}'")
        else:
            choix["Message d'avertissement"] = None
            print("Aucun message d'avertissement.")
        time.sleep(1)
        affichage()

    def force_option():
        clear()
        reponse = input("Forcer la fermeture des applications ? (y/n) : ").lower()
        choix["Forcer la fermeture"] = reponse == 'y'
        print(f"Fermeture forcée : {'activée' if choix['Forcer la fermeture'] else 'désactivée'}.")
        time.sleep(1)
        affichage()

    def rebours_option():
        clear()
        reponse = input("Afficher un compte à rebours dans le terminal ? (y/n) : ").lower()
        choix["Compte à rebours"] = reponse == 'y'
        print(f"Compte à rebours : {'activé' if choix['Compte à rebours'] else 'désactivé'}.")
        time.sleep(1)
        affichage()

    # -----------------------------------------------
    # Liste des options (même ordre que le menu)
    # -----------------------------------------------
    options = [
        ("Délai avant extinction",  delai_option),
        ("Message d'avertissement", message_option),
        ("Forcer la fermeture",     force_option),
        ("Compte à rebours",        rebours_option),
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        # Dossier de sortie
        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "shutdown_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import time\n")
            f.write("\n")

            # --- Variables de configuration ---
            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"DELAI       = {choix['Délai avant extinction'] or 0}\n")
            msg = repr(choix["Message d'avertissement"])
            f.write(f"MESSAGE     = {msg}\n")
            f.write(f"FORCE       = {choix['Forcer la fermeture'] if choix['Forcer la fermeture'] is not None else False}\n")
            f.write(f"REBOURS     = {choix['Compte à rebours'] if choix['Compte à rebours'] is not None else False}\n")
            f.write("\n")

            # --- Logique ---
            f.write("# ============================================================\n")
            f.write("# Shutdown\n")
            f.write("# ============================================================\n\n")

            # Fonction compte à rebours
            f.write("def afficher_compte_rebours(secondes):\n")
            f.write('    """Affiche un compte à rebours dans le terminal."""\n')
            f.write("    for i in range(secondes, 0, -1):\n")
            f.write("        print(f\"  Extinction dans {i} seconde(s)...\", end=\"\\r\")\n")
            f.write("        time.sleep(1)\n")
            f.write("    print()\n\n")

            # Fonction principale
            f.write("def lancer_shutdown():\n")

            f.write("    # Affichage du message d'avertissement\n")
            f.write("    if MESSAGE:\n")
            f.write("        print(f\"Avertissement : {MESSAGE}\")\n\n")

            f.write("    # Compte à rebours ou simple attente\n")
            f.write("    if DELAI > 0:\n")
            f.write("        if REBOURS:\n")
            f.write("            afficher_compte_rebours(DELAI)\n")
            f.write("        else:\n")
            f.write("            time.sleep(DELAI)\n\n")

            # Commande selon l'OS
            f.write("    # Construction de la commande selon l'OS\n")
            f.write("    if os.name == 'nt':  # Windows\n")
            f.write("        cmd = 'shutdown /s /t 0'\n")
            f.write("        if FORCE:\n")
            f.write("            cmd += ' /f'\n")
            # Le message sur Windows passe via /c mais ne peut pas contenir de guillemets doubles
            f.write("        if MESSAGE:\n")
            f.write("            # /c affiche un message dans la boîte de dialogue Windows\n")
            f.write("            msg_propre = MESSAGE.replace('\"', \"'\")\n")
            f.write("            cmd += f' /c \"{msg_propre}\"'\n")
            f.write("    else:  # Linux / macOS\n")
            f.write("        cmd = 'sudo shutdown -h now'\n\n")

            f.write("    print(f\"Exécution : {cmd}\")\n")
            f.write("    os.system(cmd)\n\n")

            f.write("# Point d'entrée\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    lancer_shutdown()\n")

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
            print(Fore.CYAN + "\nConfiguration actuelle du module Shutdown :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:40s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)

