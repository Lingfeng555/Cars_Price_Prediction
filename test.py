import os
#os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
print("TF_ENABLE_ONEDNN_OPTS:", os.getenv('TF_ENABLE_ONEDNN_OPTS'))

from NLP import *

if __name__ == '__main__':
    #train = Loader.load_train()
    model = DescModel()
    # Verifica si CUDA está disponible
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #print(torch.cuda.is_available())
    #print(torch.cuda.current_device())
    #print(torch.cuda.get_device_name(torch.cuda.current_device()))
    #print(f"Using device: {device}")

