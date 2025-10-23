# Guide de Démarrage Rapide - ARK Discord Bot

Ce guide vous permettra de démarrer rapidement avec le bot Discord ARK.

---

## Étape 1 : Configuration du Serveur API (sur le serveur ARK)

### Installation rapide

```bash
# 1. Copier les fichiers du serveur sur votre serveur ARK
cd /home/steam
mkdir ark-api-server
cd ark-api-server

# 2. Copier les fichiers depuis le dossier 'server' du projet
# (ark_api_server.py, requirements.txt, .env.example)

# 3. Installer les dépendances
pip3 install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
nano .env  # Éditez et définissez ARK_API_TOKEN avec un mot de passe fort
```

### Exemple de fichier `.env` pour le serveur

```bash
ARK_API_TOKEN=MonTokenSecretTresLong123456789
ARK_API_PORT=2603
ARKMANAGER_PATH=/usr/local/bin/arkmanager
```

### Démarrage manuel (pour tester)

```bash
# Charger les variables d'environnement
source load_env.sh

# Lancer le serveur
python3 ark_api_server.py
```

**Important** : Notez le token affiché au démarrage, vous en aurez besoin pour le bot.

### Ouvrir le port dans le pare-feu

```bash
# Avec ufw (Ubuntu)
sudo ufw allow 2603/tcp

# Ou avec iptables
sudo iptables -A INPUT -p tcp --dport 2603 -j ACCEPT
```

---

## Étape 2 : Configuration du Bot Discord

### Créer un Bot Discord

1.  Allez sur [https://discord.com/developers/applications](https://discord.com/developers/applications)
2.  Cliquez sur **"New Application"**
3.  Donnez un nom à votre application (ex: "ARK Server Manager")
4.  Allez dans l'onglet **"Bot"** → **"Add Bot"**
5.  Activez **"MESSAGE CONTENT INTENT"** dans "Privileged Gateway Intents"
6.  Copiez le **Token** du bot
7.  Allez dans **"OAuth2"** → **"URL Generator"**
    -   Cochez `bot`
    -   Cochez les permissions : `Send Messages`, `Embed Links`, `Read Messages/View Channels`
    -   Copiez l'URL générée et ouvrez-la dans votre navigateur pour inviter le bot sur votre serveur Discord

### Installation du bot

```bash
# 1. Sur la machine qui hébergera le bot (peut être n'importe où)
cd /home/ubuntu
mkdir ark-discord-bot
cd ark-discord-bot

# 2. Copier les fichiers depuis le dossier 'bot' du projet
# (discord_bot.py, requirements.txt, .env.example)

# 3. Installer les dépendances
pip3 install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
nano .env  # Éditez et remplissez toutes les valeurs
```

### Exemple de fichier `.env` pour le bot

```bash
DISCORD_BOT_TOKEN=VotreTokenDiscordIci
ARK_API_URL=http://123.45.67.89:2603
ARK_API_TOKEN=MonTokenSecretTresLong123456789
```

**Important** : `ARK_API_TOKEN` doit être **exactement le même** que celui du serveur API.

### Démarrage manuel (pour tester)

```bash
# Charger les variables d'environnement
source load_env.sh

# Lancer le bot
python3 discord_bot.py
```

---

## Étape 3 : Tester le Bot

Une fois le bot connecté à Discord, testez les commandes suivantes :

```
!ark help
!ark instances
!ark status main
!ark broadcast main Serveur en maintenance dans 10 minutes
```

Remplacez `main` par le nom de votre instance ARK.

---

## Étape 4 : Installation en tant que Service (Recommandé)

Pour que le serveur API et le bot se lancent automatiquement au démarrage du système :

### Pour le serveur API

```bash
# Éditer le fichier de service
sudo nano /etc/systemd/system/ark-api.service

# Contenu du fichier (adapter les chemins) :
[Unit]
Description=ARK API Server
After=network.target

[Service]
Type=simple
User=steam
WorkingDirectory=/home/steam/ark-api-server
EnvironmentFile=/home/steam/ark-api-server/.env
ExecStart=/usr/bin/python3 /home/steam/ark-api-server/ark_api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable ark-api.service
sudo systemctl start ark-api.service
sudo systemctl status ark-api.service
```

### Pour le bot Discord

```bash
# Même procédure, en adaptant le fichier ark-discord-bot.service
sudo cp ark-discord-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ark-discord-bot.service
sudo systemctl start ark-discord-bot.service
sudo systemctl status ark-discord-bot.service
```

---

## Commandes Utiles

### Gérer le service du serveur API

```bash
sudo systemctl start ark-api.service    # Démarrer
sudo systemctl stop ark-api.service     # Arrêter
sudo systemctl restart ark-api.service  # Redémarrer
sudo systemctl status ark-api.service   # Voir le statut
sudo journalctl -u ark-api.service -f   # Voir les logs en temps réel
```

### Gérer le service du bot Discord

```bash
sudo systemctl start ark-discord-bot.service
sudo systemctl stop ark-discord-bot.service
sudo systemctl restart ark-discord-bot.service
sudo systemctl status ark-discord-bot.service
sudo journalctl -u ark-discord-bot.service -f
```

---

## Dépannage

### Le bot ne se connecte pas à Discord

-   Vérifiez que `DISCORD_BOT_TOKEN` est correct dans le fichier `.env`.
-   Vérifiez que "MESSAGE CONTENT INTENT" est activé dans les paramètres du bot Discord.

### Le bot ne peut pas communiquer avec le serveur API

-   Vérifiez que le serveur API est en cours d'exécution : `sudo systemctl status ark-api.service`
-   Vérifiez que l'URL dans `ARK_API_URL` est correcte (IP publique + port).
-   Vérifiez que le port `2603` est ouvert dans le pare-feu du serveur de jeu.
-   Vérifiez que `ARK_API_TOKEN` est identique dans les deux fichiers `.env`.

### Les commandes arkmanager ne fonctionnent pas

-   Vérifiez que `ARKMANAGER_PATH` pointe vers le bon exécutable.
-   Testez manuellement sur le serveur : `arkmanager status @main`
-   Vérifiez les logs du serveur API : `sudo journalctl -u ark-api.service -f`

### Erreur "Token invalide"

-   Le `ARK_API_TOKEN` dans le fichier `.env` du bot doit être **exactement le même** que celui du serveur API.

---

## Support

Pour plus d'informations, consultez le fichier `README.md` complet du projet.

