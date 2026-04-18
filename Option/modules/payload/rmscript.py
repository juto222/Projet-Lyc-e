import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "[*] === Configuration Remove Script ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Nom du script à supprimer (avec extension ex: .exe)
    2. Délai avant suppression (en secondes)
    3. Chercher dans tous les dossiers parents (ou seulement le dossier courant)
        
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

def rmscript():
    clear()
    print("[*] === Remove Script Configuration ===\n\n")

    choix = {
        "Nom du script à supprimer": None,
        "Délai avant suppression": None,
        "Recherche récursive": None,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def script_option():
        clear()
        script = input("Entrez le nom du script à supprimer (avec extension, ex: tool.exe) : ").strip()
        if script == "":
            print(Fore.RED + "Le nom ne peut pas être vide." + Style.RESET_ALL)
            time.sleep(1)
            affichage()
            return
        choix["Nom du script à supprimer"] = script
        print(f"Script défini sur : {script}")
        time.sleep(1)
        affichage()

    def delai_option():
        clear()
        delai = input("Délai avant suppression (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Délai avant suppression"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def recursif_option():
        clear()
        reponse = input("Activer la recherche récursive (cherche dans tous les sous-dossiers) ? (y/n) : ").lower()
        choix["Recherche récursive"] = reponse == 'y'
        print(f"Recherche récursive : {'activée' if choix['Recherche récursive'] else 'désactivée'}.")
        time.sleep(1)
        affichage()

    # -----------------------------------------------
    # Liste des options (même ordre que le menu)
    # -----------------------------------------------
    options = [
        ("Nom du script à supprimer", script_option),
        ("Délai avant suppression",   delai_option),
        ("Recherche récursive",        recursif_option),
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        # Le nom du script est obligatoire
        if choix["Nom du script à supprimer"] is None:
            print(Fore.RED + "Erreur : vous devez définir le nom du script à supprimer (option 1)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Dossier de sortie
        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "rmscript_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import time\n")
            f.write("\n")

            # --- Variables de configuration ---
            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"NOM_SCRIPT  = {repr(choix['Nom du script à supprimer'])}\n")
            f.write(f"DELAI       = {choix['Délai avant suppression'] or 0}\n")
            f.write(f"RECURSIF    = {choix['Recherche récursive'] if choix['Recherche récursive'] is not None else False}\n")
            f.write("\n")

            # --- Logique de suppression ---
            f.write("# ============================================================\n")
            f.write("# Suppression\n")
            f.write("# ============================================================\n\n")

            f.write("def trouver_et_supprimer():\n")
            f.write('    """\n')
            f.write("    Cherche NOM_SCRIPT dans le dossier courant (ou récursivement)\n")
            f.write("    et le supprime s'il est trouvé.\n")
            f.write('    """\n\n')

            f.write("    if DELAI > 0:\n")
            f.write("        print(f\"Attente de {DELAI} secondes avant suppression...\")\n")
            f.write("        time.sleep(DELAI)\n\n")

            f.write("    dossier_base = os.getcwd()\n")
            f.write("    supprime = False\n\n")

            f.write("    if RECURSIF:\n")
            f.write("        # os.walk descend dans tous les sous-dossiers\n")
            f.write("        for dossier, sous_dossiers, fichiers in os.walk(dossier_base):\n")
            f.write("            if NOM_SCRIPT in fichiers:\n")
            f.write("                chemin = os.path.join(dossier, NOM_SCRIPT)\n")
            f.write("                try:\n")
            f.write("                    os.remove(chemin)\n")
            f.write("                    print(f\"Supprimé : {chemin}\")\n")
            f.write("                    supprime = True\n")
            f.write("                except Exception as e:\n")
            f.write("                    print(f\"Erreur suppression {chemin} : {e}\")\n")
            f.write("    else:\n")
            f.write("        # Cherche uniquement dans le dossier courant\n")
            f.write("        chemin = os.path.join(dossier_base, NOM_SCRIPT)\n")
            f.write("        if os.path.isfile(chemin):\n")
            f.write("            try:\n")
            f.write("                os.remove(chemin)\n")
            f.write("                print(f\"Supprimé : {chemin}\")\n")
            f.write("                supprime = True\n")
            f.write("            except Exception as e:\n")
            f.write("                print(f\"Erreur suppression : {e}\")\n\n")

            f.write("    if not supprime:\n")
            f.write("        print(f\"Fichier introuvable : {NOM_SCRIPT}\")\n\n")

            f.write("# Point d'entrée\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    trouver_et_supprimer()\n")

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
            print(Fore.CYAN + "\nConfiguration actuelle du module Remove Script :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:30s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)

