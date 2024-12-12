# Utilise une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le code du producteur et du consommateur dans le conteneur
COPY producer.py .
COPY consumer.py .

# Installer les dépendances
RUN pip install kafka-python requests

# Copier le script pour démarrer les deux services
COPY start.sh .

# Donner les droits d'exécution au script
RUN chmod +x start.sh

# Commande à exécuter lors du démarrage du conteneur
CMD ["./start.sh"]
