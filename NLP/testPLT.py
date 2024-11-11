import tensorflow as tf
import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
import re
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from transformers import AutoTokenizer
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Descargar la lista de stopwords si no está ya descargada
nltk.download('stopwords')

# Cargar las stopwords en español
spanish_stopwords = set(stopwords.words('spanish'))


print("¿GPU disponible?:", tf.config.list_physical_devices('GPU'))

model = AutoModelForSequenceClassification.from_pretrained('NLP/beto_model')
tokenizer = AutoTokenizer.from_pretrained('NLP/beto_model')

# Preparar el dispositivo
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Nuevos textos para predecir
new_texts = [
    'Este es un ejemplo de texto en español para predicción.',
    'Otro ejemplo de texto para probar el modelo.',
]

# Tokenizar los nuevos textos
encodings = tokenizer(
    new_texts,
    truncation=True,
    padding=True,
    max_length=128,
    return_tensors='pt'
)

# Mover los tensores al dispositivo
encodings = {key: val.to(device) for key, val in encodings.items()}

# Realizar las predicciones
model.eval()
with torch.no_grad():
    outputs = model(**encodings)
    predictions = outputs.logits.squeeze(-1)
    predictions = predictions.cpu().numpy()

# Mostrar los resultados
for text, prediction in zip(new_texts, predictions):
    print(f'Texto: {text}')
    print(f'Valor Predicho: {prediction}')
    print('---')