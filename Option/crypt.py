from colorama import Fore, Style
import os

def crypt():

    print(f"""{Fore.MAGENTA}
    Choisissez un obfuscateur pour chiffrer votre fichier python :
     {Fore.YELLOW}1.{Fore.CYAN} PyArmor (Recommandé)
     {Fore.YELLOW}2.{Fore.CYAN} Nuitka
    {Style.RESET_ALL}""")

    try:
        option = int(input("Choisissez un obfuscateur (1 ou 2 ) : "))
    except ValueError:
        print("Option invalide. Veuillez entrer un nombre (1 ou 2).")
        return
    
    path = input("Entrez le chemin du fichier python à chiffrer : ")
    output_dir = input("Entrez le répertoire de sortie pour le fichier chiffré : ")


    if option == 1:
        os.system(f"pyarmor gen --output {output_dir} {path}")
    elif option == 2:
        print("""- Avoir un compilateur C installé : https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/ (Visual Studio pour Windows)
    - A l'installation, cochez : 
        - "Desktop development with C++"
        - "MSVC v142 - VS 2019 C++ x64/x86 build tools" (après avoir coché "Desktop development with C++")
        - "Windows 10/11 SDK" (après avoir coché "Desktop development with C++")
        Ca devrait faire environ 9Go d'installation.

    - Redémarrez votre ordinateur après l'installation des outils de build.

    et vous pouvez lancer !""")
        input("Lisez les pré-requis et appuyez sur Entrée pour continuer...")
        os.system(f"nuitka --output-dir={output_dir} --onefile {path}")
    else:
        print("Option invalide. Veuillez choisir 1 ou 2.")
        return

    