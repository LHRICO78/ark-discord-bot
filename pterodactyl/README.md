# Installation Pterodactyl Panel

Ce dossier contient le fichier egg nécessaire pour installer le bot Discord ARK via Pterodactyl Panel.

---

## 📁 Fichiers

- **`egg-ark-discord-bot.json`** : Egg Pterodactyl pour le bot Discord
- **`INSTALLATION_PTERODACTYL.md`** : Guide d'installation complet

---

## 🏗️ Architecture

Le système fonctionne en deux parties :

**Serveur API** → Installé **directement sur la machine hôte** du serveur ARK (installation manuelle)

**Bot Discord** → Installé **via Pterodactyl Panel** (avec l'egg fourni)

**Communication** → API REST HTTP (port 2603) - **Pas de SSH nécessaire**

---

## 🚀 Installation Rapide

### 1. Installer le Serveur API (sur la machine hôte)

Sur la machine où se trouve votre serveur ARK avec arkmanager :

```bash
cd /home/steam
git clone https://github.com/LHRICO78/ark-discord-bot.git
cd ark-discord-bot/server
pip3 install -r requirements.txt
cp .env.example .env
nano .env  # Configurez ARK_API_TOKEN, ARK_API_PORT, ARKMANAGER_PATH
```

Installez le service systemd :

```bash
sudo cp ark-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ark-api.service
sudo systemctl start ark-api.service
```

Ouvrez le port :

```bash
sudo ufw allow 2603/tcp
```

### 2. Installer le Bot Discord (via Pterodactyl)

Dans votre panel Pterodactyl :

1. Importez l'egg `egg-ark-discord-bot.json` (Admin Area → Nests → Import Egg)
2. Créez un nouveau serveur avec l'egg "ARK Discord Bot"
3. Configurez les variables d'environnement :
   - `DISCORD_BOT_TOKEN` : Token de votre bot Discord
   - `ARK_API_URL` : `http://IP_MACHINE_HOTE:2603`
   - `ARK_API_TOKEN` : Le même token que le serveur API
4. Démarrez le serveur

Pour les instructions détaillées, consultez **[INSTALLATION_PTERODACTYL.md](INSTALLATION_PTERODACTYL.md)**.

---

## ⚙️ Configuration Requise

### Serveur API (Machine Hôte)
- **Système** : Ubuntu/Debian avec arkmanager
- **Python** : 3.8+
- **Port** : 2603 (configurable)
- **Mémoire** : 512 MB minimum

### Bot Discord (Pterodactyl)
- **Mémoire** : 256 MB minimum
- **CPU** : 50% minimum
- **Stockage** : 200 MB minimum
- **Port** : Aucun port externe nécessaire

---

## 🔑 Variables d'Environnement

### Serveur API (fichier .env sur la machine hôte)
```bash
ARK_API_TOKEN=VotreTokenSecretTresLong123456789
ARK_API_PORT=2603
ARKMANAGER_PATH=/usr/local/bin/arkmanager
```

### Bot Discord (variables Pterodactyl)
- `DISCORD_BOT_TOKEN` : Token du bot Discord
- `ARK_API_URL` : URL du serveur API (ex: `http://192.168.1.100:2603`)
- `ARK_API_TOKEN` : Token d'authentification (identique au serveur API)
- `AUTO_UPDATE` : Mise à jour automatique (1 = oui, 0 = non)

---

## ⚠️ Points Importants

**Le serveur API ne peut PAS être installé dans un conteneur Pterodactyl** car il doit avoir accès direct à la commande `arkmanager` sur la machine hôte.

**Seul le bot Discord utilise Pterodactyl.** Le serveur API est installé manuellement sur la machine hôte.

**Pas de SSH nécessaire.** La communication se fait via API REST HTTP sur le port 2603.

Le `ARK_API_TOKEN` doit être **identique** dans le serveur API et le bot Discord.

Utilisez l'**IP de la machine hôte** dans `ARK_API_URL`, pas l'IP du conteneur Pterodactyl.

---

## 🆘 Support

Pour toute question ou problème, consultez :
- [INSTALLATION_PTERODACTYL.md](INSTALLATION_PTERODACTYL.md) - Guide complet
- [../README.md](../README.md) - Documentation principale
- [../GUIDE_RAPIDE.md](../GUIDE_RAPIDE.md) - Guide rapide
- [Issues GitHub](https://github.com/LHRICO78/ark-discord-bot/issues) - Signaler un bug

