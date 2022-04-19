from tensorflow import keras
import json
from collections import defaultdict
import numpy as np
import tqdm

def load_LSTM_model(filepath, mode):
    """
    Load a trained LSTM model
    :param filepath: filepath to the model folder
    :param mode: reconstruct or predict.
        Reconstruct mode gives a model that attempts to reconstruct its inputs
        Predict mode gives a model that attempts to predict the next input in the input sequence
    :return: keras model
    """
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

    # open our vectors, which are concatenated diachronic embeddings from our training data years (1990-2009)
    with open('time_vecs.json', 'rb') as infile:
        raw_temp_vecs = json.load(infile)

    encoded_temp_vecs = {}

    # load our trained LSTM model
    model = load_LSTM_model('lstm_model_100_300', mode)

    for word, vec in tqdm.tqdm(raw_temp_vecs.items()):
        temporal_vec = np.array(vec)
        # in reconstruct mode, we tell our model to predict the reconstruction of our vector
        # and we take the encoded/compressed vector as our encoded_vec
        if mode == 'reconstruct':
            temporal_vec = temporal_vec.reshape(1, 20, 300)
            encoded_vec = np.array(model.predict(temporal_vec)).flatten()
        # in predict mode, we let our model predict the next vector in our
        # sequence of vectors and we take that vector as our encoded_vec
        elif mode == 'predict':
            last_vec = temporal_vec[-1]
            encoded_vec = np.array(model.predict(last_vec))
        else:
            assert ValueError('mode must be either reconstruct or predict')
        encoded_temp_vecs[word] = encoded_vec.tolist()

    # save the encoded vectors dictionary as a json file
    with open(f'encoded_vecs_{mode}.json', 'w') as outfile:
        json.dump(encoded_temp_vecs, outfile)

if __name__ == '__main__':
    main()