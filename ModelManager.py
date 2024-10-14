import os
import numpy as np
from NLP import *
import requests


class ModelManager:
    def __init__(self):
        self.models = {}

    def load_model(self, model_name):
        """Carga un modelo dado su nombre."""
        if model_name == 'desc_model':
            self.models[model_name] = DescModel()
            print(f'Modelo {model_name} cargado.')
        
        #No hay más modelos por ahora
        else:
            print(f'Modelo {model_name} no reconocido.')

    def predict(self, model_name, test_data):
        """Realiza una predicción usando el modelo especificado."""
        if model_name in self.models:
            model = self.models[model_name]
            prediction = model.predict(test_data)
            return prediction
        else:
            print(f'Modelo {model_name} no ha sido cargado.')
            return None

    def evaluate_model(self, model_name, test_data):
        """Evalúa el rendimiento del modelo usando el conjunto de prueba."""
        prediction = self.predict(model_name, test_data)
        if prediction is not None:
            real_price = test_data["price"]
            diff = np.mean(abs((real_price - prediction) / real_price))
            print(f"Hay un MAPE de {diff * 100}% para el modelo {model_name}.")


def get_random_sample():
    """Obtiene una muestra única de datos desde la API."""
    url = "http://127.0.0.1:5000/api/random/all"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta es un código de error
        return response.json()  # Devuelve el JSON como un diccionario
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener la muestra única: {e}')
        return None
    
    
    

if __name__ == '__main__':
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    print("TF_ENABLE_ONEDNN_OPTS:", os.getenv('TF_ENABLE_ONEDNN_OPTS'))

    test = Loader.load_test()
    print(f'Tamaño del conjunto de prueba: {len(test)}')

    # Inicializa el gestor de modelos
    model_manager = ModelManager()

    model_manager.load_model('desc_model')
    
    random_car = get_random_sample()["data"]
    random_car2 = get_random_sample()["data"]
    random_car3 = get_random_sample()["data"]
    
    
    sample_processed = Loader.load_api_sample(random_car)
    sample_processed2 = Loader.load_api_sample(random_car2)
    sample_processed3 = Loader.load_api_sample(random_car3)
    

    prediction = model_manager.predict('desc_model', sample_processed)
    print(f'Predicción 0: {prediction[0]} , Real: {random_car["price"]} , diff: {abs(prediction[0] - random_car["price"])}')
    
    prediction2 = model_manager.predict('desc_model', sample_processed2)
    print(f'Predicción 1: {prediction2[0]} , Real: {random_car2["price"]} , diff: {abs(prediction2[0] - random_car2["price"])}')
    
    prediction3 = model_manager.predict('desc_model', sample_processed3)
    print(f'Predicción 2: {prediction3[0]} , Real: {random_car3["price"]} , diff: {abs(prediction3[0] - random_car3["price"])}')
    
    
    
    
    #model_manager.evaluate_model('desc_model', test)
