#!/usr/bin/env python3
"""
ARK Discord Bot - Bot Discord pour contrôler le serveur ARK
Ce bot communique avec l'API ARK Server pour exécuter les commandes
"""

import discord
from discord.ext import commands
import aiohttp
import os
import logging
from typing import Optional

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ARK_API_URL = os.getenv('ARK_API_URL', 'http://votre-serveur-ark:2603')
ARK_API_TOKEN = os.getenv('ARK_API_TOKEN')

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Vérifier la configuration
if not DISCORD_TOKEN:
    logger.error("DISCORD_BOT_TOKEN n'est pas défini !")
    exit(1)

if not ARK_API_TOKEN:
    logger.error("ARK_API_TOKEN n'est pas défini !")
    exit(1)

# Configuration du bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def call_ark_api(endpoint: str, instance: str, message: Optional[str] = None) -> dict:
    """
    Appelle l'API ARK Server
    
    Args:
        endpoint: L'endpoint de l'API (status, start, stop, etc.)
        instance: Le nom de l'instance ARK
        message: Message optionnel pour broadcast
    
    Returns:
        dict: Réponse de l'API
    """
    url = f"{ARK_API_URL}/api/ark/{endpoint}"
    headers = {
        'Authorization': f'Bearer {ARK_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {'instance': instance}
    if message:
        data['message'] = message
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=60) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    return {
                        'success': False,
                        'error': f"Erreur HTTP {response.status}: {error_text}"
                    }
    except aiohttp.ClientError as e:
        logger.error(f"Erreur de connexion à l'API: {str(e)}")
        return {
            'success': False,
            'error': f"Impossible de se connecter au serveur ARK: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        return {
            'success': False,
            'error': f"Erreur: {str(e)}"
        }


def format_status_output(output: str) -> str:
    """
    Formate la sortie de la commande status pour Discord
    
    Args:
        output: La sortie brute de arkmanager status
    
    Returns:
        str: Sortie formatée pour Discord
    """
    # Supprimer les codes de couleur ANSI
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_output = ansi_escape.sub('', output)
    
    return f"```\n{clean_output}\n```"


@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    logger.info(f'Bot connecté en tant que {bot.user}')
    logger.info(f'URL de l\'API ARK: {ARK_API_URL}')
    await bot.change_presence(activity=discord.Game(name="ARK Server Manager"))


@bot.command(name='ark')
async def ark_help(ctx):
    """Affiche l'aide pour les commandes ARK"""
    embed = discord.Embed(
        title="🦖 ARK Server Manager - Commandes",
        description="Gérez votre serveur ARK depuis Discord",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="!ark status <instance>",
        value="Affiche le statut du serveur ARK",
        inline=False
    )
    
    embed.add_field(
        name="!ark start <instance>",
        value="Démarre le serveur ARK",
        inline=False
    )
    
    embed.add_field(
        name="!ark stop <instance>",
        value="Arrête le serveur ARK",
        inline=False
    )
    
    embed.add_field(
        name="!ark restart <instance>",
        value="Redémarre le serveur ARK",
        inline=False
    )
    
    embed.add_field(
        name="!ark backup <instance>",
        value="Crée une sauvegarde du serveur",
        inline=False
    )
    
    embed.add_field(
        name="!ark broadcast <instance> <message>",
        value="Envoie un message à tous les joueurs",
        inline=False
    )
    
    embed.add_field(
        name="!ark instances",
        value="Liste toutes les instances disponibles",
        inline=False
    )
    
    embed.set_footer(text="Exemple: !ark status main")
    
    await ctx.send(embed=embed)


@bot.command(name='status')
async def ark_status(ctx, instance: str = None):
    """Affiche le statut d'une instance ARK"""
    if not instance:
        await ctx.send("❌ Veuillez spécifier le nom de l'instance.\nExemple: `!ark status main`")
        return
    
    # Envoyer un message de chargement
    loading_msg = await ctx.send(f"⏳ Récupération du statut de l'instance `{instance}`...")
    
    # Appeler l'API
    result = await call_ark_api('status', instance)
    
    if result.get('success'):
        output = format_status_output(result.get('output', 'Aucune sortie'))
        
        embed = discord.Embed(
            title=f"📊 Statut du serveur ARK - {instance}",
            description=output,
            color=discord.Color.blue()
        )
        
        await loading_msg.edit(content=None, embed=embed)
    else:
        error = result.get('error', 'Erreur inconnue')
        await loading_msg.edit(content=f"❌ Erreur lors de la récupération du statut:\n```\n{error}\n```")


@bot.command(name='start')
async def ark_start(ctx, instance: str = None):
    """Démarre une instance ARK"""
    if not instance:
        await ctx.send("❌ Veuillez spécifier le nom de l'instance.\nExemple: `!ark start main`")
        return
    
    loading_msg = await ctx.send(f"⏳ Démarrage de l'instance `{instance}`...")
    
    result = await call_ark_api('start', instance)
    
    if result.get('success'):
        embed = discord.Embed(
            title=f"✅ Serveur démarré - {instance}",
            description=f"```\n{result.get('output', 'Serveur démarré avec succès')}\n```",
            color=discord.Color.green()
        )
        await loading_msg.edit(content=None, embed=embed)
    else:
        error = result.get('error', 'Erreur inconnue')
        await loading_msg.edit(content=f"❌ Erreur lors du démarrage:\n```\n{error}\n```")


