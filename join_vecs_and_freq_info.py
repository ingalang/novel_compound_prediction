import pandas as pd
from gensim.models.word2vec import Word2Vec
import numpy as np
import json
import tqdm

def get_freq_info(word, freq_data):
    """
    Get the frequency counts for the last five years for a word, given the word and a dataframe with frequency counts.
    :param word: word to get frequency counts for
    :param freq_data: pd.DataFrame containing frequency counts
    :return: np.array with freq. counts from the last five years of data (up until 2009), or an np.array of five 0s
    """
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

# open train, dev, and test data
freq_data_train = pd.read_csv('COCA_word_freq_train_1990_2009.csv', sep='\t')
freq_data_test = pd.read_csv('COCA_word_freq_test_1990_2009.csv', sep='\t')
freq_data_dev = pd.read_csv('COCA_word_freq_dev_1990_2009.csv', sep='\t')

# combine train, dev, and test to get the full data
full_data = pd.concat([freq_data_train, freq_data_test, freq_data_dev]).reset_index().dropna()
full_data = full_data.drop(columns=['index', 'Unnamed: 0'])
print(full_data)

# load the word2vec model
word2vec_model = Word2Vec.load('word2vec_2009.model')

vecs_with_freq_info = {}

# go through all words and join word2vec representations with the last five years of frequency counts for each word
for word in tqdm.tqdm(list(full_data['word'].values)):
    word_vector = get_embedding(word, word2vec_model)
    frequencies = get_freq_info(word, full_data)
    vecs_with_freq_info[word] = np.concatenate((word_vector, frequencies)).tolist()

# save the vectors
with open('vecs_with_freqs.json', 'w') as outfile:
    json.dump(vecs_with_freq_info, outfile)

print('done')