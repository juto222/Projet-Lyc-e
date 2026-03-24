import nmap


def scan():
    print(r"""
                    _      ______          ______  
                   | |    / _____)   /\   |  ___ \ 
                    \ \  | /        /  \  | |   | |
                     \ \ | |       / /\ \ | |   | |
                 _____) )| \_____ | |__| || |   | |
                (______/  \______)|______||_|   |_|
    """)

    print("=" * 60)

    ip         = input("[+] Adresse IP ou domaine à scanner : ").strip()
    port_range = input("[+] Plage de ports (ex: 0-1024) : ").strip()

    # ------------------------------------------------------------------ #
    # BUG 1 — nm était instancié UNE FOIS au niveau du module             #
    # Si scan() était appelé deux fois, le même objet était réutilisé     #
    # et les résultats du scan précédent pouvaient rester en mémoire.     #
    # Fix : on crée un nouvel objet à chaque appel.                       #
    # ------------------------------------------------------------------ #
    nm = nmap.PortScanner()

    # ------------------------------------------------------------------ #
    # BUG 2 — time.sleep(1) x3 = 3 secondes de délai inutile             #
    # Supprimé.                                                            #
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    # BUG 3 — nm.scan() plantait silencieusement si nmap n'est pas        #
    # installé sur le système (nmap ≠ python-nmap).                       #
    # python-nmap est juste un wrapper, il faut aussi nmap.exe / nmap     #
    # installé sur la machine.                                             #
    # Fix : on attrape l'exception nmap.PortScannerError séparément.      #
    # ------------------------------------------------------------------ #
    print(f"\n[*] Scan de {ip} sur les ports {port_range}...\n")
    print("[*] Cela peut prendre quelques secondes, merci de patienter...\n")

    try:
        nm.scan(hosts=ip, ports=port_range)

    except nmap.PortScannerError as e:
        # Cette erreur arrive quand nmap n'est PAS installé sur le système
        # Solution : installer nmap (pas python-nmap, le vrai nmap)
        # Windows : https://nmap.org/download.html
        # Linux   : sudo apt install nmap
        print(f"[!] nmap non trouvé sur le système : {e}")
        print("""[!] Solution : installer nmap (pas python-nmap, le vrai nmap)
 Windows : https://nmap.org/download.html
 Linux   : sudo apt install nmap""")
        print("[!] Installez nmap : https://nmap.org/download.html")
        input("\nAppuyez sur Entrée pour revenir au menu.")
        return

    except Exception as e:
        print(f"[!] Erreur inattendue : {e}")
        input("\nAppuyez sur Entrée pour revenir au menu.")
        return

    # ------------------------------------------------------------------ #
    # BUG 4 — all_hosts() retourne une liste vide si l'IP est injoignable #
    # ou si le scan n'a rien trouvé. Sans vérification, la boucle         #
    # s'exécutait sans rien afficher et l'utilisateur ne comprenait pas.  #
    # Fix : on vérifie que la liste n'est pas vide.                       #
    # ------------------------------------------------------------------ #
    hosts = nm.all_hosts()

    if not hosts:
        print("[!] Aucun hôte trouvé. Vérifiez l'IP et la plage de ports.")
        input("\nAppuyez sur Entrée pour revenir au menu.")
        return

    # Affichage des résultats
    for host in hosts:
        print(f"[+] Host     : {host} ({nm[host].hostname()})")
        print(f"[+] État     : {nm[host].state()}")

        for proto in nm[host].all_protocols():
            print(f"\n--- Protocole : {proto} ---")

            # ---------------------------------------------------------- #
            # BUG 5 — .keys() retourne une vue non triée                  #
            # Les ports s'affichaient dans un ordre aléatoire.            #
            # Fix : sorted() pour avoir les ports dans l'ordre croissant. #
            # ---------------------------------------------------------- #
            ports = sorted(nm[host][proto].keys())

            for port in ports:
                state   = nm[host][proto][port]["state"]
                service = nm[host][proto][port].get("name", "?")  # nom du service
                print(f"  [*] Port {port:<6} | {state:<10} | {service}")

        print()

    input("\nAppuyez sur Entrée pour revenir au menu.")

