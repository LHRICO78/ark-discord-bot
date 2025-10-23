# Solution à l'erreur "Improper token has been passed"

## 🔍 Diagnostic

L'erreur que vous rencontrez est la suivante :

```
discord.errors.LoginFailure: Improper token has been passed.
```

Cette erreur signifie que le **token Discord** configuré dans votre fichier `.env` est **invalide** ou **mal formaté**.

## 🎯 Causes possibles

1. **Le fichier `.env` n'existe pas** dans le dossier `/home/container/` de votre serveur Pterodactyl
2. **Le token Discord est incorrect** (copié partiellement, avec des espaces, ou expiré)
3. **La variable d'environnement n'est pas chargée correctement** dans Pterodactyl
4. **Le token a été régénéré** sur le portail Discord Developer et l'ancien n'est plus valide

## ✅ Solution

### Étape 1 : Vérifier votre token Discord

1. Rendez-vous sur le **[Discord Developer Portal](https://discord.com/developers/applications)**
2. Sélectionnez votre application (bot)
3. Allez dans l'onglet **"Bot"**
4. Si nécessaire, cliquez sur **"Reset Token"** pour générer un nouveau token
5. **Copiez le token complet** (une longue chaîne d'environ 70 caractères)

⚠️ **Important** : Le token ne peut être copié qu'une seule fois après sa génération. Si vous le perdez, vous devrez le régénérer.

### Étape 2 : Configurer le fichier .env dans Pterodactyl

Puisque vous utilisez Pterodactyl Panel, il y a **deux méthodes** pour configurer les variables d'environnement :

#### Méthode A : Via les variables d'environnement Pterodactyl (RECOMMANDÉ)

1. Connectez-vous à votre **Panel Pterodactyl**
2. Allez dans votre serveur **ark-discord-bot**
3. Cliquez sur l'onglet **"Startup"** (Démarrage)
4. Vous devriez voir les variables suivantes :
   - `DISCORD_BOT_TOKEN`
   - `ARK_API_URL`
   - `ARK_API_TOKEN`
5. Remplissez ces variables avec vos vraies valeurs :
   - **DISCORD_BOT_TOKEN** : Votre token Discord complet (sans espaces)
   - **ARK_API_URL** : L'URL de votre API ARK (ex: `http://123.456.789.012:2603`)
   - **ARK_API_TOKEN** : Le token d'authentification de votre API ARK
6. Cliquez sur **"Save"** ou **"Enregistrer"**
7. **Redémarrez le serveur**

#### Méthode B : Via le fichier .env (ALTERNATIVE)

Si les variables d'environnement ne sont pas configurées dans l'egg Pterodactyl :

1. Dans le **File Manager** de Pterodactyl, créez un fichier `.env` à la racine
2. Copiez le contenu de `.env.example` :

```env
# Configuration du bot Discord ARK
# Copiez ce fichier en .env et remplissez les valeurs

# Token du bot Discord (obtenu depuis https://discord.com/developers/applications)
DISCORD_BOT_TOKEN=votre_token_discord_ici

# URL de l'API ARK Server (adresse IP ou nom de domaine + port)
ARK_API_URL=http://123.456.789.012:2603

# Token d'authentification pour l'API (même que celui du serveur)
ARK_API_TOKEN=votre_token_secret_ici
```

3. Remplacez les valeurs par vos vraies informations
4. **Enregistrez le fichier**
5. **Redémarrez le serveur**

### Étape 3 : Vérifier le format du token

Assurez-vous que votre token Discord :

- ✅ Ne contient **aucun espace** avant ou après
- ✅ Est copié **en entier** (environ 70 caractères)
- ✅ N'a **pas de guillemets** autour (sauf dans le fichier .env)
- ✅ Est **récent** et non régénéré depuis

### Étape 4 : Tester le démarrage

1. Redémarrez votre serveur dans Pterodactyl
2. Consultez les logs dans la console
3. Vous devriez voir :
   ```
   2025-10-23 16:09:11 INFO discord.client logging in using static token
   ```
   Suivi de la connexion réussie du bot

## 🚨 Erreurs courantes

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Improper token has been passed` | Token invalide ou mal formaté | Vérifier et copier à nouveau le token |
| `DISCORD_BOT_TOKEN n'est pas défini !` | Variable d'environnement manquante | Configurer la variable dans Pterodactyl Startup |
| `401 Unauthorized` | Token expiré ou régénéré | Régénérer un nouveau token sur Discord Developer Portal |

## 📝 Checklist de vérification

- [ ] J'ai vérifié que mon token Discord est valide sur le Developer Portal
- [ ] J'ai copié le token complet sans espaces
- [ ] J'ai configuré les variables d'environnement dans Pterodactyl (onglet Startup)
- [ ] J'ai redémarré le serveur après la configuration
- [ ] J'ai vérifié les logs pour confirmer la connexion

## 🔗 Ressources utiles

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Documentation Discord.py](https://discordpy.readthedocs.io/)
- [Guide d'installation Pterodactyl du projet](pterodactyl/INSTALLATION_PTERODACTYL.md)

---

Si le problème persiste après avoir suivi ces étapes, vérifiez que :
1. Votre bot Discord est bien **activé** dans le Developer Portal
2. Les **intents** nécessaires sont activés (Message Content Intent)
3. Le bot a été **invité sur votre serveur Discord** avec les bonnes permissions

