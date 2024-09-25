import os
import json


folder_path = 'data'

finalData = []


for filename in os.listdir(folder_path):
    print("Procesando archivo: ", filename)
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                finalData.extend(data)
            except json.JSONDecodeError as e:
                print(f"Error al procesar {filename}: {e}")




output_file = os.path.join(folder_path, 'finalData.json')
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(finalData, f, ensure_ascii=False, indent=4)

print(f"Todos los archivos JSON han sido combinados en {output_file}")
