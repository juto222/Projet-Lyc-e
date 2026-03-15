import string
import time

def verifier():
    print(r"""

              __                        __        __
             / /                        \ \      / /
            / /                          \ \    / / 
           / /                            \ \  / /  
__        /_/         ___  ____            \_\/_/   
\ \      / /         / _ \|  _ \          / / \ \   
 \ \    / /         | | | | |_) |        / /   \ \  
  \ \  / /          | |_| |  _ <        / /     \ \ 
   \_\/_/            \___/|_| \_\      /_/       \_\



    """)

    mdp = input("Entrez le mot de passe à vérifier :")

    score = 0

    if len(mdp) >= 8:
        score += 1
    else:
        print("Le mot de passe doit contenir plus de 8 caractères.")

    if any(c in string.digits for c in mdp):
        score += 1

    if any(c in string.punctuation for c in mdp):
        score += 1

    if any(c in string.ascii_uppercase for c in mdp):
        score += 1 

    if score == 4:
        print(f"Mot de passe très fort. Score :{score}/4")
    elif 2 <= score < 4:
        print(f"Mot de passe moyen. Score :{score}/4")
    else:
        print(f"Mot de passe faible. Score :{score}/4")
    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Vérification d'un mot de passe {mdp}    \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )

