if choix == 11:
    try:
        CheckMDP.generateur()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

elif choix == 12:
    try:
        VerifMDP.verifier()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

elif choix == 21:
    print("Fonctionnalité virus en développement...")

elif choix == 22:
    print("Outil DDoS désactivé pour des raisons légales.")

elif choix == 23:
    print("Générateur de fausse page HTML en développement...")

elif choix == 31:
    try:
        PingIP.ping()
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

elif choix == 32:
    print("Affichage des journaux réseau en cours...")

elif choix == 41:
    print("Basculer entre le mode sombre et clair...")

elif choix == 42:
    print("Choisissez votre langue : FR ou EN")

elif choix == 43:
    print("Fermeture du programme.")
    exit()

elif choix == 51:
    print("Documentation utilisateur :\n - Utilisez les numéros du menu pour accéder aux fonctionnalités.")

elif choix == 52:
    print("FAQ :\n - Q : Cette app est-elle légale ?\n - R : Cela dépend de l'utilisation. Utilisation éthique uniquement.")

elif choix == 53:
    print("Mentions légales & Avertissement d’usage :\n - Ce logiciel est fourni à titre éducatif uniquement.")

elif choix == 54:
    print("Informations RGPD :\n - Aucune donnée personnelle n’est stockée.")

else:
    print("Option invalide. Veuillez choisir un numéro valide.")

    
