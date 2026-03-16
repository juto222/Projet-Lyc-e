import sys
import os
import webbrowser
import time

# Vérification de la version Python requise (3.11)
required_version = (3, 11)
if sys.version_info[:2] != required_version:
    print(f"Python {required_version[0]}.{required_version[1]} requis. Vous utilisez Python {sys.version_info.major}.{sys.version_info.minor}.")
    rep = input("Voulez-vous continuer quand même sans cx_Freeze ? (y/N) : ").strip().lower()
    if rep not in ("y", "yes"):
        print("Veuillez installer Python 3.11. Ouverture de la page de téléchargement...")
        webbrowser.open("https://www.python.org/downloads/release/python-3110/")
        sys.exit(1)
    else:
        os.environ['SKIP_CX_FREEZE'] = '1'
        print("Continuer sans cx_Freeze. Certaines fonctionnalités liées à la création d'exécutables seront désactivées.")

from colorama import init, Fore, Style
from Option import PingIP
from Option import CheckMDP
from Option import GenererMDP
from Option import phishing
from Option import crypt
from Option import Scan
from Option import quizznetwork
from Option import keylog
from Option import console
from Option import pswd
from Option import keylog
from Option import quizzmdp
from Option import quizzsecurity
from Option import username
from Option import si
from Option import test_speed
from Option import script
from Option import subdomain
from Option import iplookup
from Option import dirbuster

# Initialisation de Colorama
init(autoreset=True)

# Efface le terminal
def clear():
    os.system('cls')

# Affiche le menu principal en FR
def afficher_menuFR():
    clear()
    print(f"""{Fore.CYAN}{Style.BRIGHT}
                                 {Fore.GREEN}
                                              @                                                                                                                  
                                           @@@@@@                                                                                                               
                                         @@@@@@@                                                                                                                
                                      @@@@@@@@   @@                @@@@           @@@@@       @@@@@@@@@@     @@@@@@@@                                                         
                                   @@@@@@@@   @@@@@@@           @@@@@@@@@@@    @@@@   @@@@    @@@    @@@   @@@    @@@                                            
                                   @@@@@@@@@@@@@@@@            @@@            @@@       @@@   @@@    @@@   @@@    @@@                                           
                                     @@@@@@@@@@@@   @@@@@      @@@           @@@         @@@  @@@@@@@@@    @@@@@@@@@                                            
                                       @@@@@@@@   @@@@@@@@     @@@            @@@       @@@   @@@   @@@    @@@                                                  
                                        @@@@@@@@@@@@@@@         @@@@@@@@@@@    @@@@   @@@@    @@@    @@@   @@@                                                  
                                          @@@@@@@@@@                @@@@          @@@@@       @@@    @@@@  @@@                                                 
                                            @@@@@@                                                                                                               
                                             @@               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        

{Fore.GREEN}
                                                    Allez voir notre Gestionnaire de mot de passe !!!!
                                                    http://linganguliguli.worldlite.fr/


{Fore.MAGENTA}[1] 🔐 Mot de passe                                                     {Fore.MAGENTA}[5] 🧩 Autres
 {Fore.YELLOW}├── [11] Générateur de mot de passe                                     ├── [51] Recherche d'utilisateur
 ├── [12] Vérificateur de mot de passe                                   ├── [52] Gestionnaire de mot de passe
 ├── [13] Quizz mot de passe                                             ├── [53] Chiffrage de fichier python
 └── [14] Mot de passe compromis                                         ├── [54] Déchiffrage de fichier python
                                                                         └── [55] Console interactive   


{Fore.MAGENTA}[2] 🛡  Pentest                                                          {Fore.MAGENTA}[6] ⚙️ Paramètres
 {Fore.YELLOW}├── [21] DirBuster                                                      ├── [61] Mode sombre / clair
 ├── [22] Générateur de fausse page HTML                                 ├── [62] Choix de langue (FR/EN)
 ├── [23] Keylogger                                                      └── [63] Quitter
 ├── [24] Quizz sécurité
 └── [25] Scanner de sites web


{Fore.MAGENTA}[3] 📊 Réseau                                                           {Fore.MAGENTA}[7] ⚖️ Aide & Légalité
 {Fore.YELLOW}├── [31] Ping IP                                                        ├── [71] Documentation utilisateur
 ├── [32] Scan Réseau                                                    ├── [72] FAQ
 ├── [33] Journal / Logs                                                 ├── [73] Mentions légales
 ├── [34] Quizz réseau                                                   └── [74] Informations RGPD
 ├── [35] Info sur l'IP
 └── [36] Speedtest Internet


{Fore.MAGENTA} [4] PC
 {Fore.YELLOW} ├── [41] Informations système
  ├── [42] Gestionnaire de tâches
  ├── [43] Nettoyeur de fichiers temporaires
  └── [44] Création de faux fichier


{Style.RESET_ALL}""")

