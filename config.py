"""
CONFIGURACIÓN DEL SISTEMA
Pet Store - Chatbot con Análisis Predictivo y Red Neuronal
"""

import os
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIGURACIÓN DE BASE DE DATOS POSTGRESQL
# =============================================================================
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5433)),
    'database': os.getenv('DB_NAME', 'petstore'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '12345'),
    'sslmode': 'prefer'
}

# =============================================================================
# CONFIGURACIÓN DE MODELOS DE RED NEURONAL
# =============================================================================
MODEL_CONFIG = {
    'max_words': 5000,
    'max_len': 50,
    'embedding_dim': 128,
    'lstm_units': 64,
    'dense_units': 32,
    'dropout_rate': 0.3,
    'epochs': 50,
    'batch_size': 32,
    'validation_split': 0.2,
    'confidence_threshold': 0.65
}

# =============================================================================
# CONFIGURACIÓN DE ANÁLISIS PREDICTIVO
# =============================================================================
PREDICTOR_CONFIG = {
    'prediction_epochs': 100,
    'prediction_batch_size': 32,
    'test_size': 0.2,
    'random_state': 42
}

# =============================================================================
# RUTAS DE ARCHIVOS
# =============================================================================
PATHS = {
    'models_dir': 'models',
    'data_dir': 'data',
    'exports_dir': 'exports',
    'chatbot_model': 'models/chatbot_model.h5',
    'predictor_model': 'models/predictor_model.h5',
    'tokenizer': 'models/tokenizer.pkl',
    'label_encoder': 'models/label_encoder.pkl',
    'scaler': 'models/scaler.pkl',
    'dataset': 'data/dataset_citas_ml.csv'
}

# Crear directorios si no existen
for directory in ['models', 'data', 'exports']:
    os.makedirs(directory, exist_ok=True)

# =============================================================================
# CONFIGURACIÓN DEL CHATBOT
# =============================================================================
CHATBOT_CONFIG = {
    'nombre': 'PetBot',
    'version': '2.0',
    'idioma': 'es',
    'modo_debug': True
}

