import string

def verifier():
    print("""





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
        print("Mot de passe très fort")
    elif 2 <= score < 4:
        print("Mot de passe moyen")
    else:
        print("Mot de passe faible")
    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Vérification d'un mot de passe {mdp}    \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )


