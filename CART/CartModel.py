import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib  # Importar joblib para guardar y cargar el modelo
from utils.loader import Loader
from utils.logger import Logger
import sys
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import joblib  # Importar joblib para guardar y cargar el modelo
from utils.loader import Loader

class CarPriceClassifier:
    def __init__(self, train_folder, test_folder):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.cart_model = DecisionTreeClassifier(random_state=42, max_depth=7)
        self.ordinal_columns = ['brand', 'model', 'color', 'fuelType', 'province', 'environmentalLabel']
        self.numeric_columns2 = ['price', 'km', 'year', 'cubicCapacity', 'power_cv', 'co2Emissions', 'maxSpeed']
        self.models_paths = os.path.join(os.getcwd(), "CART", "models")

    def preprocess_data(self, df):
        # Eliminar filas con valores nulos en las columnas numéricas
        df['price_class'] = pd.qcut(df['price'], q=3, labels=['baja', 'media', 'alta'])
        df = df.dropna(subset=self.numeric_columns2)
        df = Loader.catecorical_to_numerical(df)
        # Seleccionar columnas necesarias
        columns_to_keep = self.numeric_columns2 + self.ordinal_columns + ['price_class']
        return df[columns_to_keep]

    def fit(self):
        # Cargar y procesar datos de entrenamiento
        train_df = Loader.load_train()
        train_df = self.preprocess_data(train_df)

        # Debug: Print shapes
        print("Training Data Shape:", train_df.shape)

        # Separar características (X) y variable objetivo (y)
        X_train = train_df.drop(columns=['price', 'price_class'])
        y_train = train_df['price_class']

        feature_names = X_train.columns
        # Normalizar características
        X_train = self.scaler.fit_transform(X_train)

        # Entrenar modelo
        self.cart_model.fit(X_train, y_train)
        self.feature_names = feature_names

    def save_model(self, filename='/car_price_classifier_model.pkl'):
        # Guardar el modelo y el escalador
        joblib.dump({
            'model': self.cart_model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders
        }, os.path.join(self.models_paths, filename))
        print(f"Modelo guardado en {os.path.join(self.models_paths, filename)}.")

    def load_model(self, filename='/car_price_classifier_model.pkl'):
        # Cargar el modelo y el escalador
        data = joblib.load(os.path.join(self.models_paths, filename))
        self.cart_model = data['model']
        self.scaler = data['scaler']
        self.label_encoders = data['label_encoders']
        print(f"Modelo cargado desde {os.path.join(self.models_paths, filename)}.")

    def predict(self, X):
        X_processed = self.preprocess_data(X)
        X_processed = X_processed.drop(columns=['price', 'price_class'], errors='ignore')  # Asegurarse de que se elimine sin error

        # Normalizar las características procesadas
        X_normalized = self.scaler.transform(X_processed)

        return self.cart_model.predict(X_normalized)

    def evaluate(self):
        # Cargar y procesar datos de prueba
        test_df = Loader.load_test()
        test_df = self.preprocess_data(test_df)

        # Debug: Print shapes
        print("Test Data Shape:", test_df.shape)

        # Guardar price_class en y
        y_test = test_df['price_class']

        # Hacer predicciones y evaluar
        y_pred = self.predict(test_df)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))
        print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

    def plot_tree(self):
        # Visualizar el árbol
        plt.figure(figsize=(20, 10))
        plot_tree(self.cart_model, feature_names=self.feature_names, class_names=['baja', 'media', 'alta'], filled=True, rounded=True)
        plt.show()


if __name__ == '__main__':
    # Uso de la clase
    train_folder = 'data/final_data/train'
    test_folder = 'data/final_data/test'

    # Ejecutar código
    car_classifier = CarPriceClassifier(train_folder, test_folder)
    car_classifier.fit()

    # Guardar modelo
    car_classifier.save_model()

    # Cargar modelo y evaluar
    car_classifier.load_model()
    car_classifier.evaluate()
    car_classifier.plot_tree()
