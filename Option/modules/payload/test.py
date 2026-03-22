import requests
from bs4 import BeautifulSoup
import pyautogui
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

site = "https://nonreversing-dulcie-dashingly.ngrok-free.dev/"


response = requests.get(site, verify=False)
soup = BeautifulSoup(response.text, "html.parser")
champ = soup.find("input", {"id": "cible"})
if champ:
    print(champ["value"])
    with open("test.txt", "w") as f:
        f.write(champ["value"])
else:
    print("Le champ 'Cible' n'existe pas sur la page.")





