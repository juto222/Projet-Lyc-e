import os
from colorama import Fore, Style
def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Shutdown Payload ===\n\n")
    print(f"""
          
          Options : 

    1. Délai avant extinction (en secondes)
    2. Message d'avertissement à afficher
    3. Forcer la fermeture des applications

              {Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter{Style.RESET_ALL}
          """)
    
def shutdown_module():
    clear()
    choix = {
        "Délai avant extinction": None,
        "Message d'avertissement": None,
        "Forcer la fermeture des applications": None,
    }

    def delai_option():
        clear()
        delai = input("Entrez le délai avant extinction en secondes : ")
        choix["Délai avant extinction"] = int(delai)

    def message_option():
        clear()
        message = input("Voulez vous afficher un message d'avertissement ? (oui/non) : ")
        if message.lower() == "oui":
            message = input("Entrez le message d'avertissement : ")
            choix["Message d'avertissement"] = f"{message}"
        else:
            message = None
            choix["Message d'avertissement"] = message


    def force_option():
        clear()
        force = input("Forcer la fermeture des applications ? (oui/non) : ")
        if force.lower() == "oui":
            choix["Forcer la fermeture des applications"] = True
        else:
            choix["Forcer la fermeture des applications"] = None

    options = [
        ("Délai avant extinction", delai_option),
        ("Message d'avertissement", message_option),
        ("Forcer la fermeture des applications", force_option), 
    ]
    def create_payload():
        clear()
        print("Création du payload Shutdown avec la configuration suivante :")
        filename = "shutdown_payload.py"
        with open(filename, "w") as f:
            f.write("import os\n")
            f.write("import time\n\n")
            f.write("def shutdown_system():\n")
            if choix["Délai avant extinction"] is not None:
                f.write(f"    time.sleep({choix['Délai avant extinction']})\n")
            command = "shutdown /s"
            if choix["Forcer la fermeture des applications"]:
                command += " /f"
            if choix["Message d'avertissement"]:
                command += f" /c \"{choix['Message davertissement']}\""
            f.write(f"    os.system('{command}')\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    shutdown_system()\n")
        print(f"Payload Shutdown créé : {filename}")
    
    while True:
        affichage()
        cmd = input(">> ")
        if cmd.lower() == "exit":
            break
        elif cmd.lower().startswith("set "):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 4):
                    option_funcs = {
                        1: delai_option,
                        2: message_option,
                        3: force_option,
                    }
                    option_funcs[option_num]()
                else:
                    print("Numéro d'option invalide.")
            except (IndexError, ValueError):
                print("Commande invalide. Utilisez : set <num>")
        elif cmd.lower() == "show":
            clear()
            print("\nConfiguration actuelle du module Shutdown :")
            for key, value in choix.items():
                print(f"{key}: {value}")
            input("\nAppuyez sur Entrée pour continuer...")
        elif cmd.lower() == "create":
            create_payload()
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("Commande invalide.")
