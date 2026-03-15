import random
import string
import time

def generer():
  
  print(r""" 

          _         _____ _  _   _ ____  
__  __   / \  _   _|___ /| || | | |  _ \ 
\ \/ /  / _ \| | | | |_ \| || |_| | |_) |
 >  <  / ___ \ |_| |___) |__   _|_|  _ < 
/_/\_\/_/   \_\__, |____/   |_| (_)_| \_\
              |___/                      

  """)

  motif = input("Pour quoi vous voulez un mot de passe ? : ")

  longueur = int(input("Combien de caractères vous voulez (12 minimum recommandé) ?:"))

  mdp_1 = string.ascii_letters + string.punctuation + string.digits

  mdp = "".join(random.choices(mdp_1, k=longueur))


  print(f"Le mot de passe pour {motif} est : {mdp}")
  with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Création d'un mot de passe pour {motif} ({mdp}) \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )
