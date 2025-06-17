from Option import PingIP
from Option import CheckMDP
from Option import VerifMDP


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

                       github.com/YourRepo/YourTool

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

choix = int(input("Entrez l'option de votre choix : "))

if choix == 11:
  try:
    
