# Installation Pterodactyl Panel

Ce dossier contient les fichiers nécessaires pour installer le bot Discord ARK et le serveur API via Pterodactyl Panel.

## 📁 Fichiers

- **`egg-ark-api-server.json`** : Egg Pterodactyl pour le serveur API
- **`egg-ark-discord-bot.json`** : Egg Pterodactyl pour le bot Discord
- **`INSTALLATION_PTERODACTYL.md`** : Guide d'installation complet

## 🚀 Installation Rapide

1. Importez les deux eggs dans votre panel Pterodactyl (Admin Area → Nests → Import Egg)
2. Créez un serveur avec l'egg "ARK API Server" sur le node de votre serveur ARK
3. Créez un serveur avec l'egg "ARK Discord Bot" sur n'importe quel node
4. Configurez les variables d'environnement
5. Démarrez les deux serveurs

Pour les instructions détaillées, consultez **[INSTALLATION_PTERODACTYL.md](INSTALLATION_PTERODACTYL.md)**.

## ⚙️ Configuration Requise

### Serveur API
- **Mémoire** : 512 MB minimum
- **CPU** : 50% minimum
- **Stockage** : 100 MB minimum
- **Port** : 2603 (ou autre port disponible)
- **Prérequis** : Accès à `arkmanager`

### Bot Discord
- **Mémoire** : 256 MB minimum
- **CPU** : 50% minimum
- **Stockage** : 100 MB minimum
- **Port** : Aucun port externe nécessaire

## 🔑 Variables d'Environnement

### Serveur API
- `ARK_API_TOKEN` : Token d'authentification (minimum 32 caractères)
- `ARKMANAGER_PATH` : Chemin vers arkmanager (par défaut : `/usr/local/bin/arkmanager`)
- `AUTO_UPDATE` : Mise à jour automatique (1 = oui, 0 = non)

### Bot Discord
- `DISCORD_BOT_TOKEN` : Token du bot Discord
- `ARK_API_URL` : URL du serveur API (ex: `http://192.168.1.100:2603`)
- `ARK_API_TOKEN` : Token d'authentification (identique au serveur API)
- `AUTO_UPDATE` : Mise à jour automatique (1 = oui, 0 = non)

## 📝 Notes

- Le serveur API doit être installé sur le **même node** que votre serveur ARK
- Le bot Discord peut être installé sur **n'importe quel node**
- Le `ARK_API_TOKEN` doit être **identique** dans les deux serveurs
- Le serveur API doit avoir accès à la commande `arkmanager`

## 🆘 Support

Pour toute question ou problème, consultez :
- [INSTALLATION_PTERODACTYL.md](INSTALLATION_PTERODACTYL.md) - Guide complet
- [../README.md](../README.md) - Documentation principale
- [../GUIDE_RAPIDE.md](../GUIDE_RAPIDE.md) - Guide rapide
- [Issues GitHub](https://github.com/LHRICO78/ark-discord-bot/issues) - Signaler un bug

