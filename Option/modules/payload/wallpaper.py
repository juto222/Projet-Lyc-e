import os
from colorama import Fore, Style


def clear():
    os.system("cls")

def affichage():
    clear()
    print("[*] === Configuration Wallpaper Payload ===\n\n")
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Mettre un Wallpaper

              {Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter{Style.RESET_ALL}
          """)

def wallpaper():
    clear()
    print("[*] === Wallpaper Configuration ===\n")

    choix = {
        "Mettre un Wallpaper": None,
    }

    option = [
        ("Mettre un Wallpaper", wallpaper_option),
    ]

    def wallpaper_option():
        clear()
        path = input("Entrez le chemin complet de l'image à définir comme wallpaper : ")
        if os.path.isfile(path):
            choix["Mettre un Wallpaper"] = path
        else:
            print("Le chemin spécifié n'est pas valide.")
        affichage()


    def create_payload():
        clear()
        print("[+] === Payload Wallpaper Généré ===\n")
        if choix["Mettre un Wallpaper"]:
            wallpaper_path = choix["Mettre un Wallpaper"]
            payload = f"""
def set_wallpaper():
    import ctypes
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, r"{wallpaper_path}", 3)

set_wallpaper()
            """
        payload_path = os.path.join("Option", "modules", "payload", "payload_created", "wallpaper_payload.py")
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
                        1: wallpaper_option,
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
