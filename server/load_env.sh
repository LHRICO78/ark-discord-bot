#!/bin/bash
# Script pour charger les variables d'environnement depuis .env

if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "Variables d'environnement chargées depuis .env"
else
    echo "Fichier .env introuvable. Copiez .env.example vers .env et configurez-le."
    exit 1
fi

