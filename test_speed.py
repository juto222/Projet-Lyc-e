import time
from colorama import Fore
from internetspeedtest import SpeedTest

def speedtest_librespeed(langue_actuelle="FR"):
    try:
        if langue_actuelle == "FR":
            print(Fore.CYAN + "Lancement du test de vitesse...")
            time.sleep(1)
            print(Fore.YELLOW + "Recherche du meilleur serveur...")
        else:
            print(Fore.CYAN + "Starting speed test...")
            time.sleep(1)
            print(Fore.YELLOW + "Searching for the best server...")

        st = SpeedTest()

        servers = st.get_servers()
        best_server = st.find_best_server(servers)

        ping, jitter = st.ping(best_server)
        download_speed, _ = st.download(best_server)
        upload_speed, _ = st.upload(best_server)

        print(Fore.GREEN + "\n=== SPEEDTEST ===")
        print(Fore.WHITE + f"Ping      : {ping:.2f} ms")
        print(Fore.WHITE + f"Jitter    : {jitter:.2f} ms")
        print(Fore.WHITE + f"Download  : {download_speed:.2f} Mbps")
        print(Fore.WHITE + f"Upload    : {upload_speed:.2f} Mbps")
        print(Fore.WHITE + f"Serveur   : {best_server.name}")

    except Exception as e:
        if langue_actuelle == "FR":
            print(Fore.RED + f"❌ Erreur pendant le speed test : {e}")
        else:
            print(Fore.RED + f"❌ Error during speed test: {e}")

    time.sleep(2)

if __name__ == "__main__":
    speedtest_librespeed()