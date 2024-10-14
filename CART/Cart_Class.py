import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt

class CarPriceClassifier:
    def __init__(self, train_folder, test_folder):
        self.train_folder = train_folder
        self.test_folder = test_folder
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.cart_model = DecisionTreeClassifier(random_state=42, max_depth=7)
        self.ordinal_columns = ['brand', 'model', 'color', 'fuelType', 'province', 'environmentalLabel']
        self.numeric_columns2 = ['price', 'km', 'year', 'cubicCapacity', 'power_cv', 'co2Emissions', 'color', 'maxSpeed']

    def load_data_from_folder(self, folder_path):
        all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
        df_list = [pd.read_csv(file) for file in all_files]
        return pd.concat(df_list, ignore_index=True)

    def preprocess_data(self, df):
        # Definir clases de precio
        df['price_class'] = pd.qcut(df['price'], q=3, labels=['baja', 'media', 'alta'])
        
        # Codificar columnas categóricas
        for col in self.ordinal_columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le
        
        # Eliminar filas con valores nulos en las columnas numéricas
        df = df.dropna(subset=self.numeric_columns2)
        
        # Seleccionar columnas necesarias
        columns_to_keep = self.numeric_columns2 + self.ordinal_columns + ['price_class']
        return df[columns_to_keep]

    def fit(self):
        # Cargar y procesar datos de entrenamiento
        train_df = self.load_data_from_folder(self.train_folder)
        train_df = self.preprocess_data(train_df)
        
        # Separar características (X) y variable objetivo (y)
        X_train = train_df.drop(columns=['price', 'price_class'])
        y_train = train_df['price_class']
        
        feature_names = X_train.columns
        # Normalizar características
        X_train = self.scaler.fit_transform(X_train)
        
        # Entrenar modelo
        self.cart_model.fit(X_train, y_train)
        self.feature_names = feature_names

    def evaluate(self):
        # Cargar y procesar datos de prueba
        test_df = self.load_data_from_folder(self.test_folder)
        test_df = self.preprocess_data(test_df)
        
        # Separar características (X) y variable objetivo (y)
        X_test = test_df.drop(columns=['price', 'price_class'])
        y_test = test_df['price_class']
        
        # Normalizar características
        X_test = self.scaler.transform(X_test)
        
        # Hacer predicciones y evaluar
        y_pred = self.cart_model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("\nClassification Report:\n", classification_report(y_test, y_pred))
        print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

    def plot_tree(self):
        # Visualizar el árbol
        plt.figure(figsize=(20, 10))
        plot_tree(self.cart_model, feature_names=self.feature_names, class_names=['baja', 'media', 'alta'], filled=True, rounded=True)
        plt.show()

# Uso de la clase
train_folder = 'data/final_data/train'
test_folder = 'data/final_data/test'

#EJECUCION DE CODIGO

car_classifier = CarPriceClassifier(train_folder, test_folder)
car_classifier.fit()
car_classifier.evaluate()
car_classifier.plot_tree()
