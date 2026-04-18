import requests
import time
from Option.utils.display import ask, success, error, result, log

def ping():

    ip = ask("Domaine ou URL à tester (ex : https://exemple.com)")

    try:
        scan = requests.get(ip, timeout=5)

        if scan.status_code == 200:
            success(f"{ip} est EN LIGNE (code {scan.status_code})")
            log(f"Ping {ip} : En ligne (code {scan.status_code})")
        else:
            error(f"{ip} est HORS LIGNE (code {scan.status_code})")
            log(f"Ping {ip} : Hors ligne (code {scan.status_code})")

        result("Code HTTP", scan.status_code)
        result("Temps de réponse", f"{scan.elapsed.total_seconds():.3f}s")

    except requests.exceptions.ConnectionError:
        error(f"Impossible de joindre {ip} — hôte inaccessible.")
        log(f"Ping {ip} : Erreur de connexion")
    except requests.exceptions.Timeout:
        error(f"Timeout — {ip} n'a pas répondu dans les 5 secondes.")
        log(f"Ping {ip} : Timeout")
    except Exception as e:
        error(f"Erreur inattendue : {e}")
        log(f"Ping {ip} : Erreur — {e}")
