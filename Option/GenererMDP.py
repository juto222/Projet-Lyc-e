import random
import string

print(""" 






""")

motif = input("Pour quoi vous voulez un mot de passe ? : ")

longueur = int(input("Combien de caractères vous voulez (12 minimum recommandé) ?:"))

mdp_1 = string.ascii_letters + string.punctuation + string.digits

mdp = "".join(random.choices(mdp_1, k=longueur))


print(f"Le mot de passe pour {motif} est : {mdp}")