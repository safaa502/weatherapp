from kafka import KafkaProducer
import requests
import json
import time

# Configuration Kafka
KAFKA_BROKER = "kafka:9092"  # Utilise le nom du conteneur Kafka et le port interne
TOPIC_NAME = "weather-data"   # Le nom du topic

# Configuration de l'API OpenWeatherMap
API_KEY = "3740f591db5a3cd5050c407b25551cca"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Liste des villes à surveiller
CITIES = ["Paris", "Casablanca", "New York", "Tokyo"]

# Initialisation du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Sérialisation des données en JSON
)

# Fonction pour récupérer les données météo
def fetch_weather_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',  # Température en Celsius
        'lang': 'fr'        # Langue en français
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()  # Données JSON de l'API
    else:
        print(f"Erreur API pour {city}: {response.status_code}")
        return None

# Fonction d'envoi des données à Kafka
def send_to_kafka():
    while True:
        for city in CITIES:
            data = fetch_weather_data(city)
            if data:
                producer.send(TOPIC_NAME, value=data)
                print(f"Données envoyées pour {city}: {data['main']['temp']} °C")
        
        # Pause entre les envois (par exemple toutes les 60 secondes)
        time.sleep(60)

# Lancer l'envoi des données
if __name__ == "__main__":
    try:
        print("Envoi des données vers Kafka...")
        send_to_kafka()
    except KeyboardInterrupt:
        print("Arrêt du producteur Kafka.")
    finally:
        producer.close()
