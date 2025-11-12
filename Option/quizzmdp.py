from colorama import Fore, Style
import time

def quizz_mdp():
    print(f"""

    {Fore.CYAN}
══════════════════════════════════════════════════════════════════════
        ascii art quizz mot de passe ici
══════════════════════════════════════════════════════════════════════


     {Fore.MAGENTA} Quiz sur les mots de passe

    """)

    level = input("Choisissez le niveau de difficulté (1 - Facile, 2 - Moyen, 3 - Difficile) : ")

    if level not in ['1', '2', '3']:
        print(f"{Fore.RED}Erreur : Niveau invalide. Veuillez choisir 1, 2 ou 3.{Style.RESET_ALL}")
        return
    
    score = 0 

    question_facile = ["À quoi sert un mot de passe ?",
                       "Faut-il garder son mot de passe secret ?",
                       "Est-ce une bonne idée de dire ton mot de passe à un ami ?",
                       "Un mot de passe doit-il être long et complexe ?",
                       "Est-il sûr d'utiliser le même mot de passe pour plusieurs comptes ?",
                       "Un mot de passe doit-il contenir des chiffres et des symboles ?",
                       "Si ton mot de passe est trop simple, que peut-il arriver ?",
                       "Est-il important de changer régulièrement son mot de passe ?",
                       "Un mot de passe doit-il être facile à deviner ?",
                       "Est-il sûr d'écrire son mot de passe sur un fichier sur son ordi ?"
                       ]
    
    reponse_facile = ["protéger l'accès", "oui", "non", "oui", "non", "oui", "il peut être piraté", "oui", "non", "non"]

    question_moyen = ["Qu'est-ce qu'une attaque par force brute ?",
                      "Qu'est-ce que le hachage d'un mot de passe ?",
                      "Pourquoi est-il important d'utiliser des mots de passe uniques ?",
                      "Qu'est-ce qu'un gestionnaire de mots de passe ?",
                      "Qu'est-ce que l'authentification à deux facteurs (2FA) ?",
                      "Pourquoi les mots de passe courts sont-ils moins sécurisés ?",
                      "Qu'est-ce qu'une attaque par dictionnaire ?",
                      "Pourquoi est-il risqué de réutiliser des mots de passe ?",
                      "Qu'est-ce qu'un mot de passe robuste ?",
                      "Comment fonctionne le salage des mots de passe ?"
                      ]
    
    reponse_moyen = ["essayer toutes les combinaisons", "transformer en code", "éviter le piratage", "stocker et gérer", "deux étapes de vérification", "plus de combinaisons possibles", "essayer des mots courants", "risque de piratage multiple", "long et complexe", "ajouter des données aléatoires"]
    
    question_difficile = ["Qu'est ce que le SHA-256",
                          "Quels sont les avantages des phrases de passe par rapport aux mots de passe traditionnels ?",
                          "Quelles sont les vulnérabilités des mots de passe basés sur des questions de sécurité ?",
                          "Quel est le hachage préféré pour le stockage sécurisé des mots de passe ?",
                          "P@ssW0rd! est-il un mot de passe sécurisé ?",
                          "Qu'est-ce qu'une attaque par phishing ciblée ?",
                          "Comment les attaques par keylogging compromettent-elles les mots de passe ?",
                          "Qu'est-ce que le PBKDF2 dans le contexte de la sécurité des mots de passe ?",
                          "Pourquoi les mots de passe basés sur des informations personnelles sont-ils risqués ?",
                          "Qu'est-ce que le rainbow table dans le contexte du piratage de mots de passe ?"
                          ]
    
    reponse_difficile = ["algorithme de hachage", "plus facile à retenir et plus long", "facilement devinables", "bcrypt", "non", "leurres pour voler des infos", "enregistrent les frappes clavier", "fonction de dérivation de clé", "facilement devinables", "table de hachage pré-calculée"]

    def facile():
        nonlocal score
        for i in range(10):
            print(f"\nQuestion {i+1} : {question_facile[i]}")
            reponse = input("Votre réponse : ").strip().lower()
            if reponse == reponse_facile[i]:
                print(f"{Fore.GREEN}Correct !{Style.RESET_ALL}")
                score += 1
            else:
                print(f"{Fore.RED}Incorrect. La bonne réponse est : {reponse_facile[i]}{Style.RESET_ALL}")
        print(f"\nVotre score final (Facile) : {score}/5")


    def moyen():
        nonlocal score
        for i in range(10):
            print(f"\nQuestion {i+1} : {question_moyen[i]}")
            reponse = input("Votre réponse : ").strip().lower()
            if reponse == reponse_moyen[i]:
                print(f"{Fore.GREEN}Correct !{Style.RESET_ALL}")
                score += 1
            else:
                print(f"{Fore.RED}Incorrect. La bonne réponse est : {reponse_moyen[i]}{Style.RESET_ALL}")
        print(f"\nVotre score final (Moyen) : {score}/5")

    
    def difficile():
        nonlocal score
        for i in range(10):
            print(f"\nQuestion {i+1} : {question_difficile[i]}")
            reponse = input("Votre réponse : ").strip().lower()
            if reponse == reponse_difficile[i]:
                print(f"{Fore.GREEN}Correct !{Style.RESET_ALL}")
                score += 1
            else:
                print(f"{Fore.RED}Incorrect. La bonne réponse est : {reponse_difficile[i]}{Style.RESET_ALL}")
        print(f"\nVotre score final (Difficile) : {score}/5")

    if level == '1':
        facile()
    elif level == '2':
        moyen()
    elif level == '3':
        difficile()

    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]    Quizz facile effectué. Score : {score}  \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )