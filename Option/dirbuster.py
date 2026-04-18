import requests
import urllib3
from Option.utils.display import ask, ask_confirm, success, error, warning, info, found, result, separator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def dirbuster():


    domain = ask("Domaine cible (ex: example.com)")
    domain = domain.replace("http://", "").replace("https://", "").strip("/")

    paths = [
        "admin", "admin/login", "administrator", "backend", "console",
        "manage", "dashboard", "panel", "cpanel", "root", "superadmin",
        "dev", "devtools", "debug", "debugger", "beta", "staging",
        "internal", "intranet", "hidden", "private", "secret",
        "config", "settings", "environment",
        "api", "v1", "v2", "api/internal", "api/private", "graphql",
        "swagger", "openapi", "health", "healthcheck",
        "auth", "login", "signin", "logout", "signup", "register",
        "session", "token", "oauth", "sso", "user", "users",
        "uploads", "upload", "files", "media", "assets", "static",
        "backup", "backups", "archives", "old", "logs", "tmp",
        "monitor", "monitoring", "status", "metrics", "grafana",
        "prometheus", "kibana", "elastic", "jenkins", "ci", "cd",
        "payment", "payments", "billing", "checkout", "orders",
        "customers", "account", "profile",
        "wp-admin", "wp-login.php", "wp-content",
        "drupal", "joomla", "umbraco",
        "docs", "documentation", "api-docs", "developer",
        "changelog", "release", "version",
    ]

    use_custom = ask_confirm("Utiliser une wordlist personnalisée en plus")
    if use_custom:
        wordlist_path = ask("Chemin de la wordlist (ex: C:\\wordlist.txt)")
        try:
            with open(wordlist_path, "r", encoding="utf-8") as f:
                custom = [line.strip().lstrip("/") for line in f if line.strip()]
                paths.extend(custom)
            success(f"{len(custom)} chemins supplémentaires chargés.")
        except FileNotFoundError:
            error("Wordlist introuvable — utilisation de la liste par défaut.")
        except Exception as e:
            error(f"Erreur lecture wordlist : {e}")

    total_found  = 0
    total_tested = 0

    info(f"Scan de {len(paths)} chemins sur {domain}...")
    separator()

    for path in paths:
        total_tested += 1
        path          = path.lstrip("/")
        ok            = False

        for scheme in ("https", "http"):
            url = f"{scheme}://{domain}/{path}"
            try:
                r = requests.get(url, timeout=5, verify=False, allow_redirects=True)
                if r.status_code < 400:
                    found(f"[{scheme.upper()}] /{path} → {r.status_code}")
                    total_found += 1
                    ok = True
                    break
                else:
                    info(f"[{scheme.upper()}] /{path} → {r.status_code}")
            except requests.RequestException:
                pass

        if not ok:
            warning(f"/{path} — inaccessible")

    separator()
    result("Chemins testés", total_tested)
    result("Chemins trouvés", total_found)
    success("Scan terminé.")
    ask("Appuyez sur Entrée pour revenir au menu")
