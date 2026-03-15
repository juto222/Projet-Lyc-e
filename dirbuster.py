import dns.resolver
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dirbuster():
    print(r"""
                        zfiuohhhvheovhmzqohvzovhzv
    """)
    domain = input("Entrez le domaine cible (ex: example.com): ").strip()

    subdomains = [
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


    for sub in subdomains:
        full_domain = f"{domain}/{sub}"

        found = 0

        # Vérification DNS
        try:
            dns.resolver.resolve(full_domain)
            print(f"[DNS] Le sous-domaine {full_domain} existe.\n")
            found =+ 1
        except dns.resolver.NXDOMAIN:
            print(f"[DNS] Le sous-domaine {full_domain} n'existe pas.\n")
            continue
        except dns.resolver.NoAnswer:
            print(f"[DNS] Le sous-domaine {full_domain} n'a pas de réponse.\n")
            continue
        except Exception as e:
            print(f"[DNS] Erreur avec {full_domain}: {e}\n")
            continue

        # Vérification HTTP
        try:
            response_http = requests.get(f"http://{full_domain}", timeout=5)
            print(f"[HTTP] http://{full_domain} → code {response_http.status_code}")
        except Exception as e:
            print(f"[HTTP] Erreur pour http://{full_domain} : {e}")

        # Vérification HTTPS
        try:
            response_https = requests.get(f"https://{full_domain}", timeout=5, verify=False)
            print(f"[HTTPS] https://{full_domain} → code {response_https.status_code}")
        except Exception as e:
            print(f"[HTTPS] Erreur pour https://{full_domain} : {e}")


        print(f"Nombre de site sous domaine trouvé {found}")

    input("\nAppuyez sur Entrée pour revenir au menu.")
