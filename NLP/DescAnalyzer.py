import os
import sys
sys.path.insert(1, '../') 
from utils.loader import Loader
import pandas as pd
from gensim.models import Word2Vec
import re
import nltk
from nltk.corpus import stopwords

class Embedder ():
    
    verb_size = 200

    def custom_concat(self, row, cols):
        parts = []
        for col_name in cols:
            if col_name in row.index:
                value = row[col_name]
                if value == "no tiene" or not isinstance(value, str):
                    parts.append(f"no tiene {col_name}")
                else:
                    parts.append(str(value))
        return ' '.join(parts)

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s\d]', '', text) 
        tokens = text.split()
        filtered_tokens = [token for token in tokens if token not in spanish_stopwords]
        return filtered_tokens

    def get_average_embedding(self, tokens, model):
        embeddings = [model[word] for word in tokens if word in model]
        if embeddings:
            return np.mean(embeddings, axis=0)
        else:
            return np.zeros(model.vector_size)

    def embed(self, column):
        tokens = column.apply(self.preprocess_text)
        model_w2v = Word2Vec(sentences=tokens, vector_size=self.verb_size, window=1, min_count=3, workers=8)
        word_vectors = model_w2v.wv
        return word_vectors

    def __init__(self, verb_size):
        self.verb_size = verb_size
        print("Prepare Train Dataframe")

        train = Loader.load_train()
        descriptions = [col for col in train.columns if "description" in col]
        train['full_description'] = train.apply(self.custom_concat, axis=1, args=(descriptions,))
        filtered_columns = ["idx", "price", "km", "fuelType", "full_description"]
        train = train[filtered_columns]
        train["price_per_kilometer"] = train["price"]/train["km"]
        train.dropna(inplace=True)

        print("Start transet Embedding")
        self.word_vectors = self.embed(train['full_description'])
        print("Embedding finished")
        pass

    def embedding_process(self, column):
        tokens = column.apply(self.preprocess_text)
        return tokens.apply(lambda x: self.get_average_embedding(x, word_vectors))