
<div align="center">

```
    ███████╗ ██████╗ ██████╗ ██████╗ ██████╗ 
    ██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗
    █████╗  ██║     ██║   ██║██████╔╝██████╔╝
    ██╔══╝  ██║     ██║   ██║██╔══██╗██╔═══╝ 
    ███████╗╚██████╗╚██████╔╝██║  ██║██║     
    ╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     
```

# ECORP — Elite Cyber Operations & Research Platform

**Outil de cybersécurité éducatif tout-en-un · Python 3.11 · Windows**

[![Site Web](https://img.shields.io/badge/🌐_Site_Web-ecorp--site.vercel.app-00f5a0?style=for-the-badge)](https://ecorp-site.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/downloads/release/python-3110/)
[![Licence](https://img.shields.io/badge/Licence-GPL--2.0-orange?style=for-the-badge)](./LICENSE)
[![Plateforme](https://img.shields.io/badge/Plateforme-Windows_10%2F11-0078D4?style=for-the-badge&logo=windows)](https://github.com/juto222/Projet-Lyc-e)
[![Statut](https://img.shields.io/badge/Statut-Éducatif-purple?style=for-the-badge)](#)

> ⚠️ **Usage strictement éducatif.** Toute utilisation malveillante est illégale et passible de poursuites pénales (art. 323-1 du Code pénal français).

</div>

---

## 📌 Présentation

**ECORP** est un toolkit Python interactif développé dans le cadre d'un **projet de lycée**. Il regroupe plus de **25 outils** organisés en 7 catégories, couvrant les domaines de la cybersécurité, des réseaux, de la gestion de mots de passe et de l'analyse système.

L'interface s'exécute en terminal avec une navigation par numéros, disponible en **français et en anglais**, avec un prompt personnalisé affichant `utilisateur@machine $`.

🌐 **Site officiel & documentation complète : [ecorp-site.vercel.app](https://ecorp-site.vercel.app)**

---

## 🗂️ Fonctionnalités

### 🔐 [1x] Mot de passe
| Code | Outil | Description |
|------|-------|-------------|
| `11` | Générateur de MDP | Génère un mot de passe sécurisé aléatoire |
| `12` | Vérificateur de MDP | Analyse la robustesse d'un mot de passe |
| `13` | Quiz mot de passe | Quiz interactif (interface Flet) |
| `14` | MDP compromis | Vérifie via l'API Have I Been Pwned (k-anonymat SHA-1) |

### 🛡️ [2x] Pentest
| Code | Outil | Description |
|------|-------|-------------|
| `21` | DirBuster | Découverte de répertoires cachés par force brute |
| `22` | Fausse page HTML | Générateur de page de phishing (démonstration) |
| `23` | Keylogger | Capture de frappes locale avec interface graphique |
| `24` | Quiz sécurité | Quiz 3 niveaux : facile / moyen / difficile |
| `25` | Scanner de sites | Scan de sous-domaines |

### 📊 [3x] Réseau
| Code | Outil | Description |
|------|-------|-------------|
| `31` | Ping IP | Test de connectivité vers une IP ou un domaine |
| `32` | Scan réseau | Scan de ports via python-nmap |
| `33` | Journal / Logs | Affichage du fichier `logs.txt` |
| `34` | Quiz réseau | Quiz interactif sur les réseaux (Flet) |
| `35` | IP Lookup | Géolocalisation et infos sur une adresse IP |
| `36` | Speedtest | Test de débit Internet (montant/descendant) |

### 💻 [4x] PC & Système
| Code | Outil | Description |
|------|-------|-------------|
| `41` | Infos système | OS, CPU, RAM, stockage, réseau |
| `42` | Gestionnaire de tâches | Liste des processus actifs |
| `43` | Nettoyeur de fichiers temp. | Suppression des fichiers temporaires |
| `44` | Création de faux fichier | Génère un fichier leurre |

### 🧩 [5x] Autres
| Code | Outil | Description |
|------|-------|-------------|
| `51` | Recherche d'utilisateur | OSINT sur un pseudonyme |
| `52` | Gestionnaire de MDP | Ouvre le gestionnaire web |
| `53` | Chiffrement Python | Chiffre un fichier `.py` |
| `54` | Déchiffrement Python | *(à venir)* |
| `55` | Console interactive | Terminal intégré |

### ⚙️ [6x] Paramètres
| Code | Option |
|------|--------|
| `61` | Mode sombre / clair |
| `62` | Langue (FR / EN) |
| `63` | Quitter |

---

## ⚙️ Installation

### Prérequis

- **Python 3.11** exactement → [Télécharger](https://www.python.org/downloads/release/python-3110/)
- **Windows 10 ou 11** (64 bits)
- **Nmap** installé sur le système → [nmap.org](https://nmap.org) *(requis pour le scan réseau)*
- Connexion Internet *(pour HIBP, IP Lookup, Speedtest)*
- Droits administrateur recommandés

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/juto222/Projet-Lyc-e.git
cd Projet-Lyc-e

# 2. Installer les dépendances (Windows)
setup.bat

# 3. Lancer l'outil
python main.py
```

Le script `setup.bat` installe automatiquement :

```
requests  pynput  customtkinter  colorama  psutil
internetspeedtest  clipboard  Pillow  dnspython
bs4  aiohttp  python-nmap  flet  cx_Freeze
pyarmor  nuitka
```

---

## 🖥️ Utilisation

```
🌐 Choisissez votre langue / Choose your language (FR/EN) : FR

utilisateur@machine $ 11     → Lance le générateur de mot de passe
utilisateur@machine $ 32     → Lance le scan réseau
utilisateur@machine $ 63     → Quitte le programme
```

Le prompt affiche `#` si vous êtes administrateur, `$` sinon.

Après chaque outil, appuyez sur **Entrée** pour revenir au menu principal.

---

## 📁 Structure du projet

```
Projet-Lyc-e/
├── main.py                  # Point d'entrée principal
├── setup.bat                # Script d'installation des dépendances
├── logs.txt                 # Journal des activités
├── LICENSE                  # Licence GPL-2.0
└── Option/
    ├── CheckMDP.py          # Vérificateur de mot de passe
    ├── GenererMDP.py        # Générateur de mot de passe
    ├── PingIP.py            # Ping
    ├── Scan.py              # Scan réseau Nmap
    ├── keylog.py            # Keylogger éducatif
    ├── phishing.py          # Générateur de fausse page HTML
    ├── dirbuster.py         # DirBuster
    ├── iplookup.py          # IP Lookup
    ├── subdomain.py         # Scanner de sous-domaines
    ├── username.py          # OSINT pseudonyme
    ├── crypt.py             # Chiffrement de fichier Python
    ├── console.py           # Console interactive
    ├── taskmanager.py       # Gestionnaire de tâches
    ├── si.py                # Informations système
    ├── test_speed.py        # Speedtest
    ├── tmp.py               # Nettoyeur temp
    ├── script.py            # Création faux fichier
    ├── pswd.py              # Mots de passe compromis (HIBP)
    ├── quizzmdp.py          # Quiz mot de passe (Flet)
    ├── quizznetwork.py      # Quiz réseau (Flet)
    ├── quizzsecurity.py     # Quiz sécurité (Flet)
    ├── password_manager.py  # Gestionnaire de mots de passe
    └── modules/
        ├── network/
        │   ├── networkinfo.py
        │   └── porthammer.py
        └── payload/
            ├── clipboard.py
            ├── dirlist.py
            ├── filegrab.py
            ├── keybcontrol.py
            ├── screenshot.py
            ├── shutdown.py
            └── ...
```

---

## 🔒 RGPD & Confidentialité

ECORP s'exécute **entièrement en local**. Aucune donnée personnelle n'est collectée par l'éditeur.

| Module | Envoi distant | Destinataire |
|--------|--------------|--------------|
| MDP Compromis | ✅ Hash SHA-1 partiel (5 chars) | Have I Been Pwned |
| IP Lookup | ✅ IP interrogée | API géolocalisation publique |
| Speedtest | ✅ IP publique | Speedtest.net |
| OSINT Utilisateur | ✅ Pseudonyme | Plateformes web publiques |
| Tous les autres | ❌ Aucun | — |

---

## ⚖️ Mentions légales

Ce projet est distribué sous **licence GPL-2.0**. Il est fourni à titre éducatif uniquement.

- ✅ Utilisation autorisée sur vos propres systèmes ou en environnement de test
- ❌ Toute utilisation sur des systèmes tiers sans autorisation est **illégale**
- ❌ Le keylogger ne doit jamais être installé sans consentement explicite
- ❌ La page de phishing ne doit jamais cibler de véritables utilisateurs

> Infractions sanctionnées par les **articles 323-1 à 323-8 du Code pénal français**.

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

1. Forkez le dépôt
2. Créez une branche (`git checkout -b feature/mon-outil`)
3. Committez vos changements (`git commit -m 'Ajout de mon-outil'`)
4. Pushez (`git push origin feature/mon-outil`)
5. Ouvrez une Pull Request

---

## 📄 Licence

Distribué sous licence **GNU General Public License v2.0**.  
Voir le fichier [LICENSE](./LICENSE) pour les termes complets.

---

<div align="center">

**[🌐 Site Web](https://ecorp-site.vercel.app) · [📦 Télécharger](https://github.com/juto222/Projet-Lyc-e/archive/refs/heads/main.zip) · [🐛 Signaler un bug](https://github.com/juto222/Projet-Lyc-e/issues)**

*Projet scolaire open-source · 2026*

</div>
