import os
import pandas as pd
import re
import numpy as np

class Loader:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    train_path = os.path.join(dir_path, "../data/final_data/train")
    test_path = os.path.join(dir_path, "../data/final_data/test")
    original_path = os.path.join(dir_path, "../data/final_data/original")
    
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
            return merged_df
        else:
            print("No se encontraron archivos CSV en la carpeta.")
            return pd.DataFrame()

    @classmethod
    def load_train(cls):
        return cls.__load_data(cls.train_path)

    @classmethod
    def load_test(cls):
        return cls.__load_data(cls.test_path)

    @classmethod
    def load_original(cls):
        return cls.__load_data(cls.original_path)

    @classmethod
    def load_all(cls):
        return {"original": cls.load_original(), "train": cls.load_train(), "test": cls.load_test()}