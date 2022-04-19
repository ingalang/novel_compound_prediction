import argparse
import os
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from collections import defaultdict
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--comp_file_dir', type=str, required=True, help='directory of the compound list files')
    parser.add_argument('--model_dir', type=str, required=True, help='directory of the incremental word2vec model files')
    parser.add_argument('--start_year', type=int, required=False, default=1990)
    parser.add_argument('--end_year', type=int, required=False, default=2009)
    parser.add_argument('--dims', type=int, default=300, required=False)

    args = parser.parse_args()
    dims = args.dims

    with open(os.path.join(args.comp_file_dir, 'COCA_train_min3_no_doubles_filtered.txt'), 'r') as infile:
        train_compounds = [line.strip('\n\r') for line in infile]

    with open(os.path.join(args.comp_file_dir, 'COCA_dev_min3_no_doubles_filtered.txt'), 'r') as infile:
        dev_compounds = [line.strip('\n\r') for line in infile]

    all_words = [word for comp in dev_compounds for word in comp.split()] + \
                [word for comp in train_compounds for word in comp.split()]
    print(len(all_words))
    unique_constituents = np.unique(all_words)

    def get_vec_for_word(word, model, dims):
        """
        Gets the vector for a word given a word2vec model
        :param word: word to get vector for
        :param model: a trained word2vec model
        :param dims: vector dimensions, to use if we need a vector of zeros
        :return: vector (in list format) for the word given the model, or a vector of zeros
        """
        if word in model.wv:
            return model.wv[word].tolist()
        else:
            return np.zeros(dims).tolist()

    time_vec_dict = defaultdict(list)

    # go through each year and get the embedding of the words
    # corresponding to a model trained up until (and including) said year.
    # Append all vectors to the time_vec_dict
    for year in range(args.start_year, args.end_year + 1):
        print('Appending {} vectors...'.format(year))
        word2vec_model = Word2Vec.load(os.path.join(args.model_dir, 'word2vec_{}_{}.model'.format(year, dims))) ##den riktige
        for word in unique_constituents:
            time_vec_dict[word].append(get_vec_for_word(word, word2vec_model, dims))

    # save the vector dictionary as a json file
    with open('time_vecs.json', 'w') as outfile:
        json.dump(time_vec_dict, outfile)

    print('DONE')
if __name__ == '__main__':
    main()