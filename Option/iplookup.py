import requests
from Option.utils.display import ask, success, error, result, separator, info

def obtenir_infos_ip():


    print(r"""
     ___ ____    _                _               
    |_ _|  _ \  | |    ___   ___ | | ___   _ _ __ 
     | || |_) | | |   / _ \ / _ \| |/ / | | | '_ \
     | ||  __/  | |__| (_) | (_) |   <| |_| | |_) |
    |___|_|     |_____\___/ \___/|_|\_\\__,_| .__/ 
                                             |_|    
""")

    ip_address = ask("Adresse IP à analyser")

    if not ip_address:
        error("L'adresse IP ne peut pas être vide.")
        return

    info(f"Recherche en cours pour : {ip_address}")

    try:
        response = requests.get(f"http://ipinfo.io/{ip_address}/json", timeout=8)

        if response.status_code != 200:
            error(f"Impossible de récupérer les infos (HTTP {response.status_code}).")
            return

        data = response.json()

        separator()
        result("IP",           data.get("ip",       "N/A"))
        result("Ville",        data.get("city",      "N/A"))
        result("Région",       data.get("region",    "N/A"))
        result("Pays",         data.get("country",   "N/A"))
        result("FAI / Org",    data.get("org",       "N/A"))
        result("Code postal",  data.get("postal",    "N/A"))
        result("Coordonnées",  data.get("loc",       "N/A"))
        result("Fuseau",       data.get("timezone",  "N/A"))
        separator()

        success("Recherche terminée.")

    except requests.exceptions.Timeout:
        error("Timeout — le serveur n'a pas répondu.")
    except Exception as e:
        error(f"Erreur inattendue : {e}")
