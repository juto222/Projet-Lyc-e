import string
import time
from Option.utils.display import ask, success, warning, error, result, log

def verifier():

    print(r"""
  __     __   ___  ____  
  \ \   / /  / _ \|  _ \    
   \ \ / /  | | | | |_) |
    \ V /   | |_| |  _ < 
     \_/     \___/|_| \_\
""")

    mdp   = ask("Mot de passe à vérifier")
    score = 0

    if len(mdp) >= 8:
        score += 1
    else:
        warning("Le mot de passe doit contenir au moins 8 caractères.")

    if any(c in string.digits for c in mdp):
        score += 1
    else:
        warning("Aucun chiffre détecté.")

    if any(c in string.punctuation for c in mdp):
        score += 1
    else:
        warning("Aucun symbole détecté (!@#$...).")

    if any(c in string.ascii_uppercase for c in mdp):
        score += 1
    else:
        warning("Aucune majuscule détectée.")

    result("Score", f"{score}/4")

    if score == 4:
        success("Mot de passe très fort !")
    elif 2 <= score < 4:
        warning("Mot de passe moyen — peut être amélioré.")
    else:
        error("Mot de passe faible — à changer absolument.")

    log(f"Vérification d'un mot de passe — score {score}/4")
