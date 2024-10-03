import os
import pandas as pd

class Loader:
    train_path = "data/final_data/train"
    test_path = "data/final_data/test"
    original_path = "data/final_data/original"

    def __load_data(self, folder_path):
        # Lista para almacenar los DataFrames
        df_list = []

        # Recorrer todos los archivos en la carpeta
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                # Obtener la ruta completa del archivo
                file_path = os.path.join(folder_path, filename)
                
                # Leer el archivo CSV y agregarlo a la lista de DataFrames
                df = pd.read_csv(file_path)
                df_list.append(df)

        # Concatenar todos los DataFrames en uno solo
        if df_list:
            merged_df = pd.concat(df_list, ignore_index=True)
            return merged_df
        else:
            print("No se encontraron archivos CSV en la carpeta.")
            return pd.DataFrame()
        
    def load_train(self): return self.__load_data(self.train_path)

    def load_test(self): return self.__load_data(self.test_path)

    def load_original(self): return self.__load_data(self.original_path)

    def load__all(self): return {"original": self.load_original(), "train": self.load_train(), "test": self.load_test()}