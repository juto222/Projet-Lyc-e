import os
from colorama import Fore, Style
import time

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Open URL ===\n\n")
    print("""
          
          Options : 

    1. URL à ouvrir
    2. Navigateur à utiliser (par défaut : système)
    3. Ouvrir en fenêtre 
    4. Ouvrir en onglet
    5. Nombre de fois à ouvrir
    6. Délai entre les ouvertures (si option 5 configurée)

          """)
    
def open_url_module():

    choix = {
        "URL à ouvrir": None,
        "Lancer au démarrage": None,
        "Ouvrir en fenêtre": None,
        "Ouvrir en onglet": None,
        "Nombre de fois à ouvrir": 1,
        "Délai entre les ouvertures": 0,
    }

    def url_option():
        clear()
        url = input("Entrez l'URL à ouvrir : ")
        choix["URL à ouvrir"] = url

    def demarrage_option():
        clear()
        demarrage = input("Lancer au démarrage ? (oui/non) : ")
        if demarrage.lower() == "oui":
            choix["Lancer au démarrage"] = True
        else:
            choix["Lancer au démarrage"] = None

    def fenetre_option():
        clear()
        fenetre = input("Ouvrir en fenêtre ? (oui/non) : ")
        if fenetre.lower() == "oui":
            choix["Ouvrir en fenêtre"] = True
        else:
            choix["Ouvrir en fenêtre"] = None

    def onglet_option():
        clear()
        onglet = input("Ouvrir en onglet ? (oui/non) : ")
        if onglet.lower() == "oui":
            choix["Ouvrir en onglet"] = True
        else:
            choix["Ouvrir en onglet"] = None

    def nombre_option():
        clear()
        nombre = input("Nombre de fois à ouvrir l'URL  : ")
        choix["Nombre de fois à ouvrir"] = int(nombre)

    def delai_option():
        clear()
        delai = input("Délai entre les ouvertures en secondes : ")
        choix["Délai entre les ouvertures"] = int(delai)

    options = [
        ("URL à ouvrir", url_option),
        ("Lancer au démarrage", demarrage_option),
        ("Ouvrir en fenêtre", fenetre_option),
        ("Ouvrir en onglet", onglet_option),
        ("Nombre de fois à ouvrir", nombre_option),
        ("Délai entre les ouvertures", delai_option),
    ]

    def create_payload():
        clear()
        print("Création du payload Open URL avec la configuration actuelle...\n")
        filename = "open_url_payload.py"
        with open(filename, "w") as f:
            f.write("import webbrowser\n")
            f.write("import time\n")
            f.write("import os\n")
            f.write("import sys\n\n")

            # Début fonction open_url
            f.write("def open_url():\n")
            f.write(f"    url = '{choix['URL à ouvrir']}'\n")
            if choix["Ouvrir en fenêtre"]:
                f.write("    webbrowser.open_new(url)\n")
            elif choix["Ouvrir en onglet"]:
                f.write("    webbrowser.open_new_tab(url)\n")
            f.write(f"    for _ in range({choix['Nombre de fois à ouvrir']}):\n")
            f.write("        webbrowser.open(url)\n")

    
    while True:
        affichage()
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)

        if cmd.lower() == "exit":
            break

        elif cmd.lower().startswith("set "):
            try:
                option_choix = int(cmd.split()[1]) - 1
                if 0 <= option_choix < len(options):
                    options[option_choix][1]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez saisir 'set'" + Style.RESET_ALL)
                time.sleep(2)

        if cmd.lower() == "show":
            print("\nConfiguration actuelle du module Clipboard :")
            for option, value in choix.items():
                print(f"{option} : {value}")
            input("\nAppuyez sur Entrée pour continuer...")

        if cmd.lower() == "create":
            create_payload()
            break
