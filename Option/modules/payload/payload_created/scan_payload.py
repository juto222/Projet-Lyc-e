import socket
import time
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# ============================================================
# Configuration générée automatiquement
# ============================================================
PORT_DEBUT       = 1
PORT_FIN         = 1024
NB_TENTATIVES    = 1
DELAI            = 0
TIMEOUT          = 1
SHOW_OPEN        = True
SHOW_CLOSED      = True
SHOW_FILTERED    = True
NB_THREADS       = 100
DISCORD_WEBHOOK  = 'https://discord.com/api/webhooks/1485285287427969184/fr9lo82YRqbEMLzbJBgOM0x-eMDSWTy4Gbjk08XcJrB26q13x3Pyy_wYplwEEI4F7lu9'
HTTP_URL         = None

# ============================================================
# Fonction qui teste UN seul port
# Elle sera appelée en parallèle par les threads
# ============================================================

def scanner_port(cible, port):
    for _ in range(NB_TENTATIVES):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT)
            resultat = sock.connect_ex((cible, port))
            sock.close()
            if resultat == 0:
                return (port, 'ouvert')
            else:
                return (port, 'fermé')
        except socket.timeout:
            return (port, 'filtré')
        except OSError:
            return (port, 'filtré')
        time.sleep(DELAI)
    return (port, 'fermé')

# ============================================================
# Lancement du scan avec threads
# ============================================================

def lancer_scan():
    cible = requests.get("https://api.ipify.org").text
    total = PORT_FIN - PORT_DEBUT + 1
    print(f'\nScan de {cible} | ports {PORT_DEBUT}-{PORT_FIN} | {total} ports | {NB_THREADS} threads\n')

    ouverts = []
    fermes  = []
    filtres = []
    debut   = datetime.datetime.now()
    comptes = 0

    # ThreadPoolExecutor crée NB_THREADS 'ouvriers' qui travaillent en parallèle.
    # Sans threads : 1000 ports x 1s timeout = ~1000 secondes.
    # Avec 100 threads : ~10 secondes (100x plus rapide).
    with ThreadPoolExecutor(max_workers=NB_THREADS) as executor:

        # On envoie tous les ports à tester en une seule fois
        futures = {
            executor.submit(scanner_port, cible, port): port
            for port in range(PORT_DEBUT, PORT_FIN + 1)
        }

        # On récupère les résultats au fur et à mesure qu'ils terminent
        for future in as_completed(futures):
            port, etat = future.result()
            comptes += 1
            print(f'  Progression : {comptes}/{total}', end='\r')

            if etat == 'ouvert':
                ouverts.append(port)
                if SHOW_OPEN:
                    print(f'  [OUVERT]   Port {port}     ')
            elif etat == 'fermé':
                fermes.append(port)
                if SHOW_CLOSED:
                    print(f'  [FERMÉ]    Port {port}     ')
            elif etat == 'filtré':
                filtres.append(port)
                if SHOW_FILTERED:
                    print(f'  [FILTRÉ]   Port {port}     ')

    fin = datetime.datetime.now()
    ouverts.sort()

    print(f'\n\nScan terminé en {fin - debut}')
    print(f'Ports ouverts  : {len(ouverts)}')
    print(f'Ports filtrés  : {len(filtres)}')
    print(f'Ports fermés   : {len(fermes)}')

    # ---- Écriture dans le fichier TXT ----
    nom_fichier = f"resultats_scan_{cible}_{debut.strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nom_fichier, 'w', encoding='utf-8') as txt:
        txt.write(f"Rapport de scan - {debut.strftime('%d/%m/%Y %H:%M:%S')}\n")
        txt.write(f"Cible    : {cible}\n")
        txt.write(f"Plage    : {PORT_DEBUT} -> {PORT_FIN}\n")
        txt.write(f"Threads  : {NB_THREADS}\n")
        txt.write(f"Durée    : {fin - debut}\n")
        txt.write('=' * 40 + '\n\n')

        txt.write(f"Ports ouverts ({len(ouverts)}) :\n")
        for p in ouverts:
            txt.write(f"  - {p}\n")

        txt.write(f"\nPorts filtrés ({len(filtres)}) :\n")
        for p in filtres:
            txt.write(f"  - {p}\n")

        txt.write(f"\nPorts fermés ({len(fermes)}) :\n")
        for p in fermes:
            txt.write(f"  - {p}\n")

    print(f'Résultats enregistrés dans : {nom_fichier}')

    if DISCORD_WEBHOOK:
        message = (
            f'**Scan terminé** sur `{cible}` (ports {PORT_DEBUT}-{PORT_FIN})\n'
            f'Ouverts : {len(ouverts)} | Filtrés : {len(filtres)} | Fermés : {len(fermes)}\n'
            f'Ports ouverts : {ouverts}'
        )
        try:
            requests.post(DISCORD_WEBHOOK, json={'content': message})
            print('Résultats envoyés sur Discord.')
        except Exception as e:
            print(f'Erreur envoi Discord : {e}')

    if HTTP_URL:
        data = {
            'cible': cible,
            'port_debut': PORT_DEBUT,
            'port_fin': PORT_FIN,
            'ouverts': ouverts,
            'filtres': filtres,
            'fermes': fermes,
        }
        try:
            requests.post(HTTP_URL, json=data)
            print('Résultats envoyés sur le serveur HTTP.')
        except Exception as e:
            print(f'Erreur envoi HTTP : {e}')

if __name__ == '__main__':
    lancer_scan()