# Menu en anglais
def afficher_menuEN():
    clear()
    print(f"""{Fore.CYAN}{Style.BRIGHT}
                                {Fore.CYAN}
                                 {Fore.GREEN}
                                              @                                                                                                                  
                                           @@@@@@                                                                                                               
                                         @@@@@@@                                                                                                                
                                      @@@@@@@@   @@                @@@@           @@@@@       @@@@@@@@@@     @@@@@@@@                                                         
                                   @@@@@@@@   @@@@@@@           @@@@@@@@@@@    @@@@   @@@@    @@@    @@@   @@@    @@@                                            
                                   @@@@@@@@@@@@@@@@            @@@            @@@       @@@   @@@    @@@   @@@    @@@                                           
                                     @@@@@@@@@@@@   @@@@@      @@@           @@@         @@@  @@@@@@@@@    @@@@@@@@@                                            
                                       @@@@@@@@   @@@@@@@@     @@@            @@@       @@@   @@@   @@@    @@@                                                  
                                        @@@@@@@@@@@@@@@         @@@@@@@@@@@    @@@@   @@@@    @@@    @@@   @@@                                                  
                                          @@@@@@@@@@                @@@@          @@@@@       @@@    @@@@  @@@                                                 
                                            @@@@@@                                                                                                               
                                             @@               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        
                                 {Fore.CYAN}

{Fore.GREEN}
                                                    Check out our Password Manager !!!!
                                                    http://linganguliguli.worldlite.fr/


{Fore.MAGENTA}[1] 🔐 Password                                                         {Fore.MAGENTA}[5] 🧩 Others
 {Fore.YELLOW}├── [11] Password Generator                                          ├── [51] Username Search
 ├── [12] Password Checker                                            ├── [52] Password Manager
 ├── [13] Password Quiz                                               ├── [53] Python File Encryption
 └── [14] Compromised Passwords                                       ├── [54] Python File Decryption
                                                                      └── [55] Interactive Console

{Fore.MAGENTA}[2] 🛡 Pentest                                                           {Fore.MAGENTA}[6] ⚙️ Settings
 {Fore.YELLOW}├── [21] DirBuster                                                   ├── [61] Dark / Light Mode
 ├── [22] Fake HTML Page Generator                                    ├── [62] Language Choice (FR/EN)
 ├── [23] Keylogger                                                   └── [63] Exit
 ├── [24] Security Quiz
 └── [25] Website Scanner 


{Fore.MAGENTA}[3] 📊 Network                                                           {Fore.MAGENTA}[7] ⚖️ Help & Legal
 {Fore.YELLOW}├── [31] Ping IP                                                     ├── [71] User Documentation
 ├── [32] Scan Network                                                ├── [72] FAQ
 ├── [33] Logs                                                        ├── [73] Legal Notice
 ├── [34] Network Quiz                                                └── [74] GDPR Information
 ├── [35] IP Lookup
 └── [36] Internet Speedtest


{Fore.MAGENTA} [4] PC
 {Fore.YELLOW} ├── [41] System Information
  ├── [42] Task Manager
  ├── [43] Temporary File Cleaner
  └── [44] Fake File Creator

{Style.RESET_ALL}""")

# execution securisé
def lancer(fonction, nom="Fonction"):
    clear()
    print(Fore.YELLOW + f"[ {nom} ]")
    try:
        fonction()
    except Exception as e:
        print(Fore.RED + f"❌ Erreur : {e}")
    input(Fore.GREEN + "\n✅ Appuyez sur Entrée pour revenir au menu...")

