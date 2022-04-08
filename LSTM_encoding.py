from tensorflow import keras
import json
from collections import defaultdict
import numpy as np
import tqdm

def load_LSTM_model(filepath, mode):
    model = keras.models.load_model(filepath)
    if mode == 'reconstruct':
        model = keras.models.Model(inputs=model.inputs, outputs=model.layers[0].output)
        return model
    elif mode == 'predict':
        return model
    else:
        assert ValueError('mode must be either reconstruct or predict')


def main():
    mode = 'reconstruct'

    with open('time_vecs.json', 'rb') as infile:
        raw_temp_vecs = json.load(infile)

    encoded_temp_vecs = {}

    model = load_LSTM_model('lstm_model_100_300', mode)

    for word, vec in tqdm.tqdm(raw_temp_vecs.items()):
        temporal_vec = np.array(vec)
        #print(temporal_vec.shape)
        if mode == 'reconstruct':
            temporal_vec = temporal_vec.reshape(1, 20, 300)
            encoded_vec = np.array(model.predict(temporal_vec)).flatten()
        elif mode == 'predict':
            last_vec = temporal_vec[-1]
            encoded_vec = np.array(model.predict(last_vec))
        else:
            assert ValueError('mode must be either reconstruct or predict')
        #print(len(encoded_vec))
        encoded_temp_vecs[word] = encoded_vec.tolist()

    with open(f'encoded_vecs_{mode}.json', 'w') as outfile:
        json.dump(encoded_temp_vecs, outfile)

if __name__ == '__main__':
    main()