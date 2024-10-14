import os
#os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
print("TF_ENABLE_ONEDNN_OPTS:", os.getenv('TF_ENABLE_ONEDNN_OPTS'))

from NLP import *

if __name__ == '__main__':
    test = Loader.load_test()
    print(len(test))
    model = DescModel()

    prediction = model.predict(test)

    real_price = test["price"]
    diff = np.mean(abs((real_price - prediction) / real_price))
    print(f"Hay un MAPE de {diff * 100}%")



