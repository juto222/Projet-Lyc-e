import random
import string
import time
from Option.utils.display import ask, success, error, log

def generer():

    print(r"""
          _         _____ _  _   _ ____  
__  __   / \  _   _|___ /| || | | |  _ \ 
\ \/ /  / _ \| | | | |_ \| || |_| | |_) |
 >  <  / ___ \ |_| |___) |__   _|_|  _ < 
/_/\_\/_/   \_\__, |____/   |_| (_)_| \_\
              |___/                      
""")

    motif = ask("Pour quel usage")

    try:
        longueur = int(ask("Nombre de caractères (12 minimum recommandé)"))
    except ValueError:
        error("Veuillez entrer un nombre valide.")
        return

    if longueur < 1:
        error("La longueur doit être supérieure à 0.")
        return

    mdp_1 = string.ascii_letters + string.punctuation + string.digits
    mdp   = "".join(random.choices(mdp_1, k=longueur))

    success(f"Mot de passe pour '{motif}' : {mdp}")

    log(f"Création d'un mot de passe pour {motif} ({mdp})")
