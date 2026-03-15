import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def dirbuster():
    print(r"""
                        zfiuohhhvheovhmzqohvzovhzv
    """)

    domain = input("Entrez le domaine cible (ex: example.com): ").strip()
    domain = domain.replace("http://", "").replace("https://", "").strip("/")

    wordlist_choice = input("Voulez-vous utiliser une wordlist personnalisée ? (oui/non) : ").strip().lower()

    paths = [
        # Admin / Backoffice
        "admin", "admin/login", "administrator", "backend", "console",
        "manage", "dashboard", "panel", "cpanel", "root", "superadmin",

        # Dev / Internal
        "dev", "devtools", "debug", "debugger", "beta", "staging",
        "internal", "intranet", "hidden", "private", "secret",
        "config", "settings", "environment",

        # API
        "api", "v1", "v2", "api/internal", "api/private", "graphql",
        "swagger", "openapi", "health", "healthcheck",

        # Auth
        "auth", "login", "signin", "logout", "signup", "register",
        "session", "token", "oauth", "sso", "user", "users",

        # Fichiers / stockage
        "uploads", "upload", "files", "media", "assets", "static",
        "backup", "backups", "archives", "old", "logs", "tmp",

        # Monitoring / DevOps
        "monitor", "monitoring", "status", "metrics", "grafana",
        "prometheus", "kibana", "elastic", "jenkins", "ci", "cd",

        # Commerce
        "payment", "payments", "billing", "checkout", "orders",
        "customers", "account", "profile",

        # CMS populaires
        "wp-admin", "wp-login.php", "wp-content",
        "drupal", "joomla", "umbraco",

        # Documentation / outils
        "docs", "documentation", "api-docs", "developer",
        "changelog", "release", "version"
    ]

    if wordlist_choice == "oui":
        wordlist_path = input("Entrez le chemin de votre wordlist (ex: C:\\wordlist.txt) : ").strip()
        try:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                custom_paths = [line.strip().lstrip("/") for line in f if line.strip()]
                paths.extend(custom_paths)
        except FileNotFoundError:
            print("Wordlist introuvable.")
            input("\nAppuyez sur Entrée pour revenir au menu.")
            return
        except Exception as e:
            print(f"Erreur lors de la lecture de la wordlist : {e}")
            input("\nAppuyez sur Entrée pour revenir au menu.")
            return

    found = 0
    tested = 0

    for path in paths:
        tested += 1
        path = path.lstrip("/")

        https_url = f"https://{domain}/{path}"
        http_url = f"http://{domain}/{path}"

        ok = False

        # Test HTTPS
        try:
            response_https = requests.get(https_url, timeout=5, verify=False, allow_redirects=True)
            print(f"[HTTPS] {https_url} -> code {response_https.status_code}")
            if response_https.status_code < 400:
                found += 1
                ok = True
        except requests.RequestException as e:
            print(f"[HTTPS] Erreur pour {https_url} : {e}")

        # Si HTTPS échoue ou renvoie un mauvais statut, on teste HTTP
        if not ok:
            try:
                response_http = requests.get(http_url, timeout=5, allow_redirects=True)
                print(f"[HTTP] {http_url} -> code {response_http.status_code}")
                if response_http.status_code < 400:
                    found += 1
            except requests.RequestException as e:
                print(f"[HTTP] Erreur pour {http_url} : {e}")

        print("-" * 60)

    print(f"\nNombre total de chemins trouvés : {found}")
    print(f"Nombre total de chemins testés : {tested}")

    input("\nAppuyez sur Entrée pour revenir au menu.")