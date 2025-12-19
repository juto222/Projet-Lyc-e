import os
from colorama import Fore, Style
def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Directory Listing ===\n\n")
    print("""

            Options :
    1. Chemin du répertoire à lister
    2. Inclure les fichiers cachés
    3. Délai avant listing (en secondes)

            """)
    
def directory_listing_module():
    clear()
    choix = {
        "Chemin du répertoire à lister": None,
        "Inclure les fichiers cachés": None,
        "Délai avant listing": None,
    }

    def chemin_option():
        clear()
        chemin = input("Entrez le chemin du répertoire à lister : ")
        choix["Chemin du répertoire à lister"] = chemin

    def cache_option():
        clear()
        cache = input("Inclure les fichiers cachés ? (oui/non) : ")
        if cache.lower() == "oui":
            choix["Inclure les fichiers cachés"] = True
        else:
            choix["Inclure les fichiers cachés"] = None

    def delai_option():
        clear()
        delai = input("Délai avant listing en secondes : ")
        choix["Délai avant listing"] = int(delai)

    options = [
        ("Chemin du répertoire à lister", chemin_option),    
        ("Inclure les fichiers cachés", cache_option),
        ("Délai avant listing", delai_option),
    ]
    def create_payload():
        clear()
        print("Création du payload Directory Listing avec la configuration suivante :")
        filename = "dirlist_payload.py"
        with open(filename, "w") as f:
            f.write("import os\n")
            f.write("import time\n\n")
            f.write("def list_directory():\n")
            if choix["Délai avant listing"] is not None:
                f.write(f"    time.sleep({choix['Délai avant listing']})\n")
            chemin = choix["Chemin du répertoire à lister"] or "."
            if choix["Inclure les fichiers cachés"]:
                f.write(f"    files = os.listdir(r'{chemin}')\n")
            else:
                f.write(f"    files = [f for f in os.listdir(r'{chemin}') if not f.startswith('.')] \n")
            f.write("    for file in files:\n")
            f.write("        print(file)\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    list_directory()\n")
        print(f"Payload créé et sauvegardé dans {filename}")
        
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
