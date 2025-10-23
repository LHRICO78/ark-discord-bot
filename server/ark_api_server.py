#!/usr/bin/env python3
"""
ARK Server API - Serveur API pour exécuter les commandes arkmanager
Ce serveur doit être installé sur le serveur ARK
"""

from flask import Flask, request, jsonify
import subprocess
import os
import secrets
import logging
from functools import wraps

# Configuration
API_TOKEN = os.getenv('ARK_API_TOKEN', secrets.token_urlsafe(32))
PORT = int(os.getenv('ARK_API_PORT', 2603))
ARKMANAGER_PATH = os.getenv('ARKMANAGER_PATH', '/usr/local/bin/arkmanager')

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Afficher le token au démarrage
logger.info(f"=" * 60)
logger.info(f"ARK API Server Token: {API_TOKEN}")
logger.info(f"Sauvegardez ce token pour le bot Discord !")
logger.info(f"=" * 60)


def require_token(f):
    """Décorateur pour vérifier le token d'authentification"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            logger.warning("Requête sans token d'authentification")
            return jsonify({'error': 'Token manquant'}), 401
        
        # Supporter les formats "Bearer TOKEN" et "TOKEN"
        if token.startswith('Bearer '):
            token = token[7:]
        
        if token != API_TOKEN:
            logger.warning(f"Token invalide reçu: {token[:10]}...")
            return jsonify({'error': 'Token invalide'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def execute_arkmanager(command, instance):
    """
    Exécute une commande arkmanager pour une instance donnée
    
    Args:
        command: La commande arkmanager (status, start, stop, etc.)
        instance: Le nom de l'instance ARK
    
    Returns:
        dict: Résultat avec 'success', 'output' et 'error'
    """
    try:
        # Construire la commande complète
        cmd = [ARKMANAGER_PATH, command, f'@{instance}']
        
        logger.info(f"Exécution: {' '.join(cmd)}")
        
        # Exécuter la commande
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        logger.info(f"Code retour: {result.returncode}")
        
        return {
            'success': result.returncode == 0,
            'output': output,
            'error': error,
            'returncode': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout lors de l'exécution de: {command} @{instance}")
        return {
            'success': False,
            'output': '',
            'error': 'Commande timeout après 30 secondes',
            'returncode': -1
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'exécution: {str(e)}")
        return {
            'success': False,
            'output': '',
            'error': str(e),
            'returncode': -1
        }


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé pour vérifier que l'API fonctionne"""
    return jsonify({'status': 'ok', 'service': 'ARK API Server'})


@app.route('/api/ark/status', methods=['POST'])
@require_token
def ark_status():
    """Obtenir le statut d'une instance ARK"""
    data = request.get_json()
    instance = data.get('instance')
    
    if not instance:
        return jsonify({'error': 'Instance manquante'}), 400
    
    result = execute_arkmanager('status', instance)
    return jsonify(result)


@app.route('/api/ark/start', methods=['POST'])
@require_token
def ark_start():
    """Démarrer une instance ARK"""
    data = request.get_json()
    instance = data.get('instance')
    
    if not instance:
        return jsonify({'error': 'Instance manquante'}), 400
    
    result = execute_arkmanager('start', instance)
    return jsonify(result)


@app.route('/api/ark/stop', methods=['POST'])
@require_token
def ark_stop():
    """Arrêter une instance ARK"""
    data = request.get_json()
    instance = data.get('instance')
    
    if not instance:
        return jsonify({'error': 'Instance manquante'}), 400
    
    result = execute_arkmanager('stop', instance)
    return jsonify(result)


@app.route('/api/ark/restart', methods=['POST'])
@require_token
def ark_restart():
    """Redémarrer une instance ARK"""
    data = request.get_json()
    instance = data.get('instance')
    
    if not instance:
        return jsonify({'error': 'Instance manquante'}), 400
    
    result = execute_arkmanager('restart', instance)
    return jsonify(result)


@app.route('/api/ark/backup', methods=['POST'])
@require_token
def ark_backup():
    """Faire une sauvegarde d'une instance ARK"""
    data = request.get_json()
    instance = data.get('instance')
    
    if not instance:
        return jsonify({'error': 'Instance manquante'}), 400
    
    result = execute_arkmanager('backup', instance)
    return jsonify(result)


@app.route('/api/ark/broadcast', methods=['POST'])
@require_token
def ark_broadcast():
    """Envoyer un message broadcast aux joueurs"""
    data = request.get_json()
    instance = data.get('instance')
    message = data.get('message')
    
    if not instance:
        return jsonify({'error': 'Instance manquante'}), 400
    
    if not message:
        return jsonify({'error': 'Message manquant'}), 400
    
    try:
        # Pour broadcast, on utilise rconcmd avec la commande broadcast
        cmd = [ARKMANAGER_PATH, 'rconcmd', f'@{instance}', f'broadcast {message}']
        
        logger.info(f"Broadcast: {message} vers @{instance}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout.strip(),
            'error': result.stderr.strip(),
            'returncode': result.returncode
        })
        
    except Exception as e:
        logger.error(f"Erreur broadcast: {str(e)}")
        return jsonify({
            'success': False,
            'output': '',
            'error': str(e),
            'returncode': -1
        })


@app.route('/api/ark/instances', methods=['GET'])
@require_token
def list_instances():
    """Lister les instances ARK disponibles"""
    try:
        result = subprocess.run(
            [ARKMANAGER_PATH, 'list-instances', '--brief'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        instances = result.stdout.strip().split()
        
        return jsonify({
            'success': True,
            'instances': instances
        })
        
    except Exception as e:
        logger.error(f"Erreur lors de la liste des instances: {str(e)}")
        return jsonify({
            'success': False,
            'instances': [],
            'error': str(e)
        })


if __name__ == '__main__':
    # Vérifier que arkmanager existe
    if not os.path.exists(ARKMANAGER_PATH):
        logger.error(f"arkmanager introuvable à: {ARKMANAGER_PATH}")
        logger.error("Définissez la variable ARKMANAGER_PATH avec le bon chemin")
    
    # Démarrer le serveur
    logger.info(f"Démarrage du serveur API ARK sur le port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)

