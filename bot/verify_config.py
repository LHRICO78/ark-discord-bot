#!/usr/bin/env python3
"""
Script de vérification de la configuration du bot Discord ARK
Exécutez ce script pour diagnostiquer les problèmes de configuration
"""

import os
import sys

def check_env_file():
    """Vérifie l'existence et le contenu du fichier .env"""
    print("=" * 60)
    print("🔍 Vérification de la configuration")
    print("=" * 60)
    print()
    
    # Vérifier si .env existe
    if not os.path.exists('.env'):
        print("❌ ERREUR: Le fichier .env n'existe pas!")
        print("   → Copiez .env.example vers .env et configurez-le")
        return False
    
    print("✅ Le fichier .env existe")
    print()
    
    # Charger les variables depuis .env
    env_vars = {}
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    # Vérifier DISCORD_BOT_TOKEN
    print("📋 Vérification des variables:")
    print()
    
    token = env_vars.get('DISCORD_BOT_TOKEN', '')
    print(f"1. DISCORD_BOT_TOKEN:")
    if not token or token == 'votre_token_discord_ici':
        print("   ❌ Token Discord non configuré ou invalide")
        print("   → Obtenez votre token sur https://discord.com/developers/applications")
        return False
    elif len(token) < 50:
        print(f"   ⚠️  Token trop court ({len(token)} caractères)")
        print("   → Un token Discord valide fait environ 70 caractères")
        return False
    elif ' ' in token:
        print("   ❌ Le token contient des espaces")
        print("   → Supprimez les espaces avant et après le token")
        return False
    else:
        print(f"   ✅ Token présent ({len(token)} caractères)")
        print(f"   → Début: {token[:20]}...")
    
    print()
    
    # Vérifier ARK_API_URL
    api_url = env_vars.get('ARK_API_URL', '')
    print(f"2. ARK_API_URL:")
    if not api_url or api_url.startswith('http://123.456'):
        print("   ⚠️  URL de l'API ARK non configurée (valeur par défaut)")
        print("   → Configurez l'URL de votre serveur API ARK")
    elif not api_url.startswith('http://') and not api_url.startswith('https://'):
        print("   ⚠️  L'URL doit commencer par http:// ou https://")
    else:
        print(f"   ✅ URL configurée: {api_url}")
    
    print()
    
    # Vérifier ARK_API_TOKEN
    api_token = env_vars.get('ARK_API_TOKEN', '')
    print(f"3. ARK_API_TOKEN:")
    if not api_token or api_token == 'votre_token_secret_ici':
        print("   ⚠️  Token API ARK non configuré")
        print("   → Configurez le même token que sur votre serveur API ARK")
    else:
        print(f"   ✅ Token API présent ({len(api_token)} caractères)")
    
    print()
    print("=" * 60)
    
    # Vérifier les variables d'environnement système
    print()
    print("🔍 Vérification des variables d'environnement système:")
    print()
    
    sys_token = os.getenv('DISCORD_BOT_TOKEN')
    if sys_token:
        print(f"✅ DISCORD_BOT_TOKEN défini dans l'environnement ({len(sys_token)} caractères)")
    else:
        print("⚠️  DISCORD_BOT_TOKEN non défini dans l'environnement")
        print("   → Le fichier .env sera utilisé")
    
    print()
    
    return True

def main():
    """Fonction principale"""
    try:
        success = check_env_file()
        print()
        if success:
            print("✅ Configuration valide ! Le bot devrait pouvoir démarrer.")
        else:
            print("❌ Configuration invalide. Corrigez les erreurs ci-dessus.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
