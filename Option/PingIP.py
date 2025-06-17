import requests


def ping():
    
    print("""





    """)

    ip = input("Entrez le domaine à scanner (ex : https://exemple.com): ")

    try:
        scan = requests.get(ip, timeout=5)
        if scan.status_code == 200:
            print(f"L'IP est en ligne (code {scan.status_code})")
        else:
            print(f"L'IP a répondu avec le code {scan.status_code}")
    except Exception as e:
        print(f"Une erreur est survenue le site est inaccessible ou hors ligne: {e}")
