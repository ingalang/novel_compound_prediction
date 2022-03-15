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


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, required=False, default=50)

    args = parser.parse_args()
    epochs = args.epochs

    # define input sequence


    ## test: la oss si du har vektorer med 5 dimensjoner. Du har 2 samples og 3 timesteps. Hvis alle vektorene for hver
    # sample er lagra som én lang vektor, sånn :
    # 'car' : [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    # 'boat': [4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6]
    with open('time_vecs.json', 'rb') as infile:
        time_vecs = json.load(infile)

    time_steps = 20
    input_vec_dims = 300
    num_samples = len(time_vecs)


    sequence = np.array([vec for vec in time_vecs.values()]).flatten()
    print(len(sequence))

    # reshape input into [samples, timesteps, features]
    sequence = sequence.reshape(num_samples, time_steps, input_vec_dims)
    n_in = len(sequence)

    input_vectors = np.random.rand(num_samples, input_vec_dims * time_steps)
    print(input_vectors.shape)

    # sequence = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])


    sequence = sequence.reshape((num_samples, time_steps, input_vec_dims))
    print(sequence)
    print(sequence.shape)
    # define model
    model = Sequential()
    model.add(LSTM(300, activation='relu', input_shape=(time_steps, input_vec_dims)))
    model.add(RepeatVector(time_steps))
    model.add(LSTM(300, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(1)))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(sequence, sequence, epochs=epochs, verbose=1)
    # plot_model(model, show_shapes=True, to_file='reconstruct_lstm_autoencoder.png')
    model.save('lstm_model_{}_{}'.format(epochs, input_vec_dims))

    #model = Model(inputs=model.inputs, outputs=model.layers[0].output)


    # get the feature vector for the input sequence
    #yhat = model.predict(sequence)
    #print(yhat.shape)
    #print(yhat)


if __name__ == '__main__':
    main()