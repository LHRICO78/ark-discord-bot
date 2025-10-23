# ARK Discord Bot & API Server

Bot Discord pour gérer un serveur ARK: Survival Evolved via une API REST sécurisée, conçu pour fonctionner avec [ARK Server Tools (arkmanager)](https://github.com/arkmanager/ark-server-tools).

---

## 📋 Prérequis

Ce bot nécessite que **[ARK Server Tools](https://github.com/arkmanager/ark-server-tools)** soit installé et fonctionnel sur votre serveur de jeu ARK. ARK Server Tools est un ensemble d'outils en Bash pour gérer des serveurs ARK: Survival Evolved sur Linux.

**Installation d'ARK Server Tools** : Suivez les instructions sur le dépôt officiel → https://github.com/arkmanager/ark-server-tools

---

## 🎯 Vue d'ensemble

Ce projet contient une solution complète pour gérer votre serveur ARK: Survival Evolved via un bot Discord. Il est composé de deux parties :

1.  **Serveur API (ARK API Server)** : Une application Flask qui s'exécute sur votre serveur de jeu ARK. Elle expose une API REST sécurisée par token pour exécuter les commandes `arkmanager`.
2.  **Bot Discord (ARK Discord Bot)** : Un bot Python qui interagit avec les utilisateurs sur Discord, reçoit les commandes, et communique avec le serveur API pour les exécuter.

Cette architecture a été choisie pour éviter d'exposer le port SSH de votre serveur de jeu, renforçant ainsi la sécurité.

---

## 🏗️ Architecture

```
   Utilisateur Discord          Bot Discord               Serveur de Jeu ARK
+---------------------+    +---------------------+    +-------------------------+
|                     |    |                     |    |                         |
|  Tape `!ark status` | -> | Reçoit la commande  | -> | Reçoit une requête API  |
|                     |    |                     |    | sur http://...:2603     |
|                     |    | Appelle l'API REST  |    |                         |
|                     |    | (POST /api/ark/status)|    | Exécute `arkmanager`    |
|                     |    |                     |    |                         |
|  Reçoit le statut   | <- | Reçoit la réponse   | <- | Renvoie la sortie       |
|  dans un embed      |    | de l'API            |    | de la commande (JSON)   |
|                     |    |                     |    |                         |
+---------------------+    +---------------------+    +-------------------------+
```

---

## ✨ Fonctionnalités

Le bot supporte les commandes suivantes :

-   `!ark help` : Affiche le message d'aide
-   `!ark status <instance>` : Affiche le statut détaillé du serveur
-   `!ark start <instance>` : Démarre le serveur
-   `!ark stop <instance>` : Arrête le serveur
-   `!ark restart <instance>` : Redémarre le serveur
-   `!ark backup <instance>` : Lance une sauvegarde du monde
-   `!ark broadcast <instance> <message>` : Envoie un message à tous les joueurs connectés
-   `!ark instances` : Liste toutes les instances `arkmanager` disponibles sur le serveur de jeu

---

## 📦 Installation

### Étape 0 : Installer ARK Server Tools (si ce n'est pas déjà fait)

**Sur votre serveur de jeu ARK**, installez ARK Server Tools en suivant la documentation officielle :

```bash
curl -sL https://raw.githubusercontent.com/arkmanager/ark-server-tools/master/netinstall.sh | sudo bash -s steam
```

Pour plus d'informations : https://github.com/arkmanager/ark-server-tools

Vérifiez que `arkmanager` fonctionne :

```bash
arkmanager status @main  # Remplacez 'main' par le nom de votre instance
```

---

### Partie 1 : Installation du Serveur API (sur le serveur de jeu ARK)

**Prérequis :**

*   Un serveur Linux (Ubuntu/Debian) avec `arkmanager` fonctionnel
*   Python 3.8+ et `pip`
*   Un port ouvert sur votre pare-feu (par défaut `2603`)

**Étapes :**

1.  **Clonez le projet** sur votre serveur de jeu, par exemple dans le répertoire home de votre utilisateur `steam` :
    ```bash
    git clone https://github.com/LHRICO78/ark-discord-bot.git /home/steam/ark-api-server
    cd /home/steam/ark-api-server/server
    ```

2.  **Installez les dépendances Python** :
    ```bash
    pip3 install -r requirements.txt
    ```

3.  **Configurez les variables d'environnement** :
    -   Copiez le fichier d'exemple :
        ```bash
        cp .env.example .env
        ```
    -   Éditez le fichier `.env` et configurez les variables :
        ```bash
        nano .env
        ```
        -   `ARK_API_TOKEN` : Définissez un mot de passe long et complexe. **C'est le secret qui protège votre API.**
        -   `ARK_API_PORT` : Laissez `2603` ou changez si nécessaire
        -   `ARKMANAGER_PATH` : Vérifiez que le chemin vers `arkmanager` est correct (généralement `/usr/local/bin/arkmanager`)

4.  **Testez le serveur manuellement** :
    ```bash
    source load_env.sh
    python3 ark_api_server.py
    ```
    Le serveur devrait démarrer et afficher le token API. Vous pouvez l'arrêter avec `Ctrl+C`.

5.  **(Optionnel mais recommandé) Installez en tant que service systemd** pour qu'il se lance automatiquement au démarrage :
    -   Éditez le fichier `ark-api.service` pour vérifier que les chemins (`WorkingDirectory`, `EnvironmentFile`, `ExecStart`) et l'utilisateur (`User`) sont corrects
    -   Copiez le fichier de service dans le répertoire systemd :
        ```bash
        sudo cp ark-api.service /etc/systemd/system/
        ```
    -   Rechargez systemd, activez et démarrez le service :
        ```bash
        sudo systemctl daemon-reload
        sudo systemctl enable ark-api.service
        sudo systemctl start ark-api.service
        ```
    -   Vérifiez son statut :
        ```bash
        sudo systemctl status ark-api.service
        ```

6.  **Ouvrez le port dans le pare-feu** :
    ```bash
    # Avec ufw (Ubuntu)
    sudo ufw allow 2603/tcp
    
    # Ou avec iptables
    sudo iptables -A INPUT -p tcp --dport 2603 -j ACCEPT
    ```

---

### Partie 2 : Installation du Bot Discord (sur n'importe quel serveur ou machine)

**Prérequis :**

*   Python 3.8+ et `pip`
*   Un token de bot Discord

**Étapes :**

1.  **Créez un Bot Discord** :
    -   Allez sur le [Portail des développeurs Discord](https://discord.com/developers/applications)
    -   Créez une nouvelle application
    -   Allez dans l'onglet "Bot", cliquez sur "Add Bot"
    -   Activez les **"Privileged Gateway Intents"** (`MESSAGE CONTENT INTENT`)
    -   Copiez le **token du bot**
    -   Invitez le bot sur votre serveur Discord en utilisant le "URL Generator" dans l'onglet "OAuth2" (avec les permissions `bot` et `Send Messages`, `Embed Links`)

2.  **Clonez le projet** sur la machine où le bot sera hébergé :
    ```bash
    git clone https://github.com/LHRICO78/ark-discord-bot.git /home/ubuntu/ark-discord-bot
    cd /home/ubuntu/ark-discord-bot/bot
    ```

3.  **Installez les dépendances Python** :
    ```bash
    pip3 install -r requirements.txt
    ```

4.  **Configurez les variables d'environnement** :
    -   Copiez le fichier d'exemple :
        ```bash
        cp .env.example .env
        ```
    -   Éditez le fichier `.env` et remplissez **toutes** les valeurs :
        ```bash
        nano .env
        ```
        -   `DISCORD_BOT_TOKEN` : Le token que vous avez copié à l'étape 1
        -   `ARK_API_URL` : L'adresse IP publique de votre serveur de jeu et le port configuré (ex: `http://123.45.67.89:2603`)
        -   `ARK_API_TOKEN` : Le **même token** que vous avez défini pour le serveur API

5.  **Testez le bot manuellement** :
    ```bash
    source load_env.sh
    python3 discord_bot.py
    ```
    Le bot devrait se connecter à Discord. Allez sur votre serveur et tapez `!ark help`.

6.  **(Optionnel mais recommandé) Installez en tant que service systemd** :
    -   Suivez la même procédure que pour le serveur API, en utilisant le fichier `ark-discord-bot.service` et en adaptant les chemins et l'utilisateur

---

## 🔒 Sécurité

-   **Ne partagez jamais vos tokens** (API et Discord)
-   Assurez-vous que le `ARK_API_TOKEN` est fort et unique
-   Configurez votre pare-feu sur le serveur de jeu pour n'autoriser les connexions sur le port `2603` (ou celui que vous avez choisi) que depuis l'adresse IP de la machine qui héberge le bot Discord. C'est une mesure de sécurité cruciale.

```bash
# Exemple avec ufw (Uncomplicated Firewall) sur Ubuntu
# Remplacer 1.2.3.4 par l'IP de votre bot
sudo ufw allow from 1.2.3.4 to any port 2603 proto tcp
```

---

## 📚 Documentation

-   **[GUIDE_RAPIDE.md](GUIDE_RAPIDE.md)** : Guide de démarrage rapide étape par étape
-   **[EXEMPLES_COMMANDES.md](EXEMPLES_COMMANDES.md)** : Exemples d'utilisation et scénarios pratiques

---

## 🔗 Liens utiles

-   **ARK Server Tools (arkmanager)** : https://github.com/arkmanager/ark-server-tools
-   **Documentation arkmanager** : https://github.com/arkmanager/ark-server-tools/blob/master/README.asciidoc
-   **Discord Developer Portal** : https://discord.com/developers/applications

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

---

## ⚠️ Avertissement

Ce projet n'est pas affilié à Studio Wildcard, Snail Games USA, ARK: Survival Evolved, ou au projet arkmanager. Il s'agit d'un outil tiers créé par la communauté pour faciliter la gestion des serveurs ARK.

