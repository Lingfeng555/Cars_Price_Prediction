import sys
sys.path.insert(1, '../') 
from utils.loader import Loader

import os
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Concatenate, BatchNormalization
import pickle

from .Embedder import Embedder

class DescModel:

    def __init__(self):
        train = Loader.load_train()
        self.embedder = Embedder(200, train)
        # Intentar cargar el modelo o entrenar si no existe
        self.model = self.load_model("models/model_2_text_km_to_price.keras", train)

    def preprocess_data(self, train):
        """Preprocesa los datos para obtener las descripciones embebidas y normaliza los valores."""
        descriptions = [col for col in train.columns if "description" in col]
        train['full_description'] = train.apply(self.embedder.custom_concat, axis=1, args=(descriptions,))
        train['embedding'] = self.embedder.embedding_process(train['full_description'])
        return train

    def split_and_scale_data(self, train):
        """Divide el dataset en entrenamiento y prueba, y escala las características."""
        train_df, test_df = train_test_split(train, test_size=0.2, random_state=42, stratify=train['fuelType'])

        x_embeddings = np.stack(train_df["embedding"].values)
        x_km = train_df['km'].to_numpy().reshape(-1, 1)
        y = train_df['price'].to_numpy()

        self.scaler_embeddings = StandardScaler()
        x_embeddings_scaled = self.scaler_embeddings.fit_transform(x_embeddings)

        self.scaler_km = StandardScaler()
        x_km_scaled = self.scaler_km.fit_transform(x_km)

        self.scaler_y = StandardScaler()
        y_scaled = self.scaler_y.fit_transform(y.reshape(-1, 1)).flatten()

        return train_df, test_df, x_embeddings_scaled, x_km_scaled, y_scaled

    def build_model(self):
        """Construye el modelo de red neuronal."""
        input_embeddings = Input(shape=(200,), name='embeddings_input')
        input_km = Input(shape=(1,), name='km_input')

        # Procesamiento de embeddings
        x = Dense(200, activation='relu')(input_embeddings)
        x = BatchNormalization()(x)
        x = Dense(64, activation='relu')(x)
        x = BatchNormalization()(x)

        # Procesamiento de 'km'
        km_processed = Dense(32, activation='relu')(input_km)

        # Combinar embeddings y 'km'
        combined = Concatenate()([x, km_processed])

        z = Dense(16, activation='softplus')(combined)
        z = BatchNormalization()(z)
        z = Dense(1)(z)  # Capa de salida

        model = Model(inputs=[input_embeddings, input_km], outputs=z)
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mean_squared_error')

        return model

    def train_model(self, train):
        """Entrena el modelo con los datos dados."""
        train = self.preprocess_data(train)
        train_df, test_df, x_embeddings_scaled, x_km_scaled, y_scaled = self.split_and_scale_data(train)

        self.model = self.build_model()

        print("COMIENZA EL ENTRENAMIENTO...")
        history = self.model.fit(
            [x_embeddings_scaled, x_km_scaled],
            y_scaled,
            epochs=200,
            batch_size=32,
            verbose=True
        )
        print("TERMINA EL ENTRENAMIENTO...")
        print(self.model.summary())

        # Evaluación en datos de prueba
        new_embeddings_scaled = self.scaler_embeddings.transform(np.stack(test_df["embedding"].values))
        new_km_scaled = self.scaler_km.transform(test_df['km'].to_numpy().reshape(-1, 1))

        print('Forma de new_embeddings_scaled:', new_embeddings_scaled.shape)
        print('Forma de new_km_scaled:', new_km_scaled.shape)

        prediction = self.model.predict([new_embeddings_scaled, new_km_scaled]).flatten()
        prediction = self.scaler_y.inverse_transform(prediction.reshape(-1, 1)).flatten()
        real_price = test_df['price'].to_numpy()

        result = pd.DataFrame({'Prediction': prediction, 'Real price': real_price})

        diff = np.mean(abs((real_price - prediction) / real_price))
        print(result)
        print(f"Hay un MAPE de {diff * 100}%")

    def load_model(self, path_modelo, train):
        """Intenta cargar el modelo desde un archivo o entrena uno nuevo si no existe."""
        self.train_model(train)
        return
        if os.path.isfile(path_modelo) and path_modelo.endswith('.keras'):
            try:
                self.model = tf.keras.models.load_model(path_modelo)
                print("Modelo cargado exitosamente.")
            except Exception as e:
                print(f"Error al cargar el modelo: {e}. Entrenando nuevo modelo...")
                self.train_model(train)
        else:
            print("El archivo no existe o no tiene la extensión '.keras'. Entrenando nuevo modelo...")
            self.train_model(train)
