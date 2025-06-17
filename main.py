from Option import PingIP
from Option import CheckMDP
from Option import VerifMDP

def afficher_menu():
    print("""                                                                                                                                                                                                                                                                                                                                                 
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

═══════════════════════════════════════════════════════════════════════
[1] 🔐 Mot de passe
    ├── [11] Générateur de mot de passe
    ├── [12] Vérificateur de mot de passe
      
[2] 🛡 Pentest
    ├── [21] Virus
    ├── [22] Outil DDoS
    ├── [23] Générateur de fausse page HTML

[3] 📊 Réseau
    ├── [31] Ping IP
    ├── [32] Journal / Logs

[4] ⚙️ Paramètres
    ├── [41] Mode sombre / clair
    ├── [42] Choix de langue (FR/EN)
    └── [43] Exit
      
[5] ⚖️ Aide & Légalité
    ├── [51] Documentation utilisateur
    ├── [52] FAQ
    ├── [53] Mentions légales & avertissement d’usage
    └── [54] Informations RGPD
═══════════════════════════════════════════════════════════════════════
    """)

# Boucle principale du menu
while True:
    afficher_menu()
    
    try:
        choix = int(input("Entrez l'option de votre choix : "))
    except ValueError:
        print("❌ Veuillez entrer un numéro valide.")
        continue

    # Mot de passe
    if choix == 11:
        try:
            CheckMDP.verifier()
        except Exception as e:
            print(f"❌ Erreur générateur : {e}")

    elif choix == 12:
        try:
            GenererMDP.generer()
        except Exception as e:
            print(f"❌ Erreur vérification : {e}")

    # Pentest
    elif choix == 21:
        print("🛡 Fonction Virus : Cette fonction est désactivée à des fins de sécurité.")

    elif choix == 22:
        print("❌ Outil DDoS non disponible. Ce type d’outil est illégal en dehors d’un cadre autorisé.")

    elif choix == 23:
        print("🛠 Générateur de fausse page HTML : en développement...")

    # Réseau
    elif choix == 31:
        try:
            PingIP.ping()
        except Exception as e:
            print(f"❌ Erreur de ping : {e}")

    elif choix == 32:
        print("📄 Journaux réseau : fonctionnalité en développement...")

    # Paramètres
    elif choix == 41:
        print("🌓 Changement de thème : clair/sombre... (simulé)")

    elif choix == 42:
        langue = input("Choisissez votre langue (FR/EN) : ").upper()
        if langue in ["FR", "EN"]:
            print(f"🌐 Langue définie sur : {langue}")
        else:
            print("❌ Langue non reconnue.")

    elif choix == 43:
        print("👋 Fermeture du programme. À bientôt !")
        break

    # Aide & Légalité
    elif choix == 51:
        print("""
📘 Documentation utilisateur :
- Utilisez les numéros du menu pour accéder aux outils.
- Les modules sensibles sont désactivés par défaut pour respecter la légalité.
""")

    elif choix == 52:
        print("""
❓ FAQ :
Q : Cette app est-elle légale ?
R : Oui, si utilisée à des fins pédagogiques uniquement.

Q : Puis-je modifier ce script ?
R : Bien sûr, sous réserve de respecter la loi.
""")

    elif choix == 53:
        print("""
⚠️ Mentions légales & Avertissement :
Ce programme est fourni uniquement à des fins éducatives.
L’auteur décline toute responsabilité en cas d’usage illégal.
""")

    elif choix == 54:
        print("""
🔒 Informations RGPD :
Ce programme ne collecte ni ne conserve aucune donnée personnelle.
""")

    else:
        print("❌ Option invalide. Veuillez choisir un numéro parmi ceux listés.")
