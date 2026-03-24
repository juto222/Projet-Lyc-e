from colorama import Fore, Style, init
import hashlib
import requests

def pswd_compromis():
    print(f"""


    {Fore.MAGENTA} Mot de passe compromis
    


    """)

    pswd = input("[+] Entrez le mot de passe à vérifier : ")
    if not pswd:
        print(f"{Fore.RED}[!] Erreur : Le mot de passe ne peut pas être vide.{Style.RESET_ALL}")
        return

    sha1_pswd = hashlib.sha1(pswd.encode('utf-8')).hexdigest().upper()
    prefix = sha1_pswd[:5]
    suffix = sha1_pswd[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "Lycée - PwnedPasswordCheck (contact: freepalestine@gmail.com)"}

    try:
        mdp = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException as e:
        print(f"{Fore.RED}[!] Erreur réseau lors de la requête : {e}{Style.RESET_ALL}")
        return

    if mdp.status_code == 429:
        print(f"{Fore.YELLOW}[!] Trop de requêtes (429). Réessaie plus tard.{Style.RESET_ALL}")
        return
    if mdp.status_code != 200:
        print(f"{Fore.RED}[!] Erreur lors de la requête à l'API : HTTP {mdp.status_code}{Style.RESET_ALL}")
        return

    for line in mdp.text.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        h, count = line.split(':', 1)
        if h.upper() == suffix:
            print(f"{Fore.RED}[!] Le mot de passe '{pswd}' a été compromis {count.strip()} fois !{Style.RESET_ALL}")
            return

    print(f"{Fore.GREEN}[✓] Le mot de passe '{pswd}' n'a pas été trouvé dans la base de données des mots de passe compromis.{Style.RESET_ALL}")