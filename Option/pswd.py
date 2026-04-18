import hashlib
import requests
from Option.utils.display import ask, success, error, warning, info, result

def pswd_compromis():


    pswd = ask("Mot de passe à vérifier")

    if not pswd:
        error("Le mot de passe ne peut pas être vide.")
        return

    sha1_pswd = hashlib.sha1(pswd.encode("utf-8")).hexdigest().upper()
    prefix    = sha1_pswd[:5]
    suffix    = sha1_pswd[5:]

    info("Interrogation de la base HaveIBeenPwned...")

    url     = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "Projet-Lycee-PwnedCheck"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        error(f"Erreur réseau : {e}")
        return

    if response.status_code == 429:
        warning("Trop de requêtes (429) — réessaie dans quelques secondes.")
        return
    if response.status_code != 200:
        error(f"Erreur API : HTTP {response.status_code}")
        return

    for line in response.text.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        h, count = line.split(":", 1)
        if h.upper() == suffix:
            error(f"Mot de passe compromis {count.strip()} fois !")
            result("Conseil", "Change ce mot de passe immédiatement")
            return

    success("Ce mot de passe n'a pas été trouvé dans les bases de données compromises.")
    result("Conseil", "Même s'il n'est pas compromis, pense à utiliser un mot de passe fort et unique pour chaque compte.")