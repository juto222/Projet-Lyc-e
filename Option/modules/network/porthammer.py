import os
from colorama import Fore, Style, init
import time
import random

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "[*] === Configuration Scan de Ports ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Port de début (plage)
    2. Port de fin (plage)
    3. Nombre de tentatives de connexion
    4. Délai entre les tentatives (en secondes)
    5. Timeout de la connexion (en secondes)
    6. Afficher les ports ouverts
    7. Afficher les ports fermés
    8. Afficher les ports filtrés
    11. Nombre de threads (parallélisme)
        
         
          {Fore.YELLOW}Sortie et envoi:
{Fore.WHITE}
    9. Envoi sur Discord
    10. Envoi sur serveur HTTP
    
{Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
                  """)

def scan_module():
    clear()

    choix = {
        "Port de début": None,
        "Port de fin": None,
        "Nombre de tentatives": None,
        "Délai entre tentatives": None,
        "Timeout de connexion": None,
        "Afficher ports ouverts": None,
        "Afficher ports fermés": None,
        "Afficher ports filtrés": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
        "Nombre de threads": 100,
    }

    def port_debut():
        clear()
        port = input("Entrez le port de début de la plage (ex: 1) : ")
        try:
            port = int(port)
            if 1 <= port <= 65535:
                choix["Port de début"] = port
                print(f"[+] Port de début défini sur {port}.")
            else:
                print(Fore.RED + "[!] Le port doit être entre 1 et 65535." + Style.RESET_ALL)
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def port_fin():
        clear()
        port = input("Entrez le port de fin de la plage (ex: 1024) : ")
        try:
            port = int(port)
            if 1 <= port <= 65535:
                choix["Port de fin"] = port
                print(f"[+] Port de fin défini sur {port}.")
            else:
                print(Fore.RED + "Le port doit être entre 1 et 65535." + Style.RESET_ALL)
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def nb_tentatives():
        clear()
        nb = input("Nombre de tentatives de connexion : ")
        try:
            nb = int(nb)
            choix["Nombre de tentatives"] = nb
            print(f"[+] Nombre de tentatives défini sur {nb}.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def delai_tentatives():
        clear()
        delay = input("Délai entre les tentatives (secondes, 'random' pour 1-10s) : ")
        try:
            if delay.lower() == "random":
                delay = random.randint(1, 10)
            else:
                delay = float(delay)
            choix["Délai entre tentatives"] = delay
            print(f"[+] Délai défini sur {delay} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide ou 'random'." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def timeout_connexion():
        clear()
        timeout = input("Timeout de connexion (secondes) : ")
        try:
            timeout = float(timeout)
            choix["Timeout de connexion"] = timeout
            print(f"[+] Timeout défini sur {timeout} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def afficher_ports(typ):
        clear()
        reponse = input(f"Afficher les ports {typ} ? (y/n) : ").lower()
        choix[f"Afficher ports {typ}"] = reponse == 'y'
        affichage()

    def envoi_discord():
        clear()
        webhook = input("Entrez l'URL du webhook Discord : ")
        choix["Envoi sur Discord"] = webhook
        affichage()

    def envoi_http():
        clear()
        url = input("Entrez l'URL de votre serveur HTTP : ")
        choix["Envoi sur serveur HTTP"] = url
        affichage()

    def nb_threads():
        clear()
        print("Le nombre de threads = combien de ports sont scannés EN MÊME TEMPS.")
        print("Plus c'est élevé, plus c'est rapide. Recommandé : 100 à 500.\n")
        nb = input("Nombre de threads (défaut : 100) : ")
        try:
            nb = int(nb)
            if nb < 1:
                raise ValueError
            choix["Nombre de threads"] = nb
            print(f"Nombre de threads défini sur {nb}.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre entier positif." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    options = [
        ("Port de début",            port_debut),        # 1
        ("Port de fin",              port_fin),          # 2
        ("Nombre de tentatives",     nb_tentatives),     # 3
        ("Délai entre tentatives",   delai_tentatives),  # 4
        ("Timeout de connexion",     timeout_connexion), # 5
        ("Afficher ports ouverts",   lambda: afficher_ports("ouverts")),  # 6
        ("Afficher ports fermés",    lambda: afficher_ports("fermés")),   # 7
        ("Afficher ports filtrés",   lambda: afficher_ports("filtrés")),  # 8
        ("Envoi sur Discord",        envoi_discord),     # 9
        ("Envoi sur serveur HTTP",   envoi_http),        # 10
        ("Nombre de threads",        nb_threads),        # 11
    ]

    def create_payload():

        if choix["Port de début"] is None or choix["Port de fin"] is None:
            print(Fore.RED + "Erreur : définissez le port de début ET le port de fin (options 1 et 2)." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        if choix["Port de début"] > choix["Port de fin"]:
            print(Fore.RED + "Erreur : le port de début doit être <= au port de fin." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "scan_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:

            f.write("import socket\n")
            f.write("import time\n")
            f.write("import datetime\n")
            # ThreadPoolExecutor : lance plusieurs fonctions en parallèle (= threads)
            # as_completed       : récupère les résultats au fur et à mesure
            f.write("from concurrent.futures import ThreadPoolExecutor, as_completed\n")
            if choix["Envoi sur Discord"] or choix["Envoi sur serveur HTTP"]:
                f.write("import requests\n")
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"PORT_DEBUT       = {choix['Port de début']}\n")
            f.write(f"PORT_FIN         = {choix['Port de fin']}\n")
            f.write(f"NB_TENTATIVES    = {choix['Nombre de tentatives'] or 1}\n")
            f.write(f"DELAI            = {choix['Délai entre tentatives'] or 0}\n")
            f.write(f"TIMEOUT          = {choix['Timeout de connexion'] or 1}\n")
            f.write(f"SHOW_OPEN        = {choix['Afficher ports ouverts'] if choix['Afficher ports ouverts'] is not None else True}\n")
            f.write(f"SHOW_CLOSED      = {choix['Afficher ports fermés'] if choix['Afficher ports fermés'] is not None else False}\n")
            f.write(f"SHOW_FILTERED    = {choix['Afficher ports filtrés'] if choix['Afficher ports filtrés'] is not None else False}\n")
            f.write(f"NB_THREADS       = {choix['Nombre de threads']}\n")
            if choix["Envoi sur Discord"]:
                f.write(f"DISCORD_WEBHOOK  = {repr(choix['Envoi sur Discord'])}\n")
            else:
                f.write("DISCORD_WEBHOOK  = None\n")
            if choix["Envoi sur serveur HTTP"]:
                f.write(f"HTTP_URL         = {repr(choix['Envoi sur serveur HTTP'])}\n")
            else:
                f.write("HTTP_URL         = None\n")
            f.write("\n")

            f.write("# ============================================================\n")
            f.write("# Fonction qui teste UN seul port\n")
            f.write("# Elle sera appelée en parallèle par les threads\n")
            f.write("# ============================================================\n\n")

            f.write("def scanner_port(cible, port):\n")
            f.write("    for _ in range(NB_TENTATIVES):\n")
            f.write("        try:\n")
            f.write("            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n")
            f.write("            sock.settimeout(TIMEOUT)\n")
            f.write("            resultat = sock.connect_ex((cible, port))\n")
            f.write("            sock.close()\n")
            f.write("            if resultat == 0:\n")
            f.write("                return (port, 'ouvert')\n")
            f.write("            else:\n")
            f.write("                return (port, 'fermé')\n")
            f.write("        except socket.timeout:\n")
            f.write("            return (port, 'filtré')\n")
            f.write("        except OSError:\n")
            f.write("            return (port, 'filtré')\n")
            f.write("        time.sleep(DELAI)\n")
            f.write("    return (port, 'fermé')\n\n")

            f.write("# ============================================================\n")
            f.write("# Lancement du scan avec threads\n")
            f.write("# ============================================================\n\n")

            f.write("def lancer_scan():\n")
            f.write("    cible = input('Adresse IP ou hôte à scanner : ').strip()\n")
            f.write("    total = PORT_FIN - PORT_DEBUT + 1\n")
            f.write("    print(f'\\nScan de {cible} | ports {PORT_DEBUT}-{PORT_FIN} | {total} ports | {NB_THREADS} threads\\n')\n\n")
            f.write("    ouverts = []\n")
            f.write("    fermes  = []\n")
            f.write("    filtres = []\n")
            f.write("    debut   = datetime.datetime.now()\n")
            f.write("    comptes = 0\n\n")

            f.write("    # ThreadPoolExecutor crée NB_THREADS 'ouvriers' qui travaillent en parallèle.\n")
            f.write("    # Sans threads : 1000 ports x 1s timeout = ~1000 secondes.\n")
            f.write("    # Avec 100 threads : ~10 secondes (100x plus rapide).\n")
            f.write("    with ThreadPoolExecutor(max_workers=NB_THREADS) as executor:\n\n")
            f.write("        # On envoie tous les ports à tester en une seule fois\n")
            f.write("        futures = {\n")
            f.write("            executor.submit(scanner_port, cible, port): port\n")
            f.write("            for port in range(PORT_DEBUT, PORT_FIN + 1)\n")
            f.write("        }\n\n")
            f.write("        # On récupère les résultats au fur et à mesure qu'ils terminent\n")
            f.write("        for future in as_completed(futures):\n")
            f.write("            port, etat = future.result()\n")
            f.write("            comptes += 1\n")
            f.write("            print(f'  Progression : {comptes}/{total}', end='\\r')\n\n")
            f.write("            if etat == 'ouvert':\n")
            f.write("                ouverts.append(port)\n")
            f.write("                if SHOW_OPEN:\n")
            f.write("                    print(f'  [OUVERT]   Port {port}     ')\n")
            f.write("            elif etat == 'fermé':\n")
            f.write("                fermes.append(port)\n")
            f.write("                if SHOW_CLOSED:\n")
            f.write("                    print(f'  [FERMÉ]    Port {port}     ')\n")
            f.write("            elif etat == 'filtré':\n")
            f.write("                filtres.append(port)\n")
            f.write("                if SHOW_FILTERED:\n")
            f.write("                    print(f'  [FILTRÉ]   Port {port}     ')\n\n")

            f.write("    fin = datetime.datetime.now()\n")
            f.write("    ouverts.sort()\n\n")

            f.write("    print(f'\\n\\nScan terminé en {fin - debut}')\n")
            f.write("    print(f'Ports ouverts  : {len(ouverts)}')\n")
            f.write("    print(f'Ports filtrés  : {len(filtres)}')\n")
            f.write("    print(f'Ports fermés   : {len(fermes)}')\n\n")

            f.write("    # ---- Écriture dans le fichier TXT ----\n")
            f.write("    nom_fichier = f\"resultats_scan_{cible}_{debut.strftime('%Y%m%d_%H%M%S')}.txt\"\n")
            f.write("    with open(nom_fichier, 'w', encoding='utf-8') as txt:\n")
            f.write("        txt.write(f\"Rapport de scan - {debut.strftime('%d/%m/%Y %H:%M:%S')}\\n\")\n")
            f.write("        txt.write(f\"Cible    : {cible}\\n\")\n")
            f.write("        txt.write(f\"Plage    : {PORT_DEBUT} -> {PORT_FIN}\\n\")\n")
            f.write("        txt.write(f\"Threads  : {NB_THREADS}\\n\")\n")
            f.write("        txt.write(f\"Durée    : {fin - debut}\\n\")\n")
            f.write("        txt.write('=' * 40 + '\\n\\n')\n\n")
            f.write("        txt.write(f\"Ports ouverts ({len(ouverts)}) :\\n\")\n")
            f.write("        for p in ouverts:\n")
            f.write("            txt.write(f\"  - {p}\\n\")\n\n")
            f.write("        txt.write(f\"\\nPorts filtrés ({len(filtres)}) :\\n\")\n")
            f.write("        for p in filtres:\n")
            f.write("            txt.write(f\"  - {p}\\n\")\n\n")
            f.write("        txt.write(f\"\\nPorts fermés ({len(fermes)}) :\\n\")\n")
            f.write("        for p in fermes:\n")
            f.write("            txt.write(f\"  - {p}\\n\")\n\n")
            f.write("    print(f'Résultats enregistrés dans : {nom_fichier}')\n\n")

            f.write("    if DISCORD_WEBHOOK:\n")
            f.write("        message = (\n")
            f.write("            f'**Scan terminé** sur `{cible}` (ports {PORT_DEBUT}-{PORT_FIN})\\n'\n")
            f.write("            f'Ouverts : {len(ouverts)} | Filtrés : {len(filtres)} | Fermés : {len(fermes)}\\n'\n")
            f.write("            f'Ports ouverts : {ouverts}'\n")
            f.write("        )\n")
            f.write("        try:\n")
            f.write("            requests.post(DISCORD_WEBHOOK, json={'content': message})\n")
            f.write("            print('Résultats envoyés sur Discord.')\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f'Erreur envoi Discord : {e}')\n\n")

            f.write("    if HTTP_URL:\n")
            f.write("        data = {\n")
            f.write("            'cible': cible,\n")
            f.write("            'port_debut': PORT_DEBUT,\n")
            f.write("            'port_fin': PORT_FIN,\n")
            f.write("            'ouverts': ouverts,\n")
            f.write("            'filtres': filtres,\n")
            f.write("            'fermes': fermes,\n")
            f.write("        }\n")
            f.write("        try:\n")
            f.write("            requests.post(HTTP_URL, json=data)\n")
            f.write("            print('Résultats envoyés sur le serveur HTTP.')\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f'Erreur envoi HTTP : {e}')\n\n")

            f.write("if __name__ == '__main__':\n")
            f.write("    lancer_scan()\n")

        print(Fore.GREEN + f"Payload généré dans {payload_path}" + Style.RESET_ALL)
        input("\nAppuyez sur Entrée pour continuer...")

    # -----------------------------------------------
    # Boucle principale
    # -----------------------------------------------
    while True:
        affichage()
        cmd = input(Fore.GREEN + ">> " + Style.RESET_ALL).strip()

        if cmd.lower() == "exit":
            break

        elif cmd.lower().startswith("set "):
            try:
                option_choix = int(cmd.split()[1]) - 1
                if 0 <= option_choix < len(options):
                    options[option_choix][1]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
                    time.sleep(1)
            except (ValueError, IndexError):
                print(Fore.RED + "Veuillez saisir 'set <num>'" + Style.RESET_ALL)
                time.sleep(1)

        elif cmd.lower() == "show":
            clear()
            print(Fore.CYAN + "\nConfiguration actuelle :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:30s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)
