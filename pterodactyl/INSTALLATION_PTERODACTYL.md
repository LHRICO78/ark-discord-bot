# Installation via Pterodactyl Panel

Ce guide vous explique comment installer le bot Discord ARK en utilisant Pterodactyl Panel.

---

## 📋 Prérequis

**Important** : Ce système nécessite que [ARK Server Tools (arkmanager)](https://github.com/arkmanager/ark-server-tools) soit installé sur votre serveur de jeu ARK.

Vous aurez besoin de :
- Un panel Pterodactyl fonctionnel
- Un serveur ARK avec arkmanager installé **sur la machine hôte** (pas dans un conteneur)
- Le serveur API ARK installé **sur la machine hôte** du serveur ARK
- Un token de bot Discord

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Machine Hôte (Serveur ARK)               │
│                                                             │
│  ┌──────────────┐      ┌─────────────────┐                │
│  │   Serveur    │ ───> │   Serveur API   │                │
│  │     ARK      │      │   (Port 2603)   │                │
│  │ (arkmanager) │      │  Installation   │                │
│  └──────────────┘      │    manuelle     │                │
│                        └─────────────────┘                │
│                               ▲                            │
└───────────────────────────────┼────────────────────────────┘
                                │
                          HTTP REST API
                                │
                                ▼
                   ┌────────────────────────┐
                   │   Bot Discord          │
                   │   (Pterodactyl Panel)  │
                   │   Installation via egg │
                   └────────────────────────┘
```

---

## 🥚 Fichier Egg Fourni

Un seul fichier egg est fourni dans le dossier `pterodactyl/` :

- **`egg-ark-discord-bot.json`** : Bot Discord (peut être installé sur n'importe quel node Pterodactyl)

---

## 📦 Installation

### Étape 1 : Installer le Serveur API sur la Machine Hôte

**Le serveur API doit être installé directement sur la machine hôte** où se trouve votre serveur ARK et arkmanager. **Il ne doit PAS être dans un conteneur Pterodactyl.**

**Sur la machine hôte de votre serveur ARK :**

```bash
# 1. Cloner le projet
cd /home/steam  # ou le répertoire de votre choix
git clone https://github.com/LHRICO78/ark-discord-bot.git
cd ark-discord-bot/server

# 2. Installer les dépendances Python
pip3 install -r requirements.txt

# 3. Configurer l'environnement
cp .env.example .env
nano .env
```

**Configurez le fichier `.env` :**

```bash
ARK_API_TOKEN=VotreTokenSecretTresLong123456789ABCDEF
ARK_API_PORT=2603
ARKMANAGER_PATH=/usr/local/bin/arkmanager
```

**Générez un token sécurisé** (minimum 32 caractères) :

```bash
# Exemple de génération de token
openssl rand -base64 32
```

**Installez le service systemd** :

```bash
# Éditer le fichier de service pour adapter les chemins
sudo nano ark-api.service

# Copier le service
sudo cp ark-api.service /etc/systemd/system/

# Activer et démarrer
sudo systemctl daemon-reload
sudo systemctl enable ark-api.service
sudo systemctl start ark-api.service

# Vérifier le statut
sudo systemctl status ark-api.service
```

**Ouvrir le port dans le pare-feu :**

```bash
sudo ufw allow 2603/tcp
```

**Notez le token API** affiché dans les logs au démarrage :

```bash
sudo journalctl -u ark-api.service -f
```

---

### Étape 2 : Importer l'Egg dans Pterodactyl

**En tant qu'administrateur du panel :**

1. Connectez-vous à votre panel Pterodactyl
2. Allez dans **Admin Area** → **Nests**
3. Créez un nouveau nest appelé "Bots" (ou utilisez un nest existant)
4. Dans le nest, cliquez sur **Import Egg**
5. Importez le fichier **`egg-ark-discord-bot.json`**

---

### Étape 3 : Créer le Bot Discord dans Pterodactyl

**Le bot Discord peut être installé sur n'importe quel node Pterodactyl.**

1. Créez un nouveau serveur dans Pterodactyl
2. Sélectionnez l'egg **"ARK Discord Bot"**
3. Configurez les paramètres :
   - **Nom** : ARK Discord Bot
   - **Node** : N'importe quel node
   - **Allocation** : Aucun port externe nécessaire (laissez par défaut)
   - **Mémoire** : 256 MB minimum
   - **CPU** : 50% minimum
   - **Stockage** : 200 MB minimum

4. Dans les **variables d'environnement** :
   - **Discord Bot Token** : Votre token de bot Discord (voir section suivante)
   - **ARK API URL** : `http://IP_MACHINE_HOTE:2603`
     - Remplacez `IP_MACHINE_HOTE` par l'IP de la machine hôte où tourne le serveur API
     - **Important** : Utilisez l'IP de la machine hôte, pas l'IP du conteneur Pterodactyl
   - **ARK API Token** : Le **même token** que celui configuré dans le serveur API
   - **Auto Update** : `1` (pour activer les mises à jour automatiques)

5. Démarrez le serveur

---

## 🤖 Créer un Bot Discord

Si vous n'avez pas encore de bot Discord :

1. Allez sur [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Cliquez sur **"New Application"**
3. Donnez un nom à votre application (ex: "ARK Server Manager")
4. Allez dans l'onglet **"Bot"** → **"Add Bot"**
5. Activez **"MESSAGE CONTENT INTENT"** dans "Privileged Gateway Intents"
6. Cliquez sur **"Reset Token"** et copiez le token
7. Allez dans **"OAuth2"** → **"URL Generator"**
   - Cochez `bot`
   - Cochez les permissions : `Send Messages`, `Embed Links`, `Read Messages/View Channels`
   - Copiez l'URL générée et ouvrez-la dans votre navigateur pour inviter le bot sur votre serveur Discord

---

## 🔧 Configuration Réseau

### Trouver l'IP de la Machine Hôte

Le bot Discord (dans Pterodactyl) doit pouvoir communiquer avec le serveur API (sur la machine hôte).

**Sur la machine hôte, trouvez l'IP :**

```bash
# IP locale
ip addr show

# Ou
hostname -I
```

**Utilisez cette IP dans `ARK_API_URL`** :
- Si le bot est sur le **même serveur physique** : Utilisez l'IP locale (ex: `192.168.1.100`)
- Si le bot est sur un **serveur distant** : Utilisez l'IP publique et ouvrez le port 2603 dans le pare-feu

### Sécurité Réseau

Pour renforcer la sécurité, limitez l'accès au port 2603 uniquement depuis l'IP du serveur Pterodactyl :

```bash
# Sur la machine hôte du serveur ARK
sudo ufw delete allow 2603/tcp
sudo ufw allow from IP_DU_PTERODACTYL to any port 2603 proto tcp
```

---

## 🎮 Utilisation

Une fois le serveur API et le bot démarrés, testez le bot sur Discord :

```
!ark help
!ark instances
!ark status main
```

Remplacez `main` par le nom de votre instance ARK.

---

## 🐛 Dépannage

### Le bot ne peut pas se connecter au serveur API

**Erreur** : `Impossible de se connecter au serveur ARK`

**Solutions** :

1. Vérifiez que le serveur API est démarré :
   ```bash
   sudo systemctl status ark-api.service
   ```

2. Testez la connexion depuis le conteneur Pterodactyl :
   ```bash
   # Dans la console du bot Pterodactyl
   curl http://IP_MACHINE_HOTE:2603/health
   ```

3. Vérifiez que l'IP dans `ARK_API_URL` est correcte (IP de la machine hôte, pas du conteneur)

4. Vérifiez que le port 2603 est ouvert :
   ```bash
   sudo ufw status
   ```

5. Vérifiez que `ARK_API_TOKEN` est identique dans les deux configurations

### Les commandes arkmanager ne fonctionnent pas

**Erreur** : `arkmanager: command not found`

**Solution** : Vérifiez que `ARKMANAGER_PATH` dans le fichier `.env` du serveur API pointe vers le bon exécutable :

```bash
# Sur la machine hôte
which arkmanager
```

### Le bot ne répond pas sur Discord

**Solutions** :

1. Vérifiez que `DISCORD_BOT_TOKEN` est correct
2. Vérifiez que "MESSAGE CONTENT INTENT" est activé dans les paramètres du bot Discord
3. Consultez les logs du bot dans la console Pterodactyl

---

## 📚 Ressources

- **Documentation complète** : [README.md](../README.md)
- **Guide rapide** : [GUIDE_RAPIDE.md](../GUIDE_RAPIDE.md)
- **Exemples de commandes** : [EXEMPLES_COMMANDES.md](../EXEMPLES_COMMANDES.md)
- **ARK Server Tools** : https://github.com/arkmanager/ark-server-tools
- **Pterodactyl Panel** : https://pterodactyl.io/

---

## 💡 Points Importants

✅ **Le serveur API est installé sur la machine hôte** (pas dans Pterodactyl)

✅ **Le bot Discord est installé via Pterodactyl** (avec l'egg fourni)

✅ **Pas de SSH nécessaire** : Communication via API REST HTTP

✅ **Le token API doit être identique** dans le serveur API et le bot Discord

✅ **Utilisez l'IP de la machine hôte** dans `ARK_API_URL`, pas l'IP du conteneur

