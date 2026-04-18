import os
from Option.utils.display import ask, success, error, info, warning, separator

def crypt():

    print(r"""
     _____ ______   ____  ____  ____
    / ____|  ____| |  _ \|  _ \|  _ \
   | |    | |_     | |_) | |_) | |_) |
   | |    |  _|    |  __/|  __/|  _ <
   | |____| |      | |   | |   | |_) |
    \_____|_|      |_|   |_|   |____/
""")

    info("Obfuscateurs disponibles :")
    separator()
    info("1. PyArmor  — Protège le code avec du bytecode chiffré")
    info("2. Nuitka   — Compile Python → C (protection maximale)")
    separator()

    try:
        option = int(ask("Choisissez un obfuscateur (1 ou 2)"))
    except ValueError:
        error("Veuillez entrer 1 ou 2.")
        return

    if option not in (1, 2):
        error("Option invalide. Choisissez 1 ou 2.")
        return

    path       = ask("Chemin du fichier Python à chiffrer")
    output_dir = ask("Répertoire de sortie")

    if not os.path.isfile(path):
        error(f"Fichier introuvable : {path}")
        return

    if option == 1:
        info("Lancement de PyArmor...")
        os.system(f"pyarmor gen --output {output_dir} {path}")
        success(f"Fichier chiffré généré dans : {output_dir}")

    elif option == 2:
        warning("Pré-requis Nuitka :")
        info("  • Compilateur C installé (Visual Studio Build Tools)")
        info("    https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/")
        info("  • Cochez : Desktop development with C++")
        info("  • Cochez : Windows 10/11 SDK")
        info("  • Environ 9 Go — redémarrez après installation")
        separator()
        ask("Lisez les pré-requis, puis appuyez sur Entrée pour continuer")
        info("Lancement de Nuitka...")
        os.system(f"nuitka --output-dir={output_dir} --onefile {path}")
        success(f"Exécutable généré dans : {output_dir}")
