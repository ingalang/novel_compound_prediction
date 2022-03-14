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

    embedding_df = pd.DataFrame()
    embedding_df['word'] = unique_constituents

    def get_vec_for_word(word, model, dims):
        if word in model.wv:
            return model.wv[word]
        else:
            return np.zeros(dims)

    def get_full_vector(df, word):
        full_vec = df.loc[df['word'] == word]
        print(full_vec)
        del full_vec['word']
        return np.array([v for vec in full_vec.values for v in vec]).flatten()

    time_vec_dict = defaultdict(list)
    for year in range(args.start_year, args.end_year + 1):
        word2vec_model = Word2Vec.load(os.path.join(args.model_dir, 'word2vec_{}_{}.model'.format(year, dims)))
        for word in unique_constituents:
            time_vec_dict[word].append(get_vec_for_word(word, word2vec_model, dims))

    with open('time_vecs.json', 'w') as outfile:
        json.dump(time_vec_dict, outfile)

    new_df = pd.DataFrame.from_dict(time_vec_dict).T.reset_index(level=0)
    print(new_df.head())

    # test_df = pd.DataFrame()
    # test_df['word'] = ['car', 'cat', 'mouse']
    # print(test_df)
    # test_dict = {'car' : [[1, 7, 18, 1], [2, 2, 2, 2]],
    #              'cat' : [[3, 3, 3, 3], [4, 4, 4, 4]],
    #              'mouse' : [[5, 5, 5, 5], [6, 6, 6, 6]]}
    # new_df = pd.DataFrame.from_dict(test_dict).T.reset_index(level=0)
    # new_df.columns = ['word']+list(range(1990,1991+1))
    # print(new_df)



if __name__ == '__main__':
    main()