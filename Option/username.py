import requests
from Option.utils.display import ask, success, error, warning, info, result, separator

def username():

    pseudo = ask("Pseudo à rechercher")

    if not pseudo.strip():
        error("Le pseudo ne peut pas être vide.")
        return

    urls = [
        f"https://tiktok.com/@{pseudo}",
        f"https://instagram.com/{pseudo}",
        f"https://github.com/{pseudo}",
        f"https://youtube.com/@{pseudo}",
        f"https://x.com/{pseudo}",
        f"https://pinterest.com/{pseudo}",
        f"https://facebook.com/{pseudo}",
        f"https://linkedin.com/in/{pseudo}",
        f"https://snapchat.com/add/{pseudo}",
        f"https://reddit.com/u/{pseudo}",
        f"https://stackoverflow.com/users/{pseudo}",
        f"https://telegram.me/{pseudo}",
        f"https://flickr.com/people/{pseudo}",
        f"https://tumblr.com/blog/view/{pseudo}",
        f"https://vimeo.com/{pseudo}",
        f"https://steamcommunity.com/id/{pseudo}",
        f"https://soundcloud.com/{pseudo}",
        f"https://medium.com/@{pseudo}",
        f"https://behance.net/{pseudo}",
        f"https://dribbble.com/{pseudo}",
        f"https://gitlab.com/{pseudo}",
        f"https://twitch.tv/{pseudo}",
        f"https://dailymotion.com/{pseudo}",
        f"https://replit.com/@{pseudo}",
        f"https://bandcamp.com/{pseudo}",
    ]

    headers     = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    found_count = 0

    info(f"Recherche de '{pseudo}' sur {len(urls)} plateformes...")
    separator()

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
            if response.status_code == 200:
                success(f"Trouvé → {url}")
                found_count += 1
            elif response.status_code == 404:
                info(f"Absent  → {url}")
            else:
                warning(f"Statut {response.status_code} → {url}")
        except requests.exceptions.RequestException as e:
            error(f"Erreur  → {url} ({e})")

    separator()
    result("Plateformes testées", len(urls))
    result("Profils trouvés",     found_count)

    if found_count > 0:
        success(f"'{pseudo}' est présent sur {found_count} plateforme(s).")
    else:
        info(f"'{pseudo}' n'a été trouvé sur aucune plateforme.")
