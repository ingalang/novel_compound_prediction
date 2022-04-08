# lstm autoencoder recreate sequence
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.models import Model
import json
#from keras.utils import plot_model
import argparse

def train_LSTM_model(timesteps, input_vec_dims, input_sequence, num_samples, mode, epochs):
    if mode == 'reconstruct':
        # define model
        model = Sequential()
        model.add(LSTM(300, activation='relu', input_shape=(timesteps, input_vec_dims)))
        model.add(RepeatVector(timesteps))
        model.add(LSTM(300, activation='relu', return_sequences=True))
        model.add(TimeDistributed(Dense(1)))
        model.compile(optimizer='adam', loss='mse')
        model.fit(input_sequence, input_sequence, epochs=epochs, verbose=2)
        return model
    elif mode == 'predict':
        output_sequence = input_sequence[:, 1:, :]
        n_out = timesteps - 1
        model = Sequential()
        model.add(LSTM(100, activation='relu', input_shape=(timesteps, input_vec_dims)))
        model.add(RepeatVector(n_out))
        model.add(LSTM(100, activation='relu', return_sequences=True))
        model.add(TimeDistributed(Dense(1)))
        model.compile(optimizer='adam', loss='mse')
        model.fit(input_sequence, output_sequence, epochs=epochs, verbose=2)
        return model
    else:
        raise ValueError('mode must be either reconstruct or predict!')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, required=False, default=100)

    args = parser.parse_args()
    epochs = args.epochs

    mode = 'predict'

    # define input sequence

    with open('time_vecs.json', 'rb') as infile:
        time_vecs = json.load(infile)

    timesteps = 20
    input_vec_dims = 300
    num_samples = len(time_vecs)


    sequence = np.array([vec for vec in time_vecs.values()]).flatten()
    print(len(sequence))

    # reshape input into [samples, timesteps, features]
    sequence = sequence.reshape(num_samples, timesteps, input_vec_dims)

    model = train_LSTM_model(timesteps=timesteps,
                              input_vec_dims=input_vec_dims,
                              input_sequence = sequence,
                              num_samples = num_samples,
                              mode = mode,
                              epochs = epochs)

    model.save('lstm_model_{}_{}_{}'.format(epochs, input_vec_dims, mode))

    model = Model(inputs=model.inputs, outputs=model.layers[0].output)


    # get the feature vector for the input sequence

    test_sequence = np.array(time_vecs['car']).flatten()
    print(test_sequence.shape)
    test_sequence = test_sequence.reshape(1, timesteps, input_vec_dims)
    print(test_sequence.shape)

    yhat = model.predict(test_sequence)
    print(yhat.shape)
    print(yhat)


if __name__ == '__main__':
    main()