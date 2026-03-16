import os
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print(f"""

          {Fore.YELLOW}Options :    
          {Fore.WHITE}
    1. Port à scanner
    2. Nombre de tentatives de connexion
    3. Délai entre les tentatives (en secondes)
    4. Timeout de la connexion (en secondes)
    5. Afficher les ports ouverts
    6. Afficher les ports fermés
    7. Afficher les ports filtrés
            {Fore.GREEN}

    Sortie et envoi

    9. Envoi sur discord
    10. Envoi sur serveur HTTP
            """)