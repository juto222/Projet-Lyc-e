from colorama import Fore, Style
import time

def quizznetwork():
    print(f"""

    {Fore.CYAN}
══════════════════════════════════════════════════════════════════════
        ascii art quizz network ici
══════════════════════════════════════════════════════════════════════
    {Fore.MAGENTA} Quiz sur les réseaux informatiques
    """)
    score = 0
    questions = [
        ("Quel protocole est utilisé pour envoyer des e-mails ?", "SMTP"),
        ("Que signifie l'acronyme 'IP' ?", "Internet Protocol"),
        ("Quel port est utilisé par défaut pour le protocole HTTP ?", "80"),
        ("Qu'est-ce qu'une adresse MAC ?", "Une adresse physique unique pour un appareil réseau"),
        ("Que signifie 'DNS' ?", "Domain Name System")  
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
            f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Quiz réseau : Score {score}/{len(questions)}\n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )