import os
import subprocess

def task_manager():
    try:
        print("📋 Liste des processus en cours :\n")

        # Windows
        if os.name == "nt":
            os.system("tasklist")
        else:
            os.system("ps aux")

        choix = input("\n❓ Voulez-vous arrêter un processus ? (y/n) : ").lower()

        if choix == "y":
            pid = input("Entrez le PID du processus à arrêter : ")

            if not pid.isdigit():
                print("[!] ❌ PID invalide.")
                return

            if os.name == "nt":
                os.system(f"taskkill /PID {pid} /F")
            else:
                os.system(f"kill -9 {pid}")

            print("[+] ✅ Processus terminé.")

    except Exception as e:
        print(f"[!] ❌ Erreur dans le gestionnaire de tâches : {e}")