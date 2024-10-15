import os
import pandas as pd
import re
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler


class Loader:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    train_path = os.path.join(dir_path, "../data/final_data/train")
    test_path = os.path.join(dir_path, "../data/final_data/test")
    original_path = os.path.join(dir_path, "../data/final_data/original")
    scaler = StandardScaler()
    ordinal_columns = ['brand', 'model', 'color', 'fuelType', 'province', 'environmentalLabel', 'price_class']
    numeric_columns = ['price', 'km', 'year', 'cubicCapacity', 'power_cv', 'co2Emissions', 'maxSpeed']
    


    @staticmethod
    def convert_to_bool(cls, x):
        if x.lower() == 'true':
            return True
        elif x.lower() == 'false':
            return False
        else:
            return x
    
    @staticmethod
    def convert_to_float_or_zero(x):
        if x == "no tiene": return 0.0
        if x == "cero": return 0.0
        if x == "NA": return 0.0
        return float(x)
    
    @staticmethod
    def convert_string_to_float(x):
        if isinstance(x, str): return pd.to_numeric(x, errors='coerce')

    @staticmethod
    def extract_value(voltage_string):
        # Utilizar expresiones regulares para encontrar números en el string
        match = re.search(r'([-+]?[0-9]*\.?[0-9]+)', voltage_string)
        if match:
            # Convertir el número encontrado a float
            return float(match.group(0))
        else:
            # Devolver None si no se encuentra ningún número
            return np.nan

    @staticmethod
    def catecorical_to_numerical(df):
        # Definir clases de precio
        
        label_encoders = {}
        
        # Codificar columnas categóricas
        for col in Loader.ordinal_columns:
            if(col in df):
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le
            
        return df


    @staticmethod
    def normalize_data(df):
        # Selecciona solo las columnas numéricas
        numeric_data = df[Loader.numeric_columns]
        # Aplica la transformación solo en esas columnas
        df[Loader.numeric_columns] = Loader.scaler.transform(numeric_data)
        return df

    @staticmethod
    def normalize_fit(df):
        # Selecciona solo las columnas numéricas
        numeric_data = df[Loader.numeric_columns]
        # Ajusta y transforma solo en esas columnas
        df[Loader.numeric_columns] = Loader.scaler.fit_transform(numeric_data)
        return df

    @staticmethod
    def __load_data(folder_path):
        df_list = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path, 
                                 converters={
                                     123: Loader.convert_to_float_or_zero,
                                     127: Loader.convert_string_to_float,
                                     142: Loader.extract_value,
                                     144: Loader.extract_value,
                                     })
                df_list.append(df)
        if df_list:
            merged_df = pd.concat(df_list, ignore_index=True)
            merged_df["valves_per_cylinder"] = merged_df["valves_per_cylinder"].apply(Loader.convert_to_float_or_zero)
            merged_df = Loader.catecorical_to_numerical(merged_df)
           
            return merged_df
        else:
            print("No se encontraron archivos CSV en la carpeta.")
            return pd.DataFrame()

    @classmethod
    def load_train(cls):
        return  Loader.normalize_fit(cls.__load_data(cls.train_path))

    @classmethod
    def load_test(cls):
        return Loader.normalize_data(cls.__load_data(cls.test_path))

    @classmethod
    def load_original(cls):
        return cls.__load_data(cls.original_path)

    @classmethod
    def load_all(cls):
        return {"original": cls.load_original(), "train": cls.load_train(), "test": cls.load_test()}
    
    @classmethod
    def load_api_sample(cls, data):
        try:
            df = pd.json_normalize(data)
            
            try:
                df["displacement_liters"] = df["displacement_liters"].apply(Loader.convert_to_float_or_zero)
                df["bore_diameter"] = df["bore_diameter"].apply(Loader.convert_string_to_float)
                df["electricFeatures.standardModeChargeStart"] = df["electricFeatures.standardModeChargeStart"].apply(Loader.extract_value)
                df["electricFeatures.fastModeChargeStart"] = df["electricFeatures.fastModeChargeStart"].apply(Loader.extract_value)
                df["valves_per_cylinder"] = df["valves_per_cylinder"].apply(Loader.convert_to_float_or_zero)
            except Exception as e:
                print(f"Error al convertir los datos: {e}")
            
            df = Loader.catecorical_to_numerical(df)
            
            return df

        except Exception as e:
            print(f"Error al cargar los datos de la API: {e}")
            return pd.DataFrame()
        
