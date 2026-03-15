from colorama import init, Fore, Style
import webbrowser  
import os 


init(autoreset=True)


def afficher_menu_phishing(langue_actuelle):
   
    def menu_fr():
        print(f"""{Fore.CYAN}{Style.BRIGHT}
{Fore.MAGENTA}  🌐 Générateur de fausse page HTML



{Fore.YELLOW}              [1] TikTok
              [2] Instagram (En cours de maintenance)
              [3] Facebook   
              [4] Google (En cours de maintenance)
              [5] Netflix
              [6] PayPal
              [7] Amazon
              [8] Twitter (X) (En cours de maintenance)
              [9] LinkedIn
              [10] Snapchat
              [12] Retour au menu principal

        
""")
    
    def menu_en():
        print(f"""{Fore.CYAN}{Style.BRIGHT}
              {Fore.MAGENTA}  🌐 Fake HTML Page Generator


{Fore.YELLOW}              [1] TikTok
              [2] Instagram (Under maintenance)
              [3] Facebook   
              [4] Google (Under maintenance)
              [5] Netflix
              [6] PayPal
              [7] Amazon
              [8] Twitter (X) (Under maintenance)
              [9] LinkedIn
              [10] Snapchat
              [12] Back to main menu
              """)
    
    if langue_actuelle == "FR":
        menu_fr()
    else:
        menu_en()

    choix_local = int(input(Fore.CYAN + ("Enter choice: " if langue_actuelle == "EN" else "Entrez votre choix : ")))
    
    
    def tiktok():
        # Chemin vers le fichier HTML
        chemin_fichier = "Option/page/Tiktok.html"
        
        # Vérifier si le fichier existe
        if os.path.exists(chemin_fichier):
            # Ouvrir le fichier dans le navigateur par défaut
            chemin_complet = os.path.abspath(chemin_fichier)  # Chemin absolu
            webbrowser.open('file://' + chemin_complet)
            
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ TikTok page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page TikTok ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def instagram():
        chemin_fichier = "Option/page/Instagram.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Instagram page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Instagram ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")
    
    def facebook():
        chemin_fichier = "Option/page/Facebook.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Facebook page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Facebook ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def google():
        chemin_fichier = "Option/page/Google.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Google page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Google ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")
    
    def netflix():
        chemin_fichier = "Option/page/Netflix.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Netflix page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Netflix ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def paypal():
        chemin_fichier = "Option/page/PayPal.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ PayPal page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page PayPal ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def amazon():
        chemin_fichier = "Option/page/Amazon.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Amazon page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Amazon ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def twitter():
        chemin_fichier = "Option/page/Twitter.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Twitter page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Twitter ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def linkedin():
        chemin_fichier = "Option/page/LinkedIn.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ LinkedIn page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page LinkedIn ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

    def snapchat(): 
        chemin_fichier = "Option/page/Snapchat.html"
        if os.path.exists(chemin_fichier):
            chemin_complet = os.path.abspath(chemin_fichier)
            webbrowser.open('file://' + chemin_complet)
            if langue_actuelle == "EN":
                print(Fore.GREEN + "✅ Snapchat page opened in browser!")
            else:
                print(Fore.GREEN + "✅ Page Snapchat ouverte dans le navigateur !")
        else:
            if langue_actuelle == "EN":
                print(Fore.RED + f"❌ Error: File not found at {chemin_fichier}")
            else:
                print(Fore.RED + f"❌ Erreur : Fichier introuvable à {chemin_fichier}")

        

    if choix_local == 1:
        try:
            tiktok()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 2:
        try:
            instagram()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 3:
        try:
            facebook()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 4:
        try:
            google()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 5:
        try:
            netflix()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 6:
        try:
            paypal()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 7:
        try:
            amazon()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 8:
        try:
            twitter()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 9:
        try:
            linkedin()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 10:
        try:
            snapchat()
        except Exception as e:
            print(Fore.RED + f"❌ Error: {e}" if langue_actuelle == "EN" else f"❌ Erreur : {e}")
        finally:
            input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))
    elif choix_local == 12:
        return  # Retour au menu principal
    else:
        print(Fore.RED + ("❌ Invalid choice!" if langue_actuelle == "EN" else "❌ Choix invalide !"))
        input(Fore.GREEN + ("Press Enter to continue..." if langue_actuelle == "EN" else "Appuyez sur Entrée pour continuer..."))