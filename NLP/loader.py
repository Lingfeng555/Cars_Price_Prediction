import os
import pandas as pd

def merge_csv_files_from_folder(folder_path):
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

data = merge_csv_files_from_folder("NLP/test_data")
print(len(data))
print(data["transmissionTypeId"].value_counts())