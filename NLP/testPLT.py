import pickle


# Cargar el modelo
with open('models/desc_model.pkl', 'rb') as f:
    model = pickle.load(f)


# Mostrar un resumen del modelo para verificar su estructura
try:
    print(model.summary())
except AttributeError:
    print("El modelo no tiene el método 'summary', probablemente no sea un modelo Keras.")


