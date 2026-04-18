import os
import re
import time
import requests
import concurrent.futures
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random

# ─── User-Agents disponibles ───────────────────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
]

# ─── Dossier de sortie ─────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "page")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─── Récupère le contenu d'une URL (CSS ou JS) ────────────────────────────────
def fetch_url(url):
    try:
        r = requests.get(url, timeout=5)
        return r.text if r.status_code == 200 else None
    except Exception:
        return None


# ─── Inline tout le CSS et JS dans le HTML ────────────────────────────────────
def inline_css_and_js(html_content, base_url):
    soup = BeautifulSoup(html_content, "html.parser")

    # ── CSS ──────────────────────────────────────────────────────────────────
    print("[*] Récupération du CSS...")
    css_links = soup.find_all("link", rel="stylesheet")
    css_urls  = [urljoin(base_url, tag["href"]) for tag in css_links if tag.get("href")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        css_results = list(executor.map(fetch_url, css_urls))

    all_css = [css for css in css_results if css]
    if all_css:
        style_tag        = soup.new_tag("style")
        style_tag.string = "\n".join(all_css)
        if soup.head:
            soup.head.append(style_tag)
        for tag in css_links:       # supprime les <link> externes
            tag.decompose()

    # ── JavaScript ───────────────────────────────────────────────────────────
    print("[*] Récupération du JavaScript...")
    script_links = soup.find_all("script", src=True)
    js_urls      = [urljoin(base_url, tag["src"]) for tag in script_links if tag.get("src")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        js_results = list(executor.map(fetch_url, js_urls))

    all_js = [js for js in js_results if js]
    if all_js:
        script_tag        = soup.new_tag("script")
        script_tag.string = "\n".join(all_js)
        if soup.body:
            soup.body.append(script_tag)
        for tag in script_links:    # supprime les <script src="..."> externes
            tag.decompose()

    return soup.prettify()


# ─── Programme principal ───────────────────────────────────────────────────────
def phishing_main():
    user_agent = random.choice(USER_AGENTS)
    headers    = {"User-Agent": user_agent}
    print(f"[+] User-Agent sélectionné : {user_agent}\n")

    url = input("[?] URL du site cible -> ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # ── Récupération du HTML ──────────────────────────────────────────────────
    print("[*] Récupération du HTML...")
    try:
        session  = requests.Session()
        response = session.get(url, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"[!] Erreur de connexion : {e}")
        return

    if response.status_code != 200:
        print(f"[!] La requête a échoué (status {response.status_code}).")
        return

    # ── Nom du fichier à partir du <title> ────────────────────────────────────
    soup      = BeautifulSoup(response.text, "html.parser")
    raw_title = soup.title.string if soup.title else "Phishing"
    file_name = re.sub(r'[\\/:*?"<>|]', "-", raw_title).strip() + ".html"
    file_path = os.path.join(OUTPUT_DIR, file_name)

    # ── Inline CSS + JS puis sauvegarde ──────────────────────────────────────
    final_html = inline_css_and_js(response.text, url)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"\n[✓] Page clonée avec succès → {file_path}")

    # Log
    with open("logs.txt", "a") as fichier:
        fichier.write(
            f"------------------------------------\n"
            f"\n"
            f" [{time.strftime('%d-%m-%Y %H:%M:%S')}]     Phishing du site {url} \n"
            f"\n"
            f"------------------------------------\n"
            f"\n"
        )

phishing_main()