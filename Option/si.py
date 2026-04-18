import os
import platform
import socket
import psutil
import getpass
import time
from Option.utils.display import success, error, result, separator, log, info

def info_system():

    print(r"""
     _____ _____ _____ _____ _____  __  __
    |   __|  |  |   __|_   _|   __||  \/  |
    |__   |ystem|__   | | | |   __||      |
    |_____|_____|_____| |_| |_____||_|  |_|
""")

    uname    = platform.uname()
    hostname = socket.gethostname()

    separator()
    info("── Système d'exploitation ──")
    result("Nom machine",    uname.node)
    result("OS",             f"{uname.system} {uname.release}")
    result("Version noyau",  uname.version)
    result("Architecture",   uname.machine)
    result("Utilisateur",    getpass.getuser())

    separator()
    info("── Hardware ──")
    result("CPU", platform.processor() or "Non détecté")

    try:
        mem = psutil.virtual_memory().total / (1024 ** 3)
        result("RAM totale", f"{round(mem, 2)} GB")
    except Exception:
        try:
            mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024 ** 3)
            result("RAM totale", f"{round(mem, 2)} GB")
        except Exception:
            error("RAM — impossible à détecter")

    separator()
    info("── Réseau ──")
    result("Nom d'hôte", hostname)

    try:
        result("IP locale", socket.gethostbyname(hostname))
    except Exception:
        error("IP locale — impossible à détecter")

    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            result(f"  {interface}", f"{addr.family.name} — {addr.address}")

    separator()
    success("Informations collectées.")

    log("Consultation des informations système")
