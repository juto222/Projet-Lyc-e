import os
from colorama import Fore, Style  
import platform 
import socket
import psutil
import getpass
import time

def info_system():
    print(f"""

    {Fore.MAGENTA} Informations Système
    {Style.RESET_ALL}

    """)

    print(f"{Fore.BLUE} SYSTEME D'EXPLOITATION {Style.RESET_ALL}\n\n")

    uname = platform.uname()

    print(f"{Fore.YELLOW}Nom de l'ordinateur : {uname.node}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Système d'exploitation : {uname.system} {uname.release}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Version du noyau : {uname.version}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Architecture : {uname.machine}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Utilisateur actuel : {getpass.getuser()}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Nom de l'ordinateur : {platform.node()}{Style.RESET_ALL}\n\n")

    print(f"{Fore.BLUE} HARDWARE {Style.RESET_ALL}\n\n")

    print(f"{Fore.YELLOW}CPU : {platform.processor()}{Style.RESET_ALL}\n")
    try:
        if platform.system() == "Windows":
            mem = psutil.virtual_memory().total / (1024. ** 3)
        else:
            mem = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3)
        print(f"{Fore.YELLOW}Memoire Totale : {round(mem, 2)} GB{Style.RESET_ALL}\n")
    except:
        print(f"{Fore.YELLOW}Memoire Totale : Impossible à détecter{Style.RESET_ALL}\n")

    print(f"{Fore.BLUE} RÉSEAU {Style.RESET_ALL}\n\n")

    hostname = socket.gethostname()

    print(f"{Fore.YELLOW}Nom d'hôte : {hostname}{Style.RESET_ALL}\n")
    try:
        print(f"{Fore.YELLOW}Adresse IP : {socket.gethostbyname(hostname)}{Style.RESET_ALL}\n")
    except:
        print(f"{Fore.YELLOW}Adresse IP : Impossible à détecter{Style.RESET_ALL}")
    print(f"\n{Fore.BLUE}Interfaces réseau :")
    for interface, addrs in psutil.net_if_addrs().items():
        print(interface)
        for addr in addrs:
            print(f" {Fore.GREEN} {addr.family} - {addr.address} \n")

    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Obtention d'information du système \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )
