import dns.resolver
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def sousdomaine():
    print(r"""
                         _  _  _  _  _  _  _  _  _      ______   _____   ______  
                        | || || || || || || || || |    / _____) / ___ \ |  ___ \ 
                        | || || || || || || || || |   | /      | |   | || | _ | |
                        | ||_|| || ||_|| || ||_|| |   | |      | |   | || || || |
                        | |___| || |___| || |___| | _ | \_____ | |___| || || || |
                         \______| \______| \______|(_) \______) \_____/ |_||_||_|  
    """)

    domain = input("[+] Entrez le domaine cible (ex: example.com): ").strip()
    domain = domain.replace("http://", "").replace("https://", "").strip("/")

    subdomains = [
        'www', 'mail', 'ftp', 'dev', 'admin', 'blog', 'api', 'admin-api',
        'dashboard', 'support', 'staging', 'shop', 'portal', 'login', 'app',
        'webmail', 'dns', 'vpn', 'help', 'test', 'm', 'mobile', 'news',
        'contact', 'docs', 'git', 'status', 'secure', 'files', 'media',
        'cloud', 'storage', 'appserver', 'crm', 'billing', 'payments',
        'analytics', 'customer', 'account', 'store', 'order', 'auth',
        'devops', 'email', 'api3-dev', 'api-staging', 'monitoring',
        'sandbox', 'internal', 'backup', 'root', 'private', 'ssh'
    ]

    tested = 0
    found_dns = 0
    found_web = 0

    for sub in subdomains:
        tested += 1
        full_domain = f"{sub}.{domain}"
        dns_ok = False

        # Vérification DNS
        try:
            dns.resolver.resolve(full_domain, "A")
            print(f"[DNS] [✓] Le sous-domaine {full_domain} existe.")
            found_dns += 1
            dns_ok = True
        except dns.resolver.NXDOMAIN:
            print(f"[DNS] [!] Le sous-domaine {full_domain} n'existe pas.")
            print("-" * 60)
            continue
        except dns.resolver.NoAnswer:
            print(f"[DNS] [!] Le sous-domaine {full_domain} existe mais n'a pas de réponse A.")
            print("-" * 60)
            continue
        except dns.resolver.LifetimeTimeout:
            print(f"[DNS] [!] Timeout pour {full_domain}.")
            print("-" * 60)
            continue
        except Exception as e:
            print(f"[DNS] [!] Erreur avec {full_domain} : {e}")
            print("-" * 60)
            continue

        if dns_ok:
            web_ok = False

            # Vérification HTTP
            try:
                response_http = requests.get(
                    f"http://{full_domain}",
                    timeout=5,
                    allow_redirects=True
                )
                print(f"[HTTP] http://{full_domain} -> code {response_http.status_code}")
                if response_http.status_code < 400:
                    web_ok = True
            except requests.RequestException as e:
                print(f"[HTTP] Erreur pour http://{full_domain} : {e}")

            # Vérification HTTPS
            try:
                response_https = requests.get(
                    f"https://{full_domain}",
                    timeout=5,
                    verify=False,
                    allow_redirects=True
                )
                print(f"[HTTPS] [✓] https://{full_domain} -> code {response_https.status_code}")
                if response_https.status_code < 400:
                    web_ok = True
            except requests.RequestException as e:
                print(f"[HTTPS] [!] Erreur pour https://{full_domain} : {e}")

            if web_ok:
                found_web += 1

        print("-" * 60)

    print(f"\n[+] Nombre total de sous-domaines testés : {tested}")
    print(f"[+] Nombre total de sous-domaines trouvés en DNS : {found_dns}")
    print(f"[+] Nombre total de sous-domaines accessibles en HTTP/HTTPS : {found_web}")

    input("\nAppuyez sur Entrée pour revenir au menu.")