@bot.command(name='stop')
async def ark_stop(ctx, instance: str = None):
    """Arrête une instance ARK"""
    if not instance:
        await ctx.send("❌ Veuillez spécifier le nom de l'instance.\nExemple: `!ark stop main`")
        return
    
    loading_msg = await ctx.send(f"⏳ Arrêt de l'instance `{instance}`...")
    
    result = await call_ark_api('stop', instance)
    
    if result.get('success'):
        embed = discord.Embed(
            title=f"🛑 Serveur arrêté - {instance}",
            description=f"```\n{result.get('output', 'Serveur arrêté avec succès')}\n```",
            color=discord.Color.orange()
        )
        await loading_msg.edit(content=None, embed=embed)
    else:
        error = result.get('error', 'Erreur inconnue')
        await loading_msg.edit(content=f"❌ Erreur lors de l'arrêt:\n```\n{error}\n```")


@bot.command(name='restart')
async def ark_restart(ctx, instance: str = None):
    """Redémarre une instance ARK"""
    if not instance:
        await ctx.send("❌ Veuillez spécifier le nom de l'instance.\nExemple: `!ark restart main`")
        return
    
    loading_msg = await ctx.send(f"⏳ Redémarrage de l'instance `{instance}`...")
    
    result = await call_ark_api('restart', instance)
    
    if result.get('success'):
        embed = discord.Embed(
            title=f"🔄 Serveur redémarré - {instance}",
            description=f"```\n{result.get('output', 'Serveur redémarré avec succès')}\n```",
            color=discord.Color.blue()
        )
        await loading_msg.edit(content=None, embed=embed)
    else:
        error = result.get('error', 'Erreur inconnue')
        await loading_msg.edit(content=f"❌ Erreur lors du redémarrage:\n```\n{error}\n```")


@bot.command(name='backup')
async def ark_backup(ctx, instance: str = None):
    """Crée une sauvegarde d'une instance ARK"""
    if not instance:
        await ctx.send("❌ Veuillez spécifier le nom de l'instance.\nExemple: `!ark backup main`")
        return
    
    loading_msg = await ctx.send(f"⏳ Création d'une sauvegarde de l'instance `{instance}`...")
    
    result = await call_ark_api('backup', instance)
    
    if result.get('success'):
        embed = discord.Embed(
            title=f"💾 Sauvegarde créée - {instance}",
            description=f"```\n{result.get('output', 'Sauvegarde créée avec succès')}\n```",
            color=discord.Color.green()
        )
        await loading_msg.edit(content=None, embed=embed)
    else:
        error = result.get('error', 'Erreur inconnue')
        await loading_msg.edit(content=f"❌ Erreur lors de la sauvegarde:\n```\n{error}\n```")


@bot.command(name='broadcast')
async def ark_broadcast(ctx, instance: str = None, *, message: str = None):
    """Envoie un message broadcast aux joueurs"""
    if not instance:
        await ctx.send("❌ Veuillez spécifier le nom de l'instance.\nExemple: `!ark broadcast main Redémarrage dans 5 minutes`")
        return
    
    if not message:
        await ctx.send("❌ Veuillez spécifier un message.\nExemple: `!ark broadcast main Redémarrage dans 5 minutes`")
        return
    
    loading_msg = await ctx.send(f"⏳ Envoi du message à l'instance `{instance}`...")
    
    result = await call_ark_api('broadcast', instance, message)
    
    if result.get('success'):
        embed = discord.Embed(
            title=f"📢 Message envoyé - {instance}",
            description=f"**Message:** {message}",
            color=discord.Color.purple()
        )
        await loading_msg.edit(content=None, embed=embed)
    else:
        error = result.get('error', 'Erreur inconnue')
        await loading_msg.edit(content=f"❌ Erreur lors de l'envoi du message:\n```\n{error}\n```")


@bot.command(name='instances')
async def ark_instances(ctx):
    """Liste toutes les instances ARK disponibles"""
    loading_msg = await ctx.send("⏳ Récupération de la liste des instances...")
    
    url = f"{ARK_API_URL}/api/ark/instances"
    headers = {'Authorization': f'Bearer {ARK_API_TOKEN}'}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    
                    if result.get('success'):
                        instances = result.get('instances', [])
                        
                        if instances:
                            instances_list = '\n'.join([f"• {inst}" for inst in instances])
                            embed = discord.Embed(
                                title="📋 Instances ARK disponibles",
                                description=instances_list,
                                color=discord.Color.blue()
                            )
                            await loading_msg.edit(content=None, embed=embed)
                        else:
                            await loading_msg.edit(content="ℹ️ Aucune instance trouvée.")
                    else:
                        error = result.get('error', 'Erreur inconnue')
                        await loading_msg.edit(content=f"❌ Erreur:\n```\n{error}\n```")
                else:
                    await loading_msg.edit(content=f"❌ Erreur HTTP {response.status}")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des instances: {str(e)}")
        await loading_msg.edit(content=f"❌ Erreur de connexion: {str(e)}")


@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs de commandes"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Commande inconnue. Tapez `!ark` pour voir la liste des commandes.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argument manquant. Tapez `!ark` pour voir la liste des commandes.")
    else:
        logger.error(f"Erreur de commande: {str(error)}")
        await ctx.send(f"❌ Une erreur s'est produite: {str(error)}")


if __name__ == '__main__':
    logger.info("Démarrage du bot Discord ARK...")
    logger.info(f"Préfixe des commandes: !")
    bot.run(DISCORD_TOKEN)

