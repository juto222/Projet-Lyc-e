import time
from colorama import Fore, init
import speedtest

init(autoreset=True)

def test_speed(langue_actuelle="FR"):
    try:
        if langue_actuelle == "FR":
            print(Fore.CYAN + "[*] Lancement du test de vitesse...")
            time.sleep(1)
            print(Fore.YELLOW + "[*] Recherche du meilleur serveur...")
        else:
            print(Fore.CYAN + "[*] Starting speed test...")
            time.sleep(1)
            print(Fore.YELLOW + "[*] Searching for the best server...")

        st = speedtest.Speedtest()
        st.get_best_server()

        ping = st.results.ping
        download_speed = st.download() / 1_000_000  # bits/s -> Mbps
        upload_speed = st.upload() / 1_000_000      # bits/s -> Mbps

        server_name = st.results.server.get("name", "Inconnu")
        sponsor = st.results.server.get("sponsor", "Inconnu")

        print(Fore.GREEN + "[+] === SPEEDTEST ===")
        print(Fore.WHITE + f"[*] Ping      : {ping:.2f} ms")
        print(Fore.WHITE + f"[*] Download  : {download_speed:.2f} Mbps")
        print(Fore.WHITE + f"[*] Upload    : {upload_speed:.2f} Mbps")
        print(Fore.WHITE + f"[*] Serveur   : {server_name} ({sponsor})")

    except Exception as e:
        if langue_actuelle == "FR":
            print(Fore.RED + f"[!] ❌ Erreur pendant le speed test : {e}")
        else:
            print(Fore.RED + f"[!] ❌ Error during speed test: {e}")

    time.sleep(2)

if __name__ == "__main__":
    test_speed()