import requests
import os

path = input("Entrez le chemin complet du fichier à voler : ")

if os.path.isfile(path):
    with open(path, 'rb') as f:
        files = {'file': f}
        print("existe")
else:
    print("nn")