import requests
import time



def ping():
    
    print("""




    """)

    ip = input("Entrez le domaine à scanner (ex : https://exemple.com): ")


    try:
        scan = requests.get(ip, timeout=5)
        if scan.status_code == 200:
            status = "En ligne !"
            print(f"L'IP est en ligne (code {scan.status_code})\n")
            with open("logs.txt", "a") as fichier:
                fichier.write(
                    f"------------------------------------\n"
                    f"\n"
                    f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Ping {ip} : {status}\n"
                    f"\n"
                    f"------------------------------------\n"
            f"\n"
        )
        else:
            status = f"Hors ligne (code {scan.status_code})"
            print(f"L'IP est hors ligne (code {scan.status_code})\n")
            with open("logs.txt", "a") as fichier:
                fichier.write(
                    f"------------------------------------\n"
                    f"\n"
                    f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] Ping {ip} : {status}\n"
                    f"\n"
                    f"------------------------------------\n"
            f"\n"
        )
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}\n")
