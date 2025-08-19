import requests
import time



def ping():
    
    print("""





    """)

    ip = input("Entrez le domaine à scanner (ex : https://exemple.com): ")

    # Scan
    try:
        scan = requests.get(ip, timeout=5)
        if scan.status_code == 200:
            status = "En ligne !"
            print(f"L'IP est en ligne (code {scan.status_code})\n")
            print("Les logs sont disponible dans le fichier logs.txt\n")
        else:
            status = "Hors ligne !"
            print(f"L'IP a répondu avec le code {scan.status_code} \n")
            print("Les logs sont disponible dans le fichier logs.txt \n")
    except Exception as e:
        status = f"Hors ligne (erreur : {e})"
        print(f"Une erreur est survenue le site est inaccessible ou hors ligne: {e}\n")
        print("Les logs sont disponible dans le fichier logs.txt\n")

    # Affiche les logs
    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Ping {ip} : {status}\n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )

ping()
