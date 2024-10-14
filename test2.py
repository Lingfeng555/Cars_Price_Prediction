import os
import tensorflow as tf  # Asegúrate de importar TensorFlow
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
print("TF_ENABLE_ONEDNN_OPTS:", os.getenv('TF_ENABLE_ONEDNN_OPTS'))
import datetime

from NLP import *

if __name__ == '__main__':
    # Cargar datos de prueba
    test = Loader.load_test()
    print(len(test))
    
    model = DescModel()
    
    
    #PReparar data
    
    test = model.preprocess_data(test)
    
    x_embeddings = np.stack(test["embedding"].values)
    x_km = test['km'].to_numpy().reshape(-1, 1)
    y = test['price'].to_numpy()
    
    x_embeddings_scaled = model.scaler_embeddings.fit_transform(x_embeddings)
    x_km_scaled = model.scaler_km.fit_transform(x_km)
    y_scaled = model.scaler_y.fit_transform(y.reshape(-1, 1)).flatten() 
    
    
    

    
    # Imprimir el resumen del modelo
    #print(model.model.summary())

    # Hacer predicciones con el modelo
    #predictions = model.predict(test)
    #print(predictions)

    # Guardar el modelo para TensorBoard
    log_dir = os.path.join("logs", "model_visualization")
    os.makedirs(log_dir, exist_ok=True)  


    # Crear un callback de TensorBoard
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    # Reentrenar el modelo brevemente solo para la visualización (no afecta el estado del modelo)
    model.model.fit(
        [x_embeddings_scaled, x_km_scaled],
        y_scaled,
        epochs=1,
        batch_size=32,
        verbose=True,
        callbacks=[tensorboard_callback]
    )
    # (Opcional) Si no deseas reentrenar, simplemente guarda el modelo
    #tf.saved_model.save(model.model, log_dir)  # Descomentar si deseas guardar sin reentrenar

    # Iniciar TensorBoard (puedes hacer esto en un terminal aparte)
    print("Inicia TensorBoard en la terminal con el comando: tensorboard --logdir=logs/model_visualization/train")
