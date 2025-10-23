# Installation via Pterodactyl Panel

Ce guide vous explique comment installer le bot Discord ARK et le serveur API en utilisant Pterodactyl Panel.

---

## 📋 Prérequis

**Important** : Ce système nécessite que [ARK Server Tools (arkmanager)](https://github.com/arkmanager/ark-server-tools) soit installé sur votre serveur de jeu ARK.

Vous aurez besoin de :
- Un panel Pterodactyl fonctionnel
- Accès administrateur au panel
- Un serveur ARK avec arkmanager installé
- Un token de bot Discord

---

## 🥚 Fichiers Egg Fournis

Deux fichiers egg sont fournis dans le dossier `pterodactyl/` :

1. **`egg-ark-api-server.json`** : Serveur API (à installer sur le node où se trouve votre serveur ARK)
2. **`egg-ark-discord-bot.json`** : Bot Discord (peut être installé sur n'importe quel node)

---

## 📦 Installation

### Étape 1 : Importer les Eggs dans Pterodactyl

**En tant qu'administrateur du panel :**

1. Connectez-vous à votre panel Pterodactyl
2. Allez dans **Admin Area** → **Nests** → **Create New** (ou utilisez un nest existant)
3. Créez un nouveau nest appelé "ARK Management" (ou utilisez un nest existant)
4. Dans le nest, cliquez sur **Import Egg**
5. Importez les deux fichiers :
   - `egg-ark-api-server.json`
   - `egg-ark-discord-bot.json`

### Étape 2 : Créer le Serveur API

**Important** : Le serveur API doit être créé sur le **même node** que votre serveur ARK, car il doit avoir accès à la commande `arkmanager`.

1. Créez un nouveau serveur dans Pterodactyl
2. Sélectionnez l'egg **"ARK API Server"**
3. Configurez les paramètres :
   - **Nom** : ARK API Server
   - **Node** : Le même node que votre serveur ARK
   - **Allocation** : Choisissez le port 2603 (ou un autre port disponible)
   - **Mémoire** : 512 MB minimum
   - **CPU** : 50% minimum

4. Dans les **variables d'environnement** :
   - **ARK API Token** : Générez un token sécurisé (minimum 32 caractères)
     - Exemple : `MonTokenSecretTresLong123456789ABCDEF`
   - **ARKManager Path** : `/usr/local/bin/arkmanager` (ou le chemin où arkmanager est installé)
   - **Auto Update** : `1` (pour activer les mises à jour automatiques)

5. Démarrez le serveur
6. **Notez le token API** affiché dans la console au démarrage

### Étape 3 : Créer le Bot Discord

**Le bot Discord peut être installé sur n'importe quel node.**

1. Créez un nouveau serveur dans Pterodactyl
2. Sélectionnez l'egg **"ARK Discord Bot"**
3. Configurez les paramètres :
   - **Nom** : ARK Discord Bot
   - **Node** : N'importe quel node
   - **Allocation** : Aucun port externe nécessaire
   - **Mémoire** : 256 MB minimum
   - **CPU** : 50% minimum

4. Dans les **variables d'environnement** :
   - **Discord Bot Token** : Votre token de bot Discord (voir section suivante)
   - **ARK API URL** : `http://IP_DU_SERVEUR_API:2603`
     - Remplacez `IP_DU_SERVEUR_API` par l'IP du node où tourne le serveur API
     - Utilisez le port que vous avez configuré pour le serveur API
   - **ARK API Token** : Le **même token** que celui du serveur API
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

## 🔧 Configuration Avancée

### Accès à arkmanager depuis le conteneur Pterodactyl

**Important** : Le serveur API doit pouvoir exécuter la commande `arkmanager`. Si arkmanager est installé sur l'hôte et non dans le conteneur, vous devrez :

**Option 1 : Monter arkmanager dans le conteneur**

Ajoutez un mount dans la configuration du node Pterodactyl :

```json
{
  "source": "/usr/local/bin/arkmanager",
  "target": "/usr/local/bin/arkmanager",
  "read_only": true
}
```

**Option 2 : Installer arkmanager dans le conteneur**

Modifiez le script d'installation de l'egg pour installer arkmanager :

```bash
# Dans le script d'installation
curl -sL https://raw.githubusercontent.com/arkmanager/ark-server-tools/master/netinstall.sh | bash -s steam
```

**Option 3 : Utiliser un wrapper SSH**

Si arkmanager est sur une autre machine, vous pouvez créer un wrapper qui exécute les commandes via SSH.

### Sécurité

Pour renforcer la sécurité, configurez le pare-feu du serveur API pour n'accepter que les connexions depuis l'IP du bot Discord :

```bash
# Sur l'hôte du serveur API
sudo ufw allow from IP_DU_BOT to any port 2603 proto tcp
```

---

## 🎮 Utilisation

Une fois les deux serveurs démarrés, testez le bot sur Discord :

```
!ark help
!ark instances
!ark status main
```

Remplacez `main` par le nom de votre instance ARK.

---

## 🐛 Dépannage

### Le serveur API ne démarre pas

- Vérifiez que le fichier `.env` existe et est correctement configuré
- Vérifiez les logs du serveur dans la console Pterodactyl
- Assurez-vous que `ARKMANAGER_PATH` pointe vers le bon exécutable

### Le bot ne peut pas se connecter au serveur API

- Vérifiez que `ARK_API_URL` contient la bonne IP et le bon port
- Vérifiez que `ARK_API_TOKEN` est identique dans les deux serveurs
- Testez la connexion manuellement :
  ```bash
  curl -H "Authorization: Bearer VotreToken" http://IP:2603/health
  ```

### Les commandes arkmanager ne fonctionnent pas

- Vérifiez que arkmanager est accessible depuis le conteneur
- Testez manuellement dans la console du serveur API :
  ```bash
  /usr/local/bin/arkmanager status @main
  ```
- Vérifiez les permissions d'exécution

### Le bot ne répond pas sur Discord

- Vérifiez que `DISCORD_BOT_TOKEN` est correct
- Vérifiez que "MESSAGE CONTENT INTENT" est activé dans les paramètres du bot Discord
- Vérifiez les logs du bot dans la console Pterodactyl

---

## 📚 Ressources

- **Documentation complète** : [README.md](../README.md)
- **Guide rapide** : [GUIDE_RAPIDE.md](../GUIDE_RAPIDE.md)
- **Exemples de commandes** : [EXEMPLES_COMMANDES.md](../EXEMPLES_COMMANDES.md)
- **ARK Server Tools** : https://github.com/arkmanager/ark-server-tools
- **Pterodactyl Panel** : https://pterodactyl.io/

---

## 💡 Conseils

- **Mises à jour automatiques** : Laissez `AUTO_UPDATE=1` pour que les serveurs se mettent à jour automatiquement depuis GitHub
- **Logs** : Consultez régulièrement les logs dans la console Pterodactyl pour détecter les problèmes
- **Sauvegarde** : Sauvegardez régulièrement votre configuration (fichier `.env`)
- **Token sécurisé** : Utilisez un générateur de mots de passe pour créer un `ARK_API_TOKEN` fort

---

## ⚠️ Notes Importantes

1. Le serveur API **doit** avoir accès à `arkmanager`
2. Le `ARK_API_TOKEN` **doit** être identique dans les deux serveurs
3. Le serveur API **doit** être accessible depuis le bot Discord (vérifiez les pare-feu)
4. Le bot Discord nécessite l'intent "MESSAGE CONTENT" activé

