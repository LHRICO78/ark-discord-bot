# 🚨 Guide de résolution rapide - Erreur Token Discord

## Le problème

Votre bot Discord ne démarre pas et affiche l'erreur :
```
discord.errors.LoginFailure: Improper token has been passed.
```

## La solution en 3 étapes

### ✅ Étape 1 : Obtenir un token Discord valide

1. Allez sur **https://discord.com/developers/applications**
2. Connectez-vous avec votre compte Discord
3. Sélectionnez votre application (ou créez-en une si nécessaire)
4. Cliquez sur **"Bot"** dans le menu de gauche
5. Dans la section **"TOKEN"**, cliquez sur **"Reset Token"** (ou "Copy" si c'est la première fois)
6. **Copiez le token complet** qui s'affiche (vous ne pourrez le voir qu'une seule fois)

> ⚠️ **Le token ressemble à ça :** Une longue chaîne de caractères d'environ 70 caractères composée de lettres, chiffres et points

### ✅ Étape 2 : Configurer le token dans Pterodactyl

1. Connectez-vous à votre **Panel Pterodactyl**
2. Sélectionnez votre serveur **"ARK Discord Bot"**
3. Cliquez sur l'onglet **"Startup"** (ou "Démarrage")
4. Trouvez la variable **"Discord Bot Token"** ou **"DISCORD_BOT_TOKEN"**
5. **Collez votre token** dans le champ (sans espaces avant/après)
6. Cliquez sur **"Save"** ou **"Enregistrer"**

### ✅ Étape 3 : Redémarrer le bot

1. Retournez à l'onglet **"Console"**
2. Cliquez sur **"Restart"** (ou "Redémarrer")
3. Attendez quelques secondes
4. Vous devriez voir dans les logs :
   ```
   INFO - Démarrage du bot Discord ARK...
   INFO - Bot connecté en tant que VotreBot#1234
   ```

## 🎯 Vérifications supplémentaires

Si le problème persiste, vérifiez également :

### Dans le Discord Developer Portal

- [ ] Le bot est **activé** (toggle "Bot" sur ON)
- [ ] Les **Privileged Gateway Intents** sont activés :
  - ✅ **Message Content Intent** (obligatoire)
  - ✅ **Server Members Intent** (recommandé)
  - ✅ **Presence Intent** (optionnel)

### Dans Pterodactyl

- [ ] Les 3 variables sont remplies :
  - **DISCORD_BOT_TOKEN** : Votre token Discord
  - **ARK_API_URL** : L'URL de votre API ARK (ex: `http://123.45.67.89:2603`)
  - **ARK_API_TOKEN** : Le token de votre API ARK
- [ ] Aucune variable ne contient d'espaces avant/après
- [ ] Le fichier `.env` existe dans le File Manager (il est créé automatiquement par l'egg)

## 🔍 Comment vérifier si ça fonctionne ?

Dans la console Pterodactyl, vous devriez voir :

```
✅ SUCCÈS :
2025-10-23 16:09:11 INFO - Démarrage du bot Discord ARK...
2025-10-23 16:09:11 INFO - Préfixe des commandes: !
2025-10-23 16:09:12 INFO - Bot connecté en tant que VotreBot#1234
2025-10-23 16:09:12 INFO - Bot prêt !
```

```
❌ ÉCHEC :
discord.errors.LoginFailure: Improper token has been passed.
```

## 📞 Besoin d'aide ?

Si le problème persiste après avoir suivi toutes ces étapes :

1. Vérifiez que votre bot Discord est bien **invité sur votre serveur Discord**
2. Assurez-vous que le **serveur API ARK** est bien démarré et accessible
3. Consultez le fichier **SOLUTION_ERREUR.md** pour plus de détails
4. Vérifiez les logs complets dans la console Pterodactyl

## 🔗 Liens utiles

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Guide d'installation complet](pterodactyl/INSTALLATION_PTERODACTYL.md)
- [Documentation du projet](README.md)

