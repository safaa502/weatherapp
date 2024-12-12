#!/bin/bash

# Démarrer le producteur en arrière-plan
python producer.py &

# Démarrer le consommateur
python consumer.py
