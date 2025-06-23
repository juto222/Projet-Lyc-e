import os
import time
from colorama import init, Fore, Style
from Option import PingIP
from Option import CheckMDP
from Option import GenererMDP

# Initialisation de Colorama
init(autoreset=True)

# Efface le terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Affiche le menu principal en FR
def afficher_menuFR():
    clear()
    print(f"""{Fore.CYAN}{Style.BRIGHT}
═══════════════════════════════════════════════════════════════════════
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

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════

{Fore.MAGENTA}[1] 🔐 Mot de passe
    {Fore.YELLOW}├── [11] Générateur de mot de passe
    └── [12] Vérificateur de mot de passe

{Fore.MAGENTA}[2] 🛡 Pentest
    {Fore.YELLOW}├── [21] Virus (désactivé)
    ├── [22] Outil DDoS (désactivé)
    └── [23] Générateur de fausse page HTML

{Fore.MAGENTA}[3] 📊 Réseau
    {Fore.YELLOW}├── [31] Ping IP
    ├── [32] Scan Réseau
    └── [33] Journal / Logs

{Fore.MAGENTA}[4] ⚙️ Paramètres
    {Fore.YELLOW}├── [41] Mode sombre / clair
    ├── [42] Choix de langue (FR/EN)
    └── [43] Quitter

{Fore.MAGENTA}[5] ⚖️ Aide & Légalité
    {Fore.YELLOW}├── [51] Documentation utilisateur
    ├── [52] FAQ
    ├── [53] Mentions légales
    └── [54] Informations RGPD
═══════════════════════════════════════════════════════════════════════
{Style.RESET_ALL}""")

# Menu en anglais
def afficher_menuEN():
    clear()
    print(f"""{Fore.CYAN}{Style.BRIGHT}
═══════════════════════════════════════════════════════════════════════
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

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════

{Fore.MAGENTA}[1] 🔐 Password
    {Fore.YELLOW}├── [11] Password Generator
    └── [12] Password Checker

{Fore.MAGENTA}[2] 🛡 Pentest
    {Fore.YELLOW}├── [21] Virus (disabled)
    ├── [22] DDoS Tool (disabled)
    └── [23] Fake HTML Page Generator

{Fore.MAGENTA}[3] 📊 Network
    {Fore.YELLOW}├── [31] Ping IP
    ├── [32] Scan Network
    └── [33] Logs

{Fore.MAGENTA}[4] ⚙️ Settings
    {Fore.YELLOW}├── [41] Dark / Light Mode
    ├── [42] Language Selection (FR/EN)
    └── [43] Quit

{Fore.MAGENTA}[5] ⚖️ Help & Legal
    {Fore.YELLOW}├── [51] User Documentation
    ├── [52] FAQ
    ├── [53] Legal Notice
    └── [54] GDPR Information
═══════════════════════════════════════════════════════════════════════
{Style.RESET_ALL}""")

# Fonction d'exécution sécurisée
def lancer(fonction, nom="Fonction"):
    clear()
    print(Fore.YELLOW + f"[ {nom} ]")
    try:
        fonction()
    except Exception as e:
        print(Fore.RED + f"❌ Erreur : {e}")
    input(Fore.GREEN + "\n✅ Appuyez sur Entrée pour revenir au menu...")

# === Ajout ici : Choix initial de la langue ===
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

    try:
        choix = int(input(Fore.CYAN + "Entrez votre choix / Enter your choice: "))
    except ValueError:
        print(Fore.RED + "❌ Veuillez entrer un numéro valide.")
        time.sleep(1.5)
        continue

    if choix == 11:
        lancer(GenererMDP.generer, "Générateur de mot de passe" if langue_actuelle == "FR" else "Password Generator")

    elif choix == 12:
        lancer(CheckMDP.verifier, "Vérificateur de mot de passe" if langue_actuelle == "FR" else "Password Checker")

    elif choix == 21 or choix == 22:
        clear()
        print(Fore.RED + "❌ Fonction désactivée. / Feature disabled.")
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 31:
        lancer(PingIP.ping, "Ping IP")

    elif choix == 42:
        clear()
        langue_actuelle = input("Choisissez votre langue (FR/EN) : ").upper()
        if langue_actuelle not in ["FR", "EN"]:
            print(Fore.RED + "❌ Langue non reconnue. / Language not recognized.")
            langue_actuelle = "FR"
        else:
            print(Fore.GREEN + f"🌐 Langue définie sur : {langue_actuelle}")
        input(Fore.GREEN + "\nRetour au menu...")

    elif choix == 43:
        clear()
        print(Fore.CYAN + "👋 Fermeture du programme. À bientôt ! / Program closing. See you!")
        break

    elif choix == 51:
        clear()
        print(Fore.YELLOW + (
            "\n📘 Documentation utilisateur :\n- Utilisez les numéros du menu pour accéder aux outils." if langue_actuelle == "FR"
            else "\n📘 User documentation:\n- Use the menu numbers to access tools."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 52:
        clear()
        print(Fore.YELLOW + (
            "\n❓ FAQ :\nQ : Est-ce légal ?\nR : Oui, pour l’apprentissage uniquement." if langue_actuelle == "FR"
            else "\n❓ FAQ:\nQ: Is it legal?\nA: Yes, for learning only."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 53:
        clear()
        print(Fore.YELLOW + (
            "\n⚠️ Mentions légales :\nCe programme est fourni à titre éducatif." if langue_actuelle == "FR"
            else "\n⚠️ Legal Notice:\nThis program is for educational purposes only."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    elif choix == 54:
        clear()
        print(Fore.YELLOW + (
            "\n🔒 Données personnelles :\nCe programme ne collecte aucune information." if langue_actuelle == "FR"
            else "\n🔒 Personal data:\nThis program does not collect any information."
        ))
        input(Fore.GREEN + "\nRetour... / Back...")

    else:
        print(Fore.RED + "❌ Option invalide.")
        time.sleep(1.5)
