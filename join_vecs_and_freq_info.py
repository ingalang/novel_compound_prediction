import pandas as pd
from gensim.models.word2vec import Word2Vec
import numpy as np
import json
import tqdm

def get_freq_info(word, freq_data):
    if word in list(freq_data['word']):
            word_freq = freq_data.loc[freq_data['word'] == word]
            word_freq = np.array(word_freq.iloc[0][-5:])
            return word_freq
    else:
        return np.array([0.00]*5)

def get_embedding(word, model):
    if word in model.wv:
        return model.wv[word]
    else:
        return np.zeros(300)

freq_data_train = pd.read_csv('COCA_word_freq_train_1990_2009.csv', sep='\t')
freq_data_test = pd.read_csv('COCA_word_freq_test_1990_2009.csv', sep='\t')
freq_data_dev = pd.read_csv('COCA_word_freq_dev_1990_2009.csv', sep='\t')

full_data = pd.concat([freq_data_train, freq_data_test, freq_data_dev]).reset_index().dropna()
full_data = full_data.drop(columns=['index', 'Unnamed: 0'])
print(full_data)

word2vec_model = Word2Vec.load('word2vec_2009.model')

vecs_with_freq_info = {}

for word in tqdm.tqdm(list(full_data['word'].values)):
    word_vector = get_embedding(word, word2vec_model)
    frequencies = get_freq_info(word, full_data)
    vecs_with_freq_info[word] = np.concatenate((word_vector, frequencies)).tolist()

with open('vecs_with_freqs.json', 'w') as outfile:
    json.dump(vecs_with_freq_info, outfile)

print('done')