# Langue
clear()
langue_actuelle = input(Fore.CYAN + "🌐 Choisissez votre langue / Choose your language (FR/EN) : ").upper()
if langue_actuelle != "EN":
    langue_actuelle = "FR"  # FR par défaut

# Boucle principale
while True:
    if langue_actuelle == "EN":
        afficher_menuEN()
    else:
        afficher_menuFR()

    import os
    import getpass
    import socket
    import ctypes
    from colorama import Fore
    
    def est_admin():
        try:
            # Windows
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            # Linux / macOS
            return os.geteuid() == 0
    
    def generer_prompt(langue_actuelle):
        utilisateur = getpass.getuser()   # nom de l'utilisateur actuel
        machine = socket.gethostname()    # nom du PC
        symbole = "#" if est_admin() else "$"
    
        if langue_actuelle == "FR":
            return Fore.CYAN + f"{utilisateur}@{machine} {symbole} "
        else:
            return Fore.CYAN + f"{utilisateur}@{machine} {symbole} "
    

    try:
        prompt = generer_prompt(langue_actuelle)
        choix = int(input(prompt))
    except ValueError:
        if langue_actuelle == "FR":
            print(Fore.RED + "❌ Veuillez entrer un numéro valide.")
        else:
            print(Fore.RED + "❌ Please enter a valid number.")
        time.sleep(1.5)
        continue

    # PARTIE MOT DE PASSE

    if choix == 11:
        lancer(GenererMDP.generer, "Générateur de mot de passe" if langue_actuelle == "FR" else "Password Generator")

    elif choix == 12:
        lancer(CheckMDP.verifier, "Vérificateur de mot de passe" if langue_actuelle == "FR" else "Password Checker")

    elif choix == 13:
        clear()
        lancer(lambda: quizzmdp.quizz_mdp(langue_actuelle), "Quizz mot de passe" if langue_actuelle == "FR" else "Password Quiz")

    elif choix == 14:
        clear()
        lancer(pswd.pswd_compromis, "Mot de passe compromis" if langue_actuelle == "FR" else "Compromised Passwords")
    # PARTIE PENTEST

    elif choix == 21:
        clear()
        lancer(dirbuster.dirbuster, "Dirbuster" if langue_actuelle == "FR" else "Dirbuster")

    elif choix == 22:
        clear()
        lancer(lambda: phishing.afficher_menu_phishing(langue_actuelle),
       "Générateur de fausse page HTML" if langue_actuelle == "FR" else "Fake HTML Page Generator")
        
    elif choix == 23:
        clear()
        lancer(keylog.key, "Keylogger" if langue_actuelle == "FR" else "Keylogger")

    elif choix == 24:
        clear()
        if langue_actuelle == "FR":
            level = input("Choisissez le niveau de difficulté (1-Facile, 2-Moyen, 3-Difficile) : ")
        else:
            level = input("Choose difficulty level (1-Easy, 2-Medium, 3-Hard): ")
        lancer(lambda: quizzsecurity.quizzsecurity(level), "Quizz sécurité" if langue_actuelle == "FR" else "Security Quiz")

    elif choix == 25:
        clear()
        lancer(subdomain.sousdomaine, "Scanner de sites web" if langue_actuelle == "FR" else "Website Scanner")

    
