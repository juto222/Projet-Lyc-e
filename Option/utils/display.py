import time
import getpass
from colorama import Fore, Style, init

init(autoreset=True)

# ──────────────────────────────────────────
#  TIMESTAMP
# ──────────────────────────────────────────

def ts():
    t = time.strftime('%H:%M:%S')
    return f"{Fore.GREEN}[{Style.RESET_ALL}{t}{Fore.GREEN}]{Style.RESET_ALL}"


# ──────────────────────────────────────────
#  PRINT
# ──────────────────────────────────────────

def info(message):
    """Message normal.  [18:06:24] texte"""
    print(f"{ts()} {message}")

def success(message):
    """Succès en vert.  [18:06:24] [+] texte"""
    print(f"{ts()} {Fore.GREEN}[+] {message}{Style.RESET_ALL}")

def error(message):
    """Erreur en rouge.  [18:06:24] [!] texte"""
    print(f"{ts()} {Fore.RED}[!] {message}{Style.RESET_ALL}")

def warning(message):
    """Avertissement jaune.  [18:06:24] [~] texte"""
    print(f"{ts()} {Fore.YELLOW}[~] {message}{Style.RESET_ALL}")

def found(message):
    """Élément trouvé vert vif.  [18:06:24] [✓] texte"""
    print(f"{ts()} {Fore.GREEN}[✓] {message}{Style.RESET_ALL}")

def result(label, valeur):
    """Résultat clé/valeur.  [18:06:24] Label : valeur"""
    print(f"{ts()} {Fore.YELLOW}{label}{Style.RESET_ALL} : {Fore.WHITE}{valeur}{Style.RESET_ALL}")

def separator():
    """Ligne de séparation."""
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")


# ──────────────────────────────────────────
#  INPUT
# ──────────────────────────────────────────

def ask(label):
    """Input formaté.  [18:12:02] [>] | Label -> """
    prefix = (
        f"{ts()} "
        f"{Fore.GREEN}[>]{Style.RESET_ALL} | "
        f"{Fore.YELLOW}{label}{Style.RESET_ALL} "
        f"{Fore.GREEN}->{Style.RESET_ALL} "
    )
    return input(prefix)

def ask_secret(label):
    """Input masqué (mot de passe).  [18:12:02] [>] | Label -> """
    prefix = (
        f"{ts()} "
        f"{Fore.GREEN}[>]{Style.RESET_ALL} | "
        f"{Fore.YELLOW}{label}{Style.RESET_ALL} "
        f"{Fore.GREEN}->{Style.RESET_ALL} "
    )
    return getpass.getpass(prompt=prefix)

def ask_confirm(label):
    """Confirmation oui/non. Retourne True si oui."""
    rep = ask(f"{label} (oui/non)").strip().lower()
    return rep in ("oui", "o", "yes", "y")

def pause():
    """Pause 'Appuyez sur Entrée'."""
    ask("Appuyez sur Entrée pour continuer")


# ──────────────────────────────────────────
#  LOG FICHIER
# ──────────────────────────────────────────

def log(message):
    """Écrit dans logs.txt + affiche en info."""
    info(message)
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"------------------------------------\n")
        f.write(f"\n")
        f.write(f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] {message}\n")
        f.write(f"\n")
        f.write(f"------------------------------------\n")