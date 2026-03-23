import os

def clear():
    os.system("cls")

def affichage():
    clear()
    print("=== Configuration Steal Payload ===\n\n")
    print("""
          
          Options : 
    1. Chemin du fichier à voler (ex: C:\\Users\\User\\Documents\\secret.txt)
    2. URL de destination pour envoyer le fichier volé (ex: http://example.com/upload)
    3. Mot de passe à volé (y/n)
          """)