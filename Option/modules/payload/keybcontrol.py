import os
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print(f"""

          {Fore.YELLOW}Options :    
          {Fore.WHITE}
    1. Activer la capture des frappes clavier
    2. Intervalle de capture 'random' pour un temps entre 1 et 10 secondes
    3. Envoi sur discord
    4. Envoi sur serveur HTTP
            {Fore.GREEN}


    Tapez : set <num> pour configurer
    Tapez : show pour afficher la config
    Tapez : create pour générer
    Tapez : exit pour quitter
            """)
    