#   PARTIE RESEAU


    elif choix == 31:
        lancer(PingIP.ping, "Ping IP" if langue_actuelle == "FR" else "Ping IP")

    elif choix == 32:
       clear()
       lancer(Scan.scan, "Scan Réseau" if langue_actuelle == "FR" else "Network Scan")
       input(Fore.GREEN + "\nRetour... / Back...")
    
    elif choix == 33: 
        clear()
        with open("logs.txt", "r") as f:
            logs = f.read()
            print(Fore.YELLOW + logs)
            input(Fore.GREEN + "\nRetour... / Back...")
        
    elif choix == 34:
        clear()
        lancer(quizznetwork.quizznetwork, "Quizz réseau" if langue_actuelle == "FR" else "Network Quiz")

    elif choix == 35:
        clear()
        lancer(iplookup.obtenir_infos_ip, "Info sur l'IP" if langue_actuelle == "FR" else "IP Lookup")

    elif choix == 36:
        clear()
        lancer(test_speed.test_speed, "Speedtest Internet" if langue_actuelle == "FR" else "Internet Speedtest")

    # PARTIE PC

    elif choix == 41:
        clear()
        lancer(si.info_system, "Informations système" if langue_actuelle == "FR" else "System Information")
        
    elif choix == 45:
        clear()
        lancer(script.fichier, "Création de faux fichier" if langue_actuelle == "FR" else "Fake File Creator")

    # PARTIE AUTRES

    elif choix == 51:
        clear()
        lancer(username.username, "Recherche d'utilisateur" if langue_actuelle == "FR" else "Username Lookup")

    elif choix == 52:
        clear()
        webbrowser.open("http://linganguliguli.worldlite.fr/")

    elif choix == 53:
        clear()
        lancer(crypt.crypt, "Chiffrage de fichier python" if langue_actuelle == "FR" else "Python File Encryption")

    elif choix == 54:
        print(Fore.RED + "❌ Fonction non encore implémentée. / Feature not yet implemented.")
        input(Fore.GREEN + "\nRetour... / Back...")
    
    elif choix == 55:
        clear()
        lancer(console.console, "Console" if langue_actuelle == "FR" else "Console")

    # PARTIE PARAMETRES

    elif choix == 61:
        clear()
        if langue_actuelle == "FR":
            mode = input("Choisissez le mode (sombre/clair) : ").lower()
            if mode == "sombre":
                os.system('')  # Placeholder for dark mode
                print(Fore.GREEN + "🌙 Mode sombre activé.")
            elif mode == "clair":
                os.system('')  # Placeholder for light mode
                print(Fore.GREEN + "☀️ Mode clair activé.")
            else:
                print(Fore.RED + "❌ Mode non reconnu.")
            input(Fore.GREEN + "\nRetour au menu...")
        else:
            mode = input("Choose mode (dark/light): ").lower()
            if mode == "dark":
                os.system('')  # Placeholder for dark mode
                print(Fore.GREEN + "🌙 Dark mode activated.")
            elif mode == "light":
                os.system('')  # Placeholder for light mode
                print(Fore.GREEN + "☀️ Light mode activated.")
            else:
                print(Fore.RED + "❌ Mode not recognized.")
            input(Fore.GREEN + "\nReturn to menu...")

    elif choix == 62:
        clear()
        langue_actuelle = input("Choisissez votre langue (FR/EN) : ").upper()
        if langue_actuelle not in ["FR", "EN"]:
            print(Fore.RED + "❌ Langue non reconnue. / Language not recognized.")
            langue_actuelle = "FR"
        else:
            print(Fore.GREEN + f"🌐 Langue définie sur : {langue_actuelle}")
        input(Fore.GREEN + "\nRetour au menu...")

    elif choix == 63:
        clear()
        print(Fore.CYAN + "👋 Fermeture du programme. À bientôt ! / Program closing. See you!")
        break

    # PARTIES AIDE & LEGAL

    elif choix == 71:
        clear()
        print(Fore.YELLOW + (
            "\n📘 Documentation utilisateur :\n- Utilisez les numéros du menu pour accéder aux outils." if langue_actuelle == "FR"
            else "\n📘 User documentation:\n- Use the menu numbers to access tools."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 72:
        clear()
        print(Fore.YELLOW + (
            "\n❓ FAQ :\nQ : Est-ce légal ?\nR : Oui, pour l’apprentissage uniquement." if langue_actuelle == "FR"
            else "\n❓ FAQ:\nQ: Is it legal?\nA: Yes, for learning only."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 73:
        clear()
        print(Fore.YELLOW + (
            "\n⚠️ Mentions légales :\nCe programme est fourni à titre éducatif." if langue_actuelle == "FR"
            else "\n⚠️ Legal Notice:\nThis program is for educational purposes only."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 74:
        clear()
        print(Fore.YELLOW + (
            "\n🔒 Données personnelles :\nCe programme ne collecte aucune information." if langue_actuelle == "FR"
            else "\n🔒 Personal data:\nThis program does not collect any information."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    else:
        print(Fore.RED + "❌ Option invalide.")
        time.sleep(1.5)

