import os
import shutil
import tempfile

def clean_temp():
    try:
        print("🧹 Nettoyage des fichiers temporaires...\n")

        temp_dirs = []

        # Dossier temp principal
        temp_dirs.append(tempfile.gettempdir())

        # Windows spécifique
        if os.name == "nt":
            temp_dirs.append("C:\\Windows\\Temp")

        total_deleted = 0

        for folder in temp_dirs:
            if not os.path.exists(folder):
                continue

            print(f"📂 Nettoyage : {folder}")

            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)

                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                        total_deleted += 1
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path, ignore_errors=True)
                        total_deleted += 1
                except Exception:
                    # Ignore les fichiers utilisés
                    continue

        print(f"\n✅ Nettoyage terminé : {total_deleted} éléments supprimés.")

    except Exception as e:
        print(f"❌ Erreur nettoyage : {e}")