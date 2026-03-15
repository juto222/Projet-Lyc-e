from colorama import Fore, Style
import time

def quizzsecurity(level):
    print(f"""

        {Fore.MAGENTA} Quiz sur la sécurité informatique
    """)
    score = 0
    if level == '1':
        questions = [
            ("Que signifie l'acronyme 'VPN' ?", "Réseau Privé Virtuel"),
            ("Qu'est-ce qu'un pare-feu ?", "Un système de sécurité réseau"),
            ("Que signifie 'HTTPS' dans une URL ?", "HyperText Transfer Protocol Secure"),
            ("Qu'est-ce qu'un logiciel malveillant ?", "Un programme nuisible"),
            ("Que signifie '2FA' ?", "Authentification à deux facteurs")
        ]
    elif level == '2':
        questions = [
            ("Qu'est-ce qu'une attaque par phishing ?", "Une tentative de fraude en ligne"),
            ("Que signifie 'SSL' ?", "Secure Sockets Layer"),
            ("Qu'est-ce qu'un ransomware ?", "Un logiciel qui demande une rançon"),
            ("Que signifie 'DDoS' ?", "Attaque par déni de service distribué"),
            ("Qu'est-ce qu'un VPN et pourquoi l'utiliser ?", "Un réseau privé virtuel pour sécuriser la connexion")
        ]
    else:
        questions = [
            ("Qu'est-ce qu'une attaque par l'homme du milieu (MITM) ?", "Une interception de communication"),
            ("Que signifie 'XSS' ?", "Cross-Site Scripting"),
            ("Qu'est-ce qu'une vulnérabilité zero-day ?", "Une faille de sécurité inconnue"),
            ("Que signifie 'PKI' ?", "Infrastructure à clés publiques"),
            ("Qu'est-ce qu'un honeypot en cybersécurité ?", "Un leurre pour attirer les attaquants")
        ]
    for question, correct_answer in questions:
        reponse = input(f"{question} ")
        if reponse.strip().lower() == correct_answer.strip().lower():
            score += 1
            print(f"{Fore.GREEN}Bonne réponse !{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Mauvaise réponse. La bonne réponse est : {correct_answer}{Style.RESET_ALL}\n")
    print(f"Votre score final : {score}/{len(questions)}")
    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Quiz sécurité niveau {level} : Score {score}/{len(questions)}\n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )
        