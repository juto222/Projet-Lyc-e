import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def dirbuster():
    print(r"""
    ____  _       ____               __           
   / __ \(_)___  / __ )__  _______  / /____  _____
  / / / / / __ \/ __  / / / / ___/ / __/ _ \/ ___/
 / /_/ / / / / / /_/ / /_/ (__  ) / /_/  __/ /    
/_____/_/_/ /_/_____/\__,_/____/  \__/\___/_/     
    """)

    domain = input("Entrez le domaine cible (ex: example.com): ").strip()
    domain = domain.replace("http://", "").replace("https://", "").strip("/")

    # ------------------------------------------------------------------ #
    # Wordlist                                                             #
    # ------------------------------------------------------------------ #
    wordlist_choice = input("Wordlist personnalisée ? (oui/non) : ").strip().lower()

    if wordlist_choice == "oui":
        wordlist_path = input("Chemin de la wordlist : ").strip()

        contenu = None
        for encodage in ("utf-8", "latin-1", "cp1252"):
            try:
                with open(wordlist_path, "r", encoding=encodage) as f:
                    contenu = f.read()
                print(f"[+] Wordlist chargée ({encodage}).")
                break
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                print("[!] Fichier introuvable.")
                input("\nAppuyez sur Entrée pour revenir au menu.")
                return
            except Exception as e:
                print(f"[!] Erreur lecture : {e}")
                input("\nAppuyez sur Entrée pour revenir au menu.")
                return

        if contenu is None:
            print("[!] Impossible de lire le fichier.")
            input("\nAppuyez sur Entrée pour revenir au menu.")
            return

        # La wordlist REMPLACE les chemins par défaut
        paths = [
            ligne.strip().lstrip("/")
            for ligne in contenu.splitlines()
            if ligne.strip() and not ligne.startswith("#")
        ]
        print(f"[+] {len(paths)} chemins chargés.")

    else:
        paths = [
            "admin", "admin/login", "administrator", "backend", "console",
            "manage", "dashboard", "panel", "cpanel", "root", "superadmin",
            "dev", "devtools", "debug", "beta", "staging",
            "internal", "intranet", "hidden", "private", "secret",
            "config", "settings", "environment",
            "api", "v1", "v2", "graphql", "swagger", "openapi",
            "health", "healthcheck",
            "auth", "login", "signin", "logout", "signup", "register",
            "session", "token", "oauth", "sso", "user", "users",
            "uploads", "upload", "files", "media", "assets", "static",
            "backup", "backups", "archives", "old", "logs", "tmp",
            "monitor", "monitoring", "status", "metrics",
            "payment", "payments", "billing", "checkout", "orders",
            "customers", "account", "profile",
            "wp-admin", "wp-login.php", "wp-content",
            "docs", "documentation", "api-docs",
            "changelog", "release", "version",
        ]

    # ------------------------------------------------------------------ #
    # Threads                                                              #
    # ------------------------------------------------------------------ #
    try:
        nb_threads = int(input("Nombre de threads (défaut 20) : ") or 20)
        nb_threads = max(1, min(nb_threads, 100))
    except ValueError:
        nb_threads = 20

    print(f"\n[*] {domain} | {len(paths)} chemins | {nb_threads} threads\n")
    print("-" * 60)

    found_urls = []
    lock = threading.Lock()

    # ------------------------------------------------------------------ #
    # Fonction qui teste UN chemin                                         #
    # ------------------------------------------------------------------ #
    def tester(chemin):
        chemin = chemin.lstrip("/")
        https_url = f"https://{domain}/{chemin}"
        http_url  = f"http://{domain}/{chemin}"

        # HTTPS d'abord
        try:
            r = requests.get(https_url, timeout=3, verify=False,
                             allow_redirects=False)
            with lock:
                if r.status_code < 400:
                    print(f"  [{r.status_code}] {https_url}")
                    found_urls.append((https_url, r.status_code))
            return
        except requests.RequestException:
            pass

        # HTTP si HTTPS échoue
        try:
            r = requests.get(http_url, timeout=3, allow_redirects=False)
            with lock:
                if r.status_code < 400:
                    print(f"  [{r.status_code}] {http_url}")
                    found_urls.append((http_url, r.status_code))
        except requests.RequestException:
            pass

    # ------------------------------------------------------------------ #
    # Lancement                                                            #
    # ------------------------------------------------------------------ #
    with ThreadPoolExecutor(max_workers=nb_threads) as executor:
        futures = [executor.submit(tester, p) for p in paths]
        for future in as_completed(futures):
            future.result()

    # ------------------------------------------------------------------ #
    # Résultats                                                            #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print(f"Testés  : {len(paths)}")
    print(f"Trouvés : {len(found_urls)}\n")

    if found_urls:
        print("URLs accessibles :")
        for url, code in sorted(found_urls):
            print(f"  [{code}] {url}")

    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Analyse dirbuster de {domain} \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )

    input("\nAppuyez sur Entrée pour revenir au menu.")

