from compound_counts import load_compounds, singularize_heads
import argparse
import os
from collections import Counter
from gensim.models import Word2Vec

def load_dataset(dir, data_name):
    # load a txt file with compounds, return a list of compounds
    filepath = os.path.join(dir, f'COCA_{data_name}.txt')
    with open(filepath, 'r') as compound_file:
        compound_list = [line for line in compound_file]
    return compound_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_dir', default='test_COCA', required=False)
    parser.add_argument('--start_year', default=1999, required=False, type=int,
                        help='Start of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--end_year', default=2000, required=False, type=int,
                        help='End of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--save_dir', default='test_COCA', required=False,
                        help='Path to directory where you want to save the datasets')
    parser.add_argument('--data_name', required=True, type=str,
                        help='What kind of dataset you are making (train, dev, test)')
    parser.add_argument('--freq_cutoff', default=3, type=int,
                        help='Only include compounds that occur at least this number of times')

    args = parser.parse_args()

    top_dir, start_year, end_year, save_dir, data_name, freq_cutoff = \
        args.top_dir, args.start_year, args.end_year, args.save_dir, args.data_name, args.freq_cutoff
    assert(data_name in ['train', 'dev', 'test']), "argument --data_name must be either train, dev, or test"

    all_compounds = []

    # go through each year, load the compounds from the given year, singularize the heads, and add to list of all compounds
    for year in range(start_year, end_year + 1):
        print(f'Processing compounds from year {year}')
        compound_list = load_compounds(top_dir, year)
        singularized_compounds = singularize_heads(compound_list)
        all_compounds.extend(singularized_compounds)

    # we use a frequency cutoff to ensure that compounds occur at least a given number of times
    if freq_cutoff:
        compound_counts = dict(Counter(all_compounds))
        all_compounds = [comp for comp in compound_counts if compound_counts[comp] >= freq_cutoff]

    # get unique compounds from the all_compounds list
    unique_compounds = list({*all_compounds})

    word2vec_model = Word2Vec.load('word2vec_2009.model')

    # If we're dealing with dev data, we first need a dictionary of training compounds
    # to make sure the dev compounds are not found in training data
    if data_name == 'dev':
        train_data = load_dataset(save_dir, 'train')
        print('Making train dict...')
        train_dict = {word.strip('\n\r') : 0 for word in train_data}
        print('Making set of compounds for dev set that are not in train set...')
        unique_compounds = [comp for comp in unique_compounds if comp not in train_dict and
                            comp.split()[0] in word2vec_model.wv and comp.split()[1] in word2vec_model.wv]
    # if we're making test data, we have to make sure the compounds occur neither in the train nor in the dev data
    elif data_name == 'test':
        print('Making train dict...')
        train_data = load_dataset(save_dir, 'train')
        train_dict = {word.strip('\n\r'): 0 for word in train_data}

        print('Making dev dict...')
        dev_data = load_dataset(save_dir, 'dev')
        dev_dict = {word.strip('\n\r'): 0 for word in dev_data}

        unique_compounds = [compound.strip() for compound in unique_compounds
                        if compound.strip() not in train_dict
                            and compound not in dev_dict
                            and compound.split()[0] in word2vec_model.wv
                            and compound.split()[1] in word2vec_model.wv]

    # save compounds, indicating the frequency cutoff in the filename
    if freq_cutoff:
        filepath = os.path.join(save_dir, f'COCA_{data_name}_min{freq_cutoff}.txt')
    else:
        filepath = os.path.join(save_dir, f'COCA_{data_name}.txt')

    print(f'Saving file: {filepath}')
    with open(filepath, 'w') as outfile:
        for compound in unique_compounds:
            outfile.write(f'{compound}\n')


if __name__ == '__main__':
    main()