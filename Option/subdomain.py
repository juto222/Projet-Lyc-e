import dns.resolver
import requests
import urllib3
from Option.utils.display import ask, success, error, warning, info, found, result, separator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def sousdomaine():

    print(r"""
    ____  _   _ ____  ____   ___  __  __    _    ___ _   _ 
   / ___|| | | | __ )|  _ \ / _ \|  \/  |  / \  |_ _| \ | |
   \___ \| | | |  _ \| | | | | | | |\/| | / _ \  | ||  \| |
    ___) | |_| | |_) | |_| | |_| | |  | |/ ___ \ | || |\  |
   |____/ \___/|____/|____/ \___/|_|  |_/_/   \_\___|_| \_|
""")

    domain = ask("Domaine cible (ex: example.com)")
    domain = domain.replace("http://", "").replace("https://", "").strip("/")

    subdomains = [
        "www", "mail", "ftp", "dev", "admin", "blog", "api", "admin-api",
        "dashboard", "support", "staging", "shop", "portal", "login", "app",
        "webmail", "dns", "vpn", "help", "test", "m", "mobile", "news",
        "contact", "docs", "git", "status", "secure", "files", "media",
        "cloud", "storage", "appserver", "crm", "billing", "payments",
        "analytics", "customer", "account", "store", "order", "auth",
        "devops", "email", "api-dev", "api-staging", "monitoring",
        "sandbox", "internal", "backup", "root", "private", "ssh",
    ]

    tested   = 0
    found_dns = 0
    found_web = 0

    info(f"Test de {len(subdomains)} sous-domaines pour {domain}...")
    separator()

    for sub in subdomains:
        tested      += 1
        full_domain  = f"{sub}.{domain}"
        dns_ok       = False

        try:
            dns.resolver.resolve(full_domain, "A")
            found(f"[DNS] {full_domain} existe")
            found_dns += 1
            dns_ok     = True
        except dns.resolver.NXDOMAIN:
            info(f"[DNS] {full_domain} — inexistant")
            continue
        except dns.resolver.NoAnswer:
            warning(f"[DNS] {full_domain} — pas de réponse A")
            continue
        except dns.resolver.LifetimeTimeout:
            warning(f"[DNS] {full_domain} — timeout")
            continue
        except Exception as e:
            error(f"[DNS] {full_domain} — {e}")
            continue

        if dns_ok:
            web_ok = False

            for scheme in ("http", "https"):
                url    = f"{scheme}://{full_domain}"
                verify = scheme == "https"
                try:
                    r = requests.get(url, timeout=5, verify=False, allow_redirects=True)
                    if r.status_code < 400:
                        found(f"[{scheme.upper()}] {url} → {r.status_code}")
                        web_ok = True
                    else:
                        info(f"[{scheme.upper()}] {url} → {r.status_code}")
                except requests.RequestException as e:
                    warning(f"[{scheme.upper()}] Erreur {full_domain} : {e}")

            if web_ok:
                found_web += 1

        separator()

    result("Sous-domaines testés",           tested)
    result("Sous-domaines trouvés (DNS)",    found_dns)
    result("Sous-domaines accessibles (Web)", found_web)
    success("Scan terminé.")
    ask("Appuyez sur Entrée pour revenir au menu")
