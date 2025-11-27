import speedtest
from colorama import Fore, Style
import time
import os


def test_speed():
    os.system("cls" if os.name == "nt" else "clear")

    print(f"""
{Fore.CYAN}
{Fore.MAGENTA} Test de vitesse Internet
{Style.RESET_ALL}
""")

    try:
        st = speedtest.Speedtest()

        print(f"{Fore.YELLOW}Recherche du meilleur serveur...{Style.RESET_ALL}")
        st.get_best_server()
        time.sleep(1)

        print(f"{Fore.YELLOW}Test de téléchargement en cours...{Style.RESET_ALL}")
        download = st.download()
        download_mbps = download / 1_000_000
        print(f"{Fore.GREEN}Vitesse de téléchargement : {download_mbps:.2f} Mbps{Style.RESET_ALL}")
        time.sleep(1)

        print(f"{Fore.YELLOW}Test de téléversement en cours...{Style.RESET_ALL}")
        upload = st.upload()
        upload_mbps = upload / 1_000_000
        print(f"{Fore.GREEN}Vitesse de téléversement : {upload_mbps:.2f} Mbps{Style.RESET_ALL}")
        time.sleep(1)

        ping = st.results.ping
        print(f"{Fore.GREEN}Ping : {ping:.2f} ms{Style.RESET_ALL}\n")

        # Résultats bruts (optionnel)
        # print(st.results.dict())

        # Logging
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(
                f"------------------------------------\n"
                f"[{time.strftime('%d-%m-%Y %H:%M:%S')}] "
                f"Download: {download_mbps:.2f} Mbps | "
                f"Upload: {upload_mbps:.2f} Mbps | "
                f"Ping: {ping:.2f} ms\n"
                f"------------------------------------\n\n"
            )

    except Exception as e:
        print(f"{Fore.RED}Erreur lors du test : {e}{Style.RESET_ALL}")

