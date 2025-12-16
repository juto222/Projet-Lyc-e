import os
from colorama import Fore, Style
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
    6. Nombre de fois à ouvrir
    7. Délai entre les ouvertures (si option 6 configurée)
            
            Sortie et envoi:
    8. Envoi sur discord
    9. Envoi par HTTP
          """)
    
def open_url_module():

    choix = {
        "URL à ouvrir": None,
        "Lancer au démarrage": None,
        "Ouvrir en fenêtre": None,
        "Ouvrir en onglet": None,
        "Nombre de fois à ouvrir": None,
        "Délai entre les ouvertures": None,
        "Envoi sur Discord": None,
        "Envoi par HTTP": None,
    }

    def url_option():
        clear()
        url = input("Entrez l'URL à ouvrir : ")
        choix["URL à ouvrir"] = url

    def demarrage_option():
        clear()
        demarrage = input("Lancer au démarrage ? (oui/non) : ")
        choix["Lancer au démarrage"] = demarrage.lower() == "oui"

    def fenetre_option():
        clear()
        fenetre = input("Ouvrir en fenêtre ? (oui/non) : ")
        choix["Ouvrir en fenêtre"] = fenetre.lower() == "oui"

    def onglet_option():
        clear()
        onglet = input("Ouvrir en onglet ? (oui/non) : ")
        choix["Ouvrir en onglet"] = onglet.lower() == "oui"

    def nombre_option():
        clear()
        nombre = input("Nombre de fois à ouvrir l'URL (laisser vide pour 1) : ")
        choix["Nombre de fois à ouvrir"] = int(nombre) if nombre.isdigit() else 1

    def delai_option():
        clear()
        delai = input("Délai entre les ouvertures en secondes (laisser vide pour 0) : ")
        choix["Délai entre les ouvertures"] = int(delai) if delai.isdigit() else 0

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
            f.write("import time\n\n")

            # Début fonction open_url
            f.write("def open_url():\n")

    
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

        if cmd.lower() == "show":
            print("\nConfiguration actuelle du module Clipboard :")
            for option, value in choix.items():
                print(f"{option} : {value}")
            input("\nAppuyez sur Entrée pour continuer...")

        if cmd.lower() == "create":
            create_payload()
            break
