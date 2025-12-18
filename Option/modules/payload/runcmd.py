import code
import os
import time
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Run Command on terminal ===\n\n")
    print(f"""
          
          Options : 

    1. Commande à exécuter
    2. Lancer au démarrage
    3. Exécuter en boucle
    4. Délai entre les exécutions (en secondes)
          
    {Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter

          """)
    
def runcmd_module():
    clear()
    affichage()
    choix = {
        "Commande à exécuter": None,
        "Lancer au démarrage": None,
        "Exécuter en boucle": None,
        "Délai entre les exécutions": 0,
    }

    def commande_option():
        clear()
        commande = input("Entrez la commande à exécuter : ")
        choix["Commande à exécuter"] = commande

    def demarrage_option():
        clear()
        demarrage = input("Lancer au démarrage ? (oui/non) : ")
        if demarrage.lower() == "oui":
            choix["Lancer au démarrage"] = True
        else:
            choix["Lancer au démarrage"] = None

    def boucle_option():
        clear()
        boucle = input("Exécuter en boucle ? (oui/non) : ")
        if boucle.lower() == "oui":
            choix["Exécuter en boucle"] = True
        else:
            choix["Exécuter en boucle"] = None

    def delai_option():
        clear()
        delai = input("Délai entre les exécutions en secondes : ")
        choix["Délai entre les exécutions"] = int(delai)

    options = [
        ("Commande à exécuter", commande_option),    
        ("Lancer au démarrage", demarrage_option),
        ("Exécuter en boucle", boucle_option),
        ("Délai entre les exécutions", delai_option),
    ]

    def create_payload():
        clear()
        print("Création du payload Run Command on terminal avec la configuration suivante :") 

        if choix["Lancer au démarrage"]:
            loop_code += f"""
    # Création d'un fichier batch pour l'exécution au démarrage
    autorun_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'runcmd_payload.bat')
    with open(r "autorun_path", "w") as bat_file:
        bat_file.write(f'python "{{os.path.abspath(__file__)}}"')\n"""

        if choix["Exécuter en boucle"]:
            loop_code = f"""
    while True:
        os.system("{choix['Commande à exécuter']}")"""
        else:
            loop_code = f"""
    os.system("{choix['Commande à exécuter']}")"""
            
        if choix["Délai entre les exécutions"] > 0:
            loop_code += f"""
        time.sleep({choix['Délai entre les exécutions']})"""
            
        
            


        code = f"""
import os
import time
def runcmd():
{loop_code}

    """
        with open("Option/modules/payload/payload_created/runcmd_payload.py", "w") as f:
            f.write(code) 
    

    while True:
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)
        if cmd.lower() == "exit":
            break
        if cmd.lower().startswith("set"):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 11):
                    option_funcs = {
                        1: commande_option,
                        2: demarrage_option,
                        3: boucle_option,
                        4: delai_option,
                    }
                    option_funcs[option_num]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez saisir 'set'" + Style.RESET_ALL)

        if cmd.lower() == "show":
            clear()
            print("\nConfiguration actuelle du module Run Command on terminal :")
            for key, value in choix.items():
                print(f"{key}: {value}")

        if cmd.lower() == "create":

            create_payload()
            break

if __name__ == "__main__":  
    runcmd_module()
