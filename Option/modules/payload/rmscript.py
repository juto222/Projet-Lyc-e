import os
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Remove Script ===\n\n")
    print(f"""
          


          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Nom du script à supprimer (avec extension ex: .exe)
          
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}

          """)

def rmscript():
    clear()
    choix = {
        "Nom du script à supprimer": None,
    }

    def script_option():
        clear()
        script = input("Entrez le nom du script à supprimer (avec extension ex: .exe) : ")
        choix["Nom du script à supprimer"] = script

    def create_payload():
        clear()
        print("=== Payload Remove Script Généré ===\n")
        if choix["Nom du script à supprimer"]:
            script_name = choix["Nom du script à supprimer"]
            payload = f"""
import os
def remove_script():
    script_path = os.path.join(os.getcwd(), r"{script_name}")
    if os.path.isfile(script_path):
        os.remove(script_path)

remove_script()
            """ 
        payload_path = os.path.join("Option", "modules", "payload", "payload_created", "rmscript_payload.py")
        os.makedirs(os.path.dirname(os.path.abspath(payload_path)), exist_ok=True)
        with open(payload_path, "w", encoding="utf-8") as f:
            f.write(payload)

    while True:
        affichage()
        cmd = input(">> ")
        if cmd.lower() == "exit":
            break
        elif cmd.lower().startswith("set "):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 2):
                    option_funcs = {
                        1: script_option,
                    }
                    option_funcs[option_num]()
                else:
                    print("Numéro d'option invalide.")
            except (IndexError, ValueError):
                print("Commande invalide. Utilisez : set <num>")
        elif cmd.lower() == "show":
            clear()
            print("\nConfiguration actuelle du module Remove Script :")
            for key, value in choix.items():
                print(f"{key}: {value}")
            input("\nAppuyez sur Entrée pour continuer...")
        elif cmd.lower() == "create":
            create_payload()
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("Commande invalide.")
