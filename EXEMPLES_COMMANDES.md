# Exemples de Commandes Discord

Voici des exemples d'utilisation du bot ARK Discord.

---

## Commandes de Base

### Afficher l'aide

```
!ark help
```

Affiche la liste complète des commandes disponibles avec leur description.

---

## Gestion des Instances

### Lister les instances disponibles

```
!ark instances
```

Affiche toutes les instances ARK configurées sur le serveur.

**Exemple de réponse :**
```
📋 Instances ARK disponibles
• main
• island
• ragnarok
```

---

## Surveillance du Serveur

### Vérifier le statut d'une instance

```
!ark status main
```

Affiche le statut détaillé du serveur ARK pour l'instance `main`.

**Exemple de réponse :**
```
📊 Statut du serveur ARK - main

Server running:  Yes
Server PID:  12345
Server listening:  Yes
Server Name: Mon Serveur ARK
Steam Players: 5 / 70
Server Version: 123.45
```

---

## Contrôle du Serveur

### Démarrer le serveur

```
!ark start main
```

Démarre l'instance ARK spécifiée.

### Arrêter le serveur

```
!ark stop main
```

Arrête proprement l'instance ARK spécifiée.

### Redémarrer le serveur

```
!ark restart main
```

Redémarre l'instance ARK spécifiée (équivalent à stop + start).

---

## Sauvegarde

### Créer une sauvegarde

```
!ark backup main
```

Lance une sauvegarde complète de l'instance ARK.

**Exemple de réponse :**
```
💾 Sauvegarde créée - main

Backup created: /path/to/backup/main-2025-10-23_10-30-00.tar.gz
```

---

## Communication avec les Joueurs

### Envoyer un message broadcast

```
!ark broadcast main Redémarrage du serveur dans 10 minutes
```

Envoie un message à tous les joueurs connectés sur l'instance `main`.

**Autres exemples :**

```
!ark broadcast main Le serveur va redémarrer pour une mise à jour
!ark broadcast island Event spécial ce soir à 20h !
!ark broadcast ragnarok Maintenance programmée dans 5 minutes
```

---

## Scénarios d'Utilisation

### Scénario 1 : Maintenance planifiée

```
# 1. Avertir les joueurs
!ark broadcast main Maintenance dans 10 minutes, sauvegardez vos données !

# 2. Attendre 10 minutes...

# 3. Créer une sauvegarde
!ark backup main

# 4. Arrêter le serveur
!ark stop main

# 5. Effectuer la maintenance...

# 6. Redémarrer le serveur
!ark start main

# 7. Vérifier que tout fonctionne
!ark status main
```

### Scénario 2 : Mise à jour du serveur

```
# 1. Avertir les joueurs
!ark broadcast main Mise à jour du serveur dans 5 minutes

# 2. Créer une sauvegarde de sécurité
!ark backup main

# 3. Redémarrer le serveur (arkmanager gère les mises à jour)
!ark restart main

# 4. Vérifier le statut
!ark status main
```

### Scénario 3 : Vérification rapide

```
# Lister les instances
!ark instances

# Vérifier le statut de chaque instance
!ark status main
!ark status island
!ark status ragnarok
```

---

## Permissions Discord (Recommandé)

Pour limiter l'accès aux commandes sensibles, configurez les permissions Discord :

1.  Créez un rôle "ARK Admin" sur votre serveur Discord
2.  Attribuez ce rôle uniquement aux personnes autorisées à gérer le serveur
3.  Modifiez le code du bot pour vérifier les permissions (voir section suivante)

### Exemple de vérification de permissions dans le code

Vous pouvez ajouter cette vérification dans `discord_bot.py` :

```python
def is_ark_admin():
    async def predicate(ctx):
        # Vérifier si l'utilisateur a le rôle "ARK Admin"
        return any(role.name == "ARK Admin" for role in ctx.author.roles)
    return commands.check(predicate)

# Puis ajouter le décorateur aux commandes sensibles
@bot.command(name='stop')
@is_ark_admin()
async def ark_stop(ctx, instance: str = None):
    # ... reste du code
```

---

## Notes Importantes

-   **Nom de l'instance** : Le nom de l'instance doit correspondre exactement à celui configuré dans arkmanager (sensible à la casse).
-   **Timeout** : Certaines commandes comme `start` et `restart` peuvent prendre du temps. Le bot affiche un message de chargement pendant l'exécution.
-   **Erreurs** : Si une commande échoue, le bot affiche le message d'erreur retourné par arkmanager.

---

## Commandes Avancées (Futures Extensions)

Voici quelques idées de commandes supplémentaires que vous pourriez ajouter :

-   `!ark update <instance>` : Mettre à jour le serveur ARK
-   `!ark players <instance>` : Lister les joueurs connectés
-   `!ark saveworld <instance>` : Forcer une sauvegarde du monde
-   `!ark rcon <instance> <commande>` : Exécuter une commande RCON personnalisée
-   `!ark logs <instance>` : Afficher les dernières lignes des logs du serveur

