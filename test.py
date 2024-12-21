import sys
sys.path.insert(1, '../') 
from utils.loader import Loader
from utils.evaluator import Evaluator

from sklearn.metrics import mean_squared_error
import tensorflow as tf
import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
import re
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
from torchmetrics import MeanSquaredError
from torch.utils.data import Dataset
from transformers import AutoTokenizer, Trainer, TrainingArguments, BertModel
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Descargar la lista de stopwords si no está ya descargada
nltk.download('stopwords')

# Cargar las stopwords en español
spanish_stopwords = set(stopwords.words('spanish'))


print("¿GPU disponible?:", tf.config.list_physical_devices('GPU'))

train = Loader.load_NLP() [:2000]

def custom_concat(row, cols):
    # Construir la descripción con lógica condicional basada en el valor de la celda
    parts = []
    for col_name in cols:  # Cambio para iterar solo sobre las columnas especificadas
        if col_name in row.index:  # Verificar que el nombre de la columna esté en el DataFrame
            value = row[col_name]
            if value == "no tiene" or not isinstance(value, str):
                parts.append(f"no tiene {col_name}")
            else:
                parts.append(str(value))  # Convertir a string para evitar problemas al unir
    # Unir todas las partes con espacios
    return ' '.join(parts)

# Aplicar la función al DataFrame
def filter_train_data(train):
    descriptions = [col for col in train.columns if "description" in col]
    train['full_description'] = train.apply(custom_concat, axis=1, args=(descriptions,))
    filtered_columns = ["price", "km", "fuelType", "full_description"]
    train = train[filtered_columns]
    train.dropna(inplace=True)
    return train

train = filter_train_data(train)

km_scaler = StandardScaler()
train["km"] = km_scaler.fit_transform(train["km"].to_numpy().reshape(-1, 1))

price_scaler = StandardScaler()
train["price"] = price_scaler.fit_transform(train["price"].to_numpy().reshape(-1, 1))

verb_size = 128
model_name = 'dccuchile/bert-base-spanish-wwm-cased'  # BETO

train_texts, val_texts, train_labels, val_labels, train_km, val_km = train_test_split(
    train["full_description"],
    train["price"],
    train["km"],
    test_size=0.2,
    random_state=42,
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_encodings = tokenizer(
    list(train_texts), truncation=True, padding=True, max_length=verb_size
)
val_encodings = tokenizer(
    list(val_texts), truncation=True, padding=True, max_length=verb_size
)

class RegressionDataset(Dataset):
    def __init__(self, encodings, labels, km_values):
        self.encodings = encodings
        self.labels = labels.astype(np.float32)  # Ensure labels are float
        self.km_values = torch.tensor(km_values, dtype=torch.float32)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels.iloc[idx])
        item['km'] = self.km_values[idx]
        return item

    def __len__(self):
        return len(self.labels)
    
train_dataset = RegressionDataset(train_encodings, train_labels, train_km.values)
val_dataset = RegressionDataset(val_encodings, val_labels, val_km.values)

class CustomRegressionModel(torch.nn.Module):
    def __init__(self, bert_model_name, km_dim=1):
        super(CustomRegressionModel, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.km_layer = torch.nn.Linear(km_dim, 16)  # Process km separately
        self.regressor = torch.nn.Linear(self.bert.config.hidden_size + 16, 1)  # Combine BERT and km outputs

    def forward(self, input_ids, attention_mask, km):
        # BERT outputs
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        bert_cls_output = outputs.pooler_output  # [CLS] token representation (batch_size, hidden_size)

        # Process km
        if len(km.shape) == 1:  # Ensure km has two dimensions
            km = km.unsqueeze(1)  # Shape becomes (batch_size, 1)

        km_output = self.km_layer(km)  # Shape becomes (batch_size, 16)

        # Concatenate and pass to regression head
        combined_output = torch.cat((bert_cls_output, km_output), dim=1)  # (batch_size, hidden_size + 16)
        logits = self.regressor(combined_output)  # Output shape: (batch_size, 1)
        return logits
model = CustomRegressionModel(model_name)

mse_metric = MeanSquaredError()


def compute_metrics(pred):
    predictions = torch.tensor(pred.predictions.flatten())  # Convert predictions to tensor
    labels = torch.tensor(pred.label_ids)  # Convert labels to tensor
    mse = mse_metric(predictions, labels)  # Compute Mean Squared Error
    ret = {'eval_mse': mse.item(), 'mse': mse.item()}  # Return as dictionary
    print(f"Metrics: {ret}")  # Debug print
    return ret


training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy='steps',  # Ensure evaluation happens during training
    eval_steps=500,  # Evaluate every 500 steps
    save_strategy='steps',
    save_steps=500,
    num_train_epochs=3,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=64,
    load_best_model_at_end=True,
    metric_for_best_model='eval_mse',  # Match key in compute_metrics
    logging_dir='./logs',
    logging_steps=500,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)
print(compute_metrics)
print(trainer.compute_metrics)
metrics = trainer.evaluate()
print("Returned metrics:", metrics)
