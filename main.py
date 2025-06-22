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

# Affiche le menu principal
def afficher_menu():
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

{Fore.MAGENTA}[1] {Fore.MAGENTA}🔐 Mot de passe
    {Fore.YELLOW}├── [11] Générateur de mot de passe
    └── [12] Vérificateur de mot de passe

{Fore.MAGENTA}[2] 🛡 Pentest
    {Fore.YELLOW}├── [21] Virus (désactivé)
    ├── [22] Outil DDoS (désactivé)
    └── [23] Générateur de fausse page HTML

{Fore.MAGENTA}[3] 📊 Réseau
    {Fore.YELLOW}├── [31] Ping IP
    └── [32] Journal / Logs

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

# Fonction simplifiée pour exécuter proprement
def lancer(fonction, nom="Fonction"):
    clear()
    print(Fore.YELLOW + f"[ {nom} ]")
    try:
        fonction()
    except Exception as e:
        print(Fore.RED + f"❌ Erreur : {e}")
    input(Fore.GREEN + "\n✅ Appuyez sur Entrée pour revenir au menu...")

# Boucle principale du menu
while True:
    afficher_menu()

    try:
        choix = int(input(Fore.CYAN + "Entrez l'option de votre choix : "))
    except ValueError:
        print(Fore.RED + "❌ Veuillez entrer un numéro valide.")
        time.sleep(1.5)
        continue

    # Mot de passe
    if choix == 11:
        lancer(GenererMDP.generer, "Générateur de mot de passe")

    elif choix == 12:
        lancer(CheckMDP.verifier, "Vérificateur de mot de passe")

    # Pentest
    elif choix == 21:
        clear()
        print(Fore.RED + "🛡 Fonction Virus : désactivée pour raisons de sécurité.")
        input(Fore.GREEN + "\nRetour...")
    elif choix == 22:
        clear()
        print(Fore.RED + "❌ Outil DDoS non disponible. Illégal sans autorisation.")
        input(Fore.GREEN + "\nRetour...")

    # Réseau
    elif choix == 31:
        lancer(PingIP.ping, "Ping IP")


    # Paramètres
    elif choix == 42:
        clear()
        langue = input("Choisissez votre langue (FR/EN) : ").upper()
        if langue in ["FR", "EN"]:
            print(Fore.GREEN + f"🌐 Langue définie sur : {langue}")
        else:
            print(Fore.RED + "❌ Langue non reconnue.")
        input(Fore.GREEN + "\nRetour au menu...")

    elif choix == 43:
        clear()
        print(Fore.CYAN + "👋 Fermeture du programme. À bientôt !")
        break

    # Aide & Légalité
    elif choix == 51:
        clear()
        print(Fore.YELLOW + """
📘 Documentation utilisateur :
- Utilisez les numéros du menu pour accéder aux outils.
- Les modules sensibles sont désactivés pour rester légaux.
""")
        input(Fore.GREEN + "\nRetour...")

    elif choix == 52:
        clear()
        print(Fore.YELLOW + """
❓ FAQ :
Q : Est-ce légal ?
R : Oui, pour l’apprentissage uniquement.

Q : Puis-je modifier ce script ?
R : Oui, tant que vous respectez la loi.
""")
        input(Fore.GREEN + "\nRetour...")

    elif choix == 53:
        clear()
        print(Fore.YELLOW + """
⚠️ Mentions légales :
Ce programme est fourni à titre éducatif.
L’auteur décline toute responsabilité en cas d’abus.
""")
        input(Fore.GREEN + "\nRetour...")

    elif choix == 54:
        clear()
        print(Fore.YELLOW + """
🔒 Données personnelles :
Ce programme ne collecte aucune information.
""")
        input(Fore.GREEN + "\nRetour...")

    else:
        print(Fore.RED + "❌ Option invalide.")
        time.sleep(1.5)
