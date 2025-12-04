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


class PasswordManager:
    
    def __init__(self):
        # Fichier où les données seront sauvegardées
        self.data_file = "passwords_data.json"
        # Fichier pour stocker le mot de passe maître (haché)
        self.master_file = "master_password.json"
        # Clé de chiffrement (sera générée à partir du mot de passe maître)
        self.cipher = None
        # Indicateur de connexion
        self.logged_in = False
        
    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setup_master_password(self, password):
        # Génère un sel aléatoire pour la dérivation de clé
        salt = os.urandom(16)
        # Hash le mot de passe maître pour vérification
        hashed = self.hash_password(password)
        
        # Sauvegarde les informations
        master_data = {
            'hash': hashed,
            'salt': base64.b64encode(salt).decode()
        }
        
        with open(self.master_file, 'w') as f:
            json.dump(master_data, f)
        
        # Configure le chiffrement
        key = self.derive_key(password, salt)
        self.cipher = Fernet(key)
        self.logged_in = True
        return True
    
    def verify_master_password(self, password):
        if not os.path.exists(self.master_file):
            return False
        
        with open(self.master_file, 'r') as f:
            master_data = json.load(f)
        
        hashed = self.hash_password(password)
        
        if hashed == master_data['hash']:
            # Configure le chiffrement
            salt = base64.b64decode(master_data['salt'])
            key = self.derive_key(password, salt)
            self.cipher = Fernet(key)
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
        except:
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
            except:
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
        """
        Ajoute un nouveau mot de passe
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_password = {
            'id': secrets.token_hex(8),
            'site': site,
            'username': username,
            'password': password,
            'notes': notes,
            'category': category,
            'created': now,
            'modified': now
        }
        passwords.append(new_password)
        self.save_passwords(passwords)
        return new_password
    
    def update_password(self, passwords, password_id, site, username, password, notes='', category='Autre'):
        """
        Met à jour un mot de passe existant
        """
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
        """
        Supprime un mot de passe
        """
        passwords[:] = [pwd for pwd in passwords if pwd['id'] != password_id]
        self.save_passwords(passwords)
    
    def generate_password(self, length=16, use_uppercase=True, use_lowercase=True, 
                         use_digits=True, use_symbols=True):
        """
        Génère un mot de passe aléatoire sécurisé
        """
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
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def check_password_strength(self, password):
        """
        Évalue la force d'un mot de passe
        Retourne un score de 0 à 100
        """
        score = 0
        
        # Longueur
        if len(password) >= 8:
            score += 20
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Diversité des caractères
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
    """
    Fonction principale qui crée l'interface utilisateur
    """
    page.title = "Gestionnaire de Mots de Passe Sécurisé"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1200
    page.window.height = 800
    page.padding = 0
    
    # Instance du gestionnaire
    manager = PasswordManager()
    
    # Liste des mots de passe chargés
    passwords_list = []
    
    # Catégories disponibles
    categories = ["Réseaux sociaux", "Email", "Banque", "Travail", "Personnel", "Autre"]
    
    # Variable pour suivre le mot de passe en cours d'édition
    editing_password_id = None
    
    def show_snackbar(message, color="green"):
        """
        Affiche un message temporaire à l'utilisateur
        """
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=color
        )
        page.snack_bar.open = True
        page.update()
    
    def setup_master_password_screen():
        """
        Écran pour créer le mot de passe maître (première utilisation)
        """
        password_input = ft.TextField(
            label="Créez votre mot de passe maître",
            password=True,
            can_reveal_password=True,
            width=400,
            hint_text="Au moins 8 caractères recommandés"
        )
        
        confirm_password_input = ft.TextField(
            label="Confirmez le mot de passe maître",
            password=True,
            can_reveal_password=True,
            width=400
        )
        
        strength_bar = ft.ProgressBar(width=400, value=0, color="red")
        strength_text = ft.Text("Force du mot de passe: Faible", color="red")
        
        def update_strength(e):
            """
            Met à jour l'indicateur de force du mot de passe
            """
            password = password_input.value
            if password:
                score = manager.check_password_strength(password)
                strength_bar.value = score / 100
                
                if score < 40:
                    strength_bar.color = "red"
                    strength_text.value = "Force du mot de passe: Faible"
                    strength_text.color = "red"
                elif score < 70:
                    strength_bar.color = "orange"
                    strength_text.value = "Force du mot de passe: Moyenne"
                    strength_text.color = "orange"
                else:
                    strength_bar.color = "green"
                    strength_text.value = "Force du mot de passe: Forte"
                    strength_text.color = "green"
            else:
                strength_bar.value = 0
                strength_text.value = "Force du mot de passe: Faible"
                strength_text.color = "red"
            
            page.update()
        
        password_input.on_change = update_strength
        
        def create_master_password(e):
            """
            Crée le mot de passe maître après vérification
            """
            if not password_input.value:
                show_snackbar("Veuillez entrer un mot de passe", "red")
                return
            
            if len(password_input.value) < 8:
                show_snackbar("Le mot de passe doit contenir au moins 8 caractères", "red")
                return
            
            if password_input.value != confirm_password_input.value:
                show_snackbar("Les mots de passe ne correspondent pas", "red")
                return
            
            manager.setup_master_password(password_input.value)
            show_snackbar("Mot de passe maître créé avec succès!", "green")
            show_main_screen()
        
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=50),
                        ft.Icon(ft.Icons.LOCK, size=80, color="blue"),
                        ft.Text(
                            "Bienvenue dans votre Gestionnaire de Mots de Passe",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Pour commencer, créez un mot de passe maître sécurisé",
                            size=16,
                            text_align=ft.TextAlign.CENTER,
                            color="grey"
                        ),
                        ft.Container(height=30),
                        password_input,
                        ft.Container(height=10),
                        strength_bar,
                        strength_text,
                        ft.Container(height=20),
                        confirm_password_input,
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "Créer mon coffre-fort",
                            icon=ft.Icons.CHECK,
                            on_click=create_master_password,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor="blue"
                            )
                        ),
                        ft.Container(
                            content=ft.Text(
                                "⚠️ Important: Ne perdez pas ce mot de passe!\n"
                                "Il est impossible de le récupérer.",
                                text_align=ft.TextAlign.CENTER,
                                color="red",
                                size=12
                            ),
                            padding=20
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    def login_screen():
        """
        Écran de connexion avec le mot de passe maître
        """
        password_input = ft.TextField(
            label="Mot de passe maître",
            password=True,
            can_reveal_password=True,
            width=400,
            autofocus=True
        )
        
        def do_login(e):
            """
            Vérifie le mot de passe maître et connecte l'utilisateur
            """
            if manager.verify_master_password(password_input.value):
                show_snackbar("Connexion réussie!", "green")
                show_main_screen()
            else:
                show_snackbar("Mot de passe incorrect", "red")
                password_input.value = ""
                password_input.focus()
                page.update()
        
        password_input.on_submit = do_login
        
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Container(height=50),
                        ft.Icon(ft.Icons.LOCK_OPEN, size=80, color="blue"),
                        ft.Text(
                            "Gestionnaire de Mots de Passe",
                            size=28,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "Entrez votre mot de passe maître pour déverrouiller",
                            size=14,
                            color="grey"
                        ),
                        ft.Container(height=30),
                        password_input,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Déverrouiller",
                            icon=ft.Icons.LOGIN,
                            on_click=do_login,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor="blue"
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        )
    
    def show_main_screen():
        """
        Écran principal avec la liste des mots de passe
        """
        nonlocal passwords_list
        passwords_list = manager.load_passwords()
        
        # Champ de recherche
        search_field = ft.TextField(
            hint_text="Rechercher un site, nom d'utilisateur...",
            prefix_icon=ft.Icons.SEARCH,
            width=400,
            on_change=lambda e: filter_passwords()
        )
        
        # Filtre par catégorie
        category_filter = ft.Dropdown(
            label="Catégorie",
            options=[ft.dropdown.Option("Toutes")] + [ft.dropdown.Option(cat) for cat in categories],
            value="Toutes",
            width=200,
            on_change=lambda e: filter_passwords()
        )
        
        # Conteneur pour la liste des mots de passe
        passwords_container = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        def filter_passwords():
            """
            Filtre la liste des mots de passe selon la recherche et la catégorie
            """
            search_term = search_field.value.lower() if search_field.value else ""
            selected_category = category_filter.value
            
            filtered = [
                pwd for pwd in passwords_list
                if (search_term in pwd['site'].lower() or search_term in pwd['username'].lower())
                and (selected_category == "Toutes" or pwd['category'] == selected_category)
            ]
            
            display_passwords(filtered)
        
        def display_passwords(passwords_to_show):
            """
            Affiche la liste des mots de passe
            """
            passwords_container.controls.clear()
            
            if not passwords_to_show:
                passwords_container.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.LOCK_OPEN, size=60, color="grey"),
                                ft.Text(
                                    "Aucun mot de passe enregistré",
                                    size=18,
                                    color="grey"
                                ),
                                ft.Text(
                                    "Cliquez sur '+ Nouveau' pour ajouter votre premier mot de passe",
                                    size=14,
                                    color="grey"
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=50,
                        alignment=ft.alignment.center
                    )
                )
            else:
                for pwd in passwords_to_show:
                    passwords_container.controls.append(create_password_card(pwd))
            
            page.update()
        
        def create_password_card(pwd):
            """
            Crée une carte pour afficher un mot de passe
            """
            password_hidden = ft.Text("••••••••", size=14)
            password_visible = ft.Text(pwd['password'], size=14, visible=False)
            
            def toggle_password_visibility(e):
                """
                Affiche ou masque le mot de passe
                """
                password_hidden.visible = not password_hidden.visible
                password_visible.visible = not password_visible.visible
                eye_button.icon = ft.Icons.VISIBILITY_OFF if password_visible.visible else ft.Icons.VISIBILITY
                page.update()
            
            def copy_password(e):
                """
                Copie le mot de passe dans le presse-papiers
                """
                try:
                    pyperclip.copy(pwd['password'])
                    show_snackbar("Mot de passe copié!", "green")
                except:
                    show_snackbar("Erreur lors de la copie", "red")
            
            def edit_password(e):
                """
                Ouvre le formulaire d'édition
                """
                show_password_form(pwd)
            
            def delete_password_confirm(e):
                """
                Demande confirmation avant de supprimer
                """
                def confirm_delete(e):
                    manager.delete_password(passwords_list, pwd['id'])
                    show_snackbar("Mot de passe supprimé", "orange")
                    dialog.open = False
                    filter_passwords()
                    page.update()
                
                def cancel_delete(e):
                    dialog.open = False
                    page.update()
                
                dialog = ft.AlertDialog(
                    title=ft.Text("Confirmer la suppression"),
                    content=ft.Text(f"Êtes-vous sûr de vouloir supprimer le mot de passe pour {pwd['site']}?"),
                    actions=[
                        ft.TextButton("Annuler", on_click=cancel_delete),
                        ft.TextButton("Supprimer", on_click=confirm_delete, style=ft.ButtonStyle(color="red"))
                    ]
                )
                
                page.overlay.append(dialog)
                dialog.open = True
                page.update()
            
            eye_button = ft.IconButton(
                icon=ft.Icons.VISIBILITY,
                on_click=toggle_password_visibility,
                tooltip="Afficher/Masquer"
            )
            
            # Carte de mot de passe
            return ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.LANGUAGE if pwd['category'] in ["Réseaux sociaux", "Email"] 
                                    else ft.Icons.ACCOUNT_BALANCE if pwd['category'] == "Banque"
                                    else ft.Icons.WORK if pwd['category'] == "Travail"
                                    else ft.Icons.PERSON,
                                    size=40,
                                    color="blue"
                                ),
                                padding=10
                            ),
                            ft.Column(
                                [
                                    ft.Text(pwd['site'], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"Identifiant: {pwd['username']}", size=12, color="grey"),
                                    ft.Row([
                                        ft.Text("Mot de passe: ", size=12, color="grey"),
                                        password_hidden,
                                        password_visible
                                    ]),
                                    ft.Container(
                                        content=ft.Text(pwd['category'], size=10, color="white"),
                                        bgcolor="blue",
                                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                        border_radius=10
                                    ) if pwd['category'] != "Autre" else ft.Container()
                                ],
                                spacing=2,
                                expand=True
                            ),
                            ft.Row(
                                [
                                    eye_button,
                                    ft.IconButton(
                                        icon=ft.Icons.COPY,
                                        on_click=copy_password,
                                        tooltip="Copier"
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        on_click=edit_password,
                                        tooltip="Modifier"
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        on_click=delete_password_confirm,
                                        tooltip="Supprimer",
                                        icon_color="red"
                                    )
                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=15
                ),
                elevation=2
            )
        
        def show_password_form(password_data=None):
            """
            Affiche le formulaire pour ajouter ou modifier un mot de passe
            """
            nonlocal editing_password_id
            editing_password_id = password_data['id'] if password_data else None
            
            is_editing = password_data is not None
            
            # Champs du formulaire
            site_field = ft.TextField(
                label="Site ou application",
                value=password_data['site'] if is_editing else "",
                width=500,
                hint_text="Ex: Facebook, Gmail, Amazon..."
            )
            
            username_field = ft.TextField(
                label="Nom d'utilisateur ou email",
                value=password_data['username'] if is_editing else "",
                width=500,
                hint_text="Ex: john.doe@email.com"
            )
            
            password_field = ft.TextField(
                label="Mot de passe",
                value=password_data['password'] if is_editing else "",
                password=True,
                can_reveal_password=True,
                width=500
            )
            
            notes_field = ft.TextField(
                label="Notes (optionnel)",
                value=password_data.get('notes', '') if is_editing else "",
                multiline=True,
                min_lines=3,
                max_lines=5,
                width=500,
                hint_text="Informations supplémentaires..."
            )
            
            category_dropdown = ft.Dropdown(
                label="Catégorie",
                options=[ft.dropdown.Option(cat) for cat in categories],
                value=password_data['category'] if is_editing else "Autre",
                width=500
            )
            
            # Générateur de mot de passe
            length_slider = ft.Slider(
                min=8,
                max=32,
                value=16,
                divisions=24,
                label="{value} caractères"
            )
            
            uppercase_check = ft.Checkbox(label="Majuscules (A-Z)", value=True)
            lowercase_check = ft.Checkbox(label="Minuscules (a-z)", value=True)
            digits_check = ft.Checkbox(label="Chiffres (0-9)", value=True)
            symbols_check = ft.Checkbox(label="Symboles (!@#$...)", value=True)
            
            generated_password_text = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
            
            strength_bar = ft.ProgressBar(width=500, value=0, color="red")
            strength_text = ft.Text("Force: Faible", color="red")
            
            def update_strength(e=None):
                """
                Met à jour l'indicateur de force
                """
                password = password_field.value
                if password:
                    score = manager.check_password_strength(password)
                    strength_bar.value = score / 100
                    
                    if score < 40:
                        strength_bar.color = "red"
                        strength_text.value = "Force: Faible"
                        strength_text.color = "red"
                    elif score < 70:
                        strength_bar.color = "orange"
                        strength_text.value = "Force: Moyenne"
                        strength_text.color = "orange"
                    else:
                        strength_bar.color = "green"
                        strength_text.value = "Force: Forte"
                        strength_text.color = "green"
                else:
                    strength_bar.value = 0
                    strength_text.value = "Force: Faible"
                    strength_text.color = "red"
                
                page.update()
            
            password_field.on_change = update_strength
            
            def generate_new_password(e):
                """
                Génère un nouveau mot de passe aléatoire
                """
                new_password = manager.generate_password(
                    length=int(length_slider.value),
                    use_uppercase=uppercase_check.value,
                    use_lowercase=lowercase_check.value,
                    use_digits=digits_check.value,
                    use_symbols=symbols_check.value
                )
                password_field.value = new_password
                generated_password_text.value = f"Généré: {new_password}"
                update_strength()
                page.update()
            
            def save_password(e):
                """
                Sauvegarde le mot de passe (ajout ou modification)
                """
                nonlocal passwords_list
                
                if not site_field.value or not username_field.value or not password_field.value:
                    show_snackbar("Veuillez remplir tous les champs obligatoires", "red")
                    return
                
                if is_editing:
                    manager.update_password(
                        passwords_list,
                        editing_password_id,
                        site_field.value,
                        username_field.value,
                        password_field.value,
                        notes_field.value,
                        category_dropdown.value
                    )
                    show_snackbar("Mot de passe modifié avec succès!", "green")
                else:
                    manager.add_password(
                        passwords_list,
                        site_field.value,
                        username_field.value,
                        password_field.value,
                        notes_field.value,
                        category_dropdown.value
                    )
                    show_snackbar("Mot de passe ajouté avec succès!", "green")
                
                passwords_list = manager.load_passwords()
                filter_passwords()
                close_form()
            
            def close_form(e=None):
                """
                Ferme le formulaire
                """
                form_dialog.open = False
                page.update()
            
            # Dialogue du formulaire
            form_dialog = ft.AlertDialog(
                title=ft.Text("Modifier le mot de passe" if is_editing else "Nouveau mot de passe"),
                content=ft.Container(
                    content=ft.Column(
                        [
                            site_field,
                            username_field,
                            password_field,
                            strength_bar,
                            strength_text,
                            ft.Divider(),
                            ft.Text("Générateur de mot de passe", weight=ft.FontWeight.BOLD),
                            ft.Row([ft.Text("Longueur:"), length_slider], alignment=ft.MainAxisAlignment.START),
                            ft.Row([uppercase_check, lowercase_check]),
                            ft.Row([digits_check, symbols_check]                            ),
                            ft.ElevatedButton(
                                "Générer un mot de passe",
                                icon=ft.Icons.REFRESH,
                                on_click=generate_new_password
                            ),
                            generated_password_text,
                            ft.Divider(),
                            notes_field,
                            category_dropdown
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        width=600,
                        height=600
                    )
                ),
                actions=[
                    ft.TextButton("Annuler", on_click=close_form),
                    ft.ElevatedButton(
                        "Enregistrer",
                        icon=ft.Icons.SAVE,
                        on_click=save_password,
                        style=ft.ButtonStyle(color="white", bgcolor="blue")
                    )
                ]
            )
            
            update_strength()
            page.overlay.append(form_dialog)
            form_dialog.open = True
            page.update()
        
        # Interface principale
        page.clean()
        page.add(
            ft.Container(
                content=ft.Column(
                    [
                        # En-tête
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOCK, size=30, color="white"),
                                    ft.Text(
                                        "Gestionnaire de Mots de Passe",
                                        size=24,
                                        weight=ft.FontWeight.BOLD,
                                        color="white"
                                    ),
                                    ft.Container(expand=True),
                                    ft.Text(
                                        f"Total: {len(passwords_list)} mots de passe",
                                        color="white",
                                        size=14
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            bgcolor="blue",
                            padding=20
                        ),
                        
                        # Barre d'outils
                        ft.Container(
                            content=ft.Row(
                                [
                                    search_field,
                                    category_filter,
                                    ft.Container(expand=True),
                                    ft.ElevatedButton(
                                        "Nouveau",
                                        icon=ft.Icons.ADD,
                                        on_click=lambda e: show_password_form(),
                                        style=ft.ButtonStyle(
                                            color="white",
                                            bgcolor="green"
                                        )
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            padding=20
                        ),
                        
                        # Liste des mots de passe
                        ft.Container(
                            content=passwords_container,
                            padding=20,
                            expand=True
                        )
                    ]
                ),
                expand=True
            )
        )
        
        display_passwords(passwords_list)
    
    # Démarrage de l'application
    if not os.path.exists(manager.master_file):
        # Première utilisation - créer le mot de passe maître
        setup_master_password_screen()
    else:
        # Écran de connexion
        login_screen()


# Point d'entrée de l'application
if __name__ == "__main__":
    ft.app(target=main)
