from colorama import Fore, Style
import time


def quizz_mdp(langue_actuelle):
    score = 0

    question_FR = {
        "1": (
            ["À quoi sert un mot de passe ?",
             "Faut-il garder son mot de passe secret ?",
             "Est-ce une bonne idée de dire ton mot de passe à un ami ?",
             "Un mot de passe doit-il être long et complexe ?",
             "Est-il sûr d'utiliser le même mot de passe pour plusieurs comptes ?",
             "Un mot de passe doit-il contenir des chiffres et des symboles ?",
             "Si ton mot de passe est trop simple, que peut-il arriver ?",
             "Est-il important de changer régulièrement son mot de passe ?",
             "Un mot de passe doit-il être facile à deviner ?",
             "Est-il sûr d'écrire son mot de passe sur un fichier sur son ordi ?"
             ],
            ["protéger l'accès", "oui", "non", "oui", "non", "oui", "il peut être piraté", "oui", "non", "non"]
        ),
        "2": (
            ["Qu'est-ce qu'une attaque par force brute ?",
             "Qu'est-ce que le hachage d'un mot de passe ?",
             "Pourquoi est-il important d'utiliser des mots de passe uniques ?",
             "Qu'est-ce qu'un gestionnaire de mots de passe ?",
             "Qu'est-ce que l'authentification à deux facteurs (2FA) ?",
             "Pourquoi les mots de passe courts sont-ils moins sécurisés ?",
             "Qu'est-ce qu'une attaque par dictionnaire ?",
             "Pourquoi est-il risqué de réutiliser des mots de passe ?",
             "Qu'est-ce qu'un mot de passe robuste ?",
             "Comment fonctionne le salage des mots de passe ?"
             ],
            ["essayer toutes les combinaisons", "transformer en code", "éviter le piratage", "stocker et gérer", "deux étapes de vérification", "plus de combinaisons possibles", "essayer des mots courants", "risque de piratages multiples", "long et complexe", "ajouter des données aléatoires"]
        ),
        "3": (
            ["Qu'est ce que le SHA-256 ?",
             "Quels sont les avantages des phrases de passe par rapport aux mots de passe traditionnels ?",
             "Quelles sont les vulnérabilités des mots de passe basés sur des questions de sécurité ?",
             "Quel est le hachage préféré pour le stockage sécurisé des mots de passe ?",
             "P@ssW0rd! est-il un mot de passe sécurisé ?",
             "Qu'est-ce qu'une attaque par phishing ciblée ?",
             "Comment les attaques par keylogging compromettent-elles les mots de passe ?",
             "Qu'est-ce que le PBKDF2 dans le contexte de la sécurité des mots de passe ?",
             "Pourquoi les mots de passe basés sur des informations personnelles sont-ils risqués ?",
             "Qu'est-ce que le rainbow table dans le contexte du piratage de mots de passe ?"
             ],
            ["algorithme de hachage", "plus facile à retenir et plus long", "facilement devinables", "bcrypt", "non", "leurres pour voler des infos", "enregistrent les frappes clavier", "fonction de dérivation de clé", "facilement devinables", "table de hachage pré-calculée"]
        )
    }

    question_EN = {
        "1": (
            ["What is the purpose of a password?",
             "Should you keep your password secret?",
             "Is it a good idea to tell your password to a friend?",
             "Should a password be long and complex?",
             "Is it safe to use the same password for multiple accounts?",
             "Should a password contain numbers and symbols?",
             "What can happen if your password is too simple?",
             "Is it important to change your password regularly?",
             "Should a password be easy to guess?",
             "Is it safe to write your password in a file on your computer?"
             ],
            ["protect access", "yes", "no", "yes", "no", "yes", "it can be hacked", "yes", "no", "no"]
        ),
        "2": (
            ["What is a brute force attack?",
             "What is password hashing?",
             "Why is it important to use unique passwords?",
             "What is a password manager?",
             "What is two-factor authentication (2FA)?",
             "Why are short passwords less secure?",
             "What is a dictionary attack?",
             "Why is reusing passwords risky?",
             "What is a strong password?",
             "How does password salting work?"
             ],            
            ["trying all combinations", "transforming into code", "prevent hacking", "store and manage", "two verification steps", "more possible combinations", "trying common words", "risk of multiple hacks", "long and complex", "adding random data"]
        ),
        "3": (
            ["What is SHA-256?",
             "What are the advantages of passphrases over traditional passwords?",
             "What are the vulnerabilities of security question-based passwords?",
             "What is the preferred hashing for secure password storage?",
             "Is P@ssW0rd! a secure password?",
             "What is a targeted phishing attack?",
             "How do keylogging attacks compromise passwords?",
             "What is PBKDF2 in the context of password security?",
             "Why are passwords based on personal information risky?",
             "What is a rainbow table in the context of password hacking?"
             ],
            ["hashing algorithm", "easier to remember and longer", "easily guessable", "bcrypt", "no", "deceits to steal info", "record keystrokes", "key derivation function", "easily guessable", "pre-computed hash table"]
        )
    }

    if langue_actuelle == "FR":
        question_facile, reponse_facile = question_FR["1"]
        question_moyen, reponse_moyen = question_FR["2"]
        question_difficile, reponse_difficile = question_FR["3"]
    else:
        question_facile, reponse_facile = question_EN["1"]
        question_moyen, reponse_moyen = question_EN["2"]
        question_difficile, reponse_difficile = question_EN["3"]

    def facile():
        nonlocal score
        score = 0
        for i in range(10):
            if langue_actuelle == "FR":
                print(f"\nQuestion {i+1} : {question_facile[i]}")
                reponse = input("Votre réponse : ").strip().lower()
            else:
                print(f"\nQuestion {i+1}: {question_facile[i]}")
                reponse = input("Your answer: ").strip().lower()
                
            if reponse == reponse_facile[i].lower():
                print(f"{Fore.GREEN}Correct !{Style.RESET_ALL}" if langue_actuelle == "FR" else f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                score += 1
            else:
                if langue_actuelle == "FR":
                    print(f"{Fore.RED}Incorrect. La bonne réponse est : {reponse_facile[i]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Incorrect. The correct answer is: {reponse_facile[i]}{Style.RESET_ALL}")
                    
        if langue_actuelle == "FR":
            print(f"\nVotre score final (Facile) : {score}/10")
        else:
            print(f"\nYour final score (Easy): {score}/10")

    def moyen():
        nonlocal score
        score = 0
        for i in range(10):
            if langue_actuelle == "FR":
                print(f"\nQuestion {i+1} : {question_moyen[i]}")
                reponse = input("Votre réponse : ").strip().lower()
            else:
                print(f"\nQuestion {i+1}: {question_moyen[i]}")
                reponse = input("Your answer: ").strip().lower()
                
            if reponse == reponse_moyen[i].lower():
                print(f"{Fore.GREEN}Correct !{Style.RESET_ALL}" if langue_actuelle == "FR" else f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                score += 1
            else:
                if langue_actuelle == "FR":
                    print(f"{Fore.RED}Incorrect. La bonne réponse est : {reponse_moyen[i]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Incorrect. The correct answer is: {reponse_moyen[i]}{Style.RESET_ALL}")
                    
        if langue_actuelle == "FR":
            print(f"\nVotre score final (Moyen) : {score}/10")
        else:
            print(f"\nYour final score (Medium): {score}/10")

    def difficile():
        nonlocal score
        score = 0
        for i in range(10):
            if langue_actuelle == "FR":
                print(f"\nQuestion {i+1} : {question_difficile[i]}")
                reponse = input("Votre réponse : ").strip().lower()
            else:
                print(f"\nQuestion {i+1}: {question_difficile[i]}")
                reponse = input("Your answer: ").strip().lower()
                
            if reponse == reponse_difficile[i].lower():
                print(f"{Fore.GREEN}Correct !{Style.RESET_ALL}" if langue_actuelle == "FR" else f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                score += 1
            else:
                if langue_actuelle == "FR":
                    print(f"{Fore.RED}Incorrect. La bonne réponse est : {reponse_difficile[i]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}Incorrect. The correct answer is: {reponse_difficile[i]}{Style.RESET_ALL}")
                    
        if langue_actuelle == "FR":
            print(f"\nVotre score final (Difficile) : {score}/10")
        else:
            print(f"\nYour final score (Hard): {score}/10")

    def fr():
        print(f"""
         {Fore.MAGENTA}Quiz sur les mots de passe{Style.RESET_ALL}
        """)

        level = input("Choisissez le niveau de difficulté (1 - Facile, 2 - Moyen, 3 - Difficile) : ")

        if level not in ['1', '2', '3']:
            print(f"{Fore.RED}Erreur : Niveau invalide. Veuillez choisir 1, 2 ou 3.{Style.RESET_ALL}")
            return
        
        if level == '1':
            facile()
        elif level == '2':
            moyen()
        elif level == '3':
            difficile()
        
    def en():
        print(f"""
         {Fore.MAGENTA}Password Quiz{Style.RESET_ALL}
        """)

        level = input("Choose difficulty level (1 - Easy, 2 - Medium, 3 - Hard): ")

        if level not in ['1', '2', '3']:
            print(f"{Fore.RED}Error: Invalid level. Please choose 1, 2, or 3.{Style.RESET_ALL}")
            return
            
        if level == '1':
            facile()
        elif level == '2':
            moyen()
        elif level == '3':
            difficile()

    if langue_actuelle == "FR":
        fr()
    else:
        en()

    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]    Quiz effectué. Score : {score}/10  \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )