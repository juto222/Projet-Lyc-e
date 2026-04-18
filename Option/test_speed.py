import time
import speedtest
from Option.utils.display import success, error, info, result, separator

def test_speed():

    try:
        info("Initialisation du test...")
        st = speedtest.Speedtest()

        info("Recherche du meilleur serveur...")
        st.get_best_server()

        info("Test du ping...")
        ping = st.results.ping

        info("Test de la vitesse de téléchargement...")
        download_speed = st.download() / 1_000_000

        info("Test de la vitesse d'envoi...")
        upload_speed = st.upload() / 1_000_000

        server_name = st.results.server.get("name", "Inconnu")
        sponsor     = st.results.server.get("sponsor", "Inconnu")

        separator()
        result("Ping",      f"{ping:.2f} ms")
        result("Download",  f"{download_speed:.2f} Mbps")
        result("Upload",    f"{upload_speed:.2f} Mbps")
        result("Serveur",   f"{server_name} ({sponsor})")
        separator()

        success("Test terminé.")

    except Exception as e:
        error(f"Erreur pendant le speedtest : {e}")

    time.sleep(1)
