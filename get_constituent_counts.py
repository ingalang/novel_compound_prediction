import argparse
import numpy as np
from os import path
from collections import Counter
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compound_file', type=str, required=True)
    parser.add_argument('--coca_filepath', type=str, required=True)
    parser.add_argument('--start_year', type=int, required=True)
    parser.add_argument('--end_year', type=int, required=True)

    args = parser.parse_args()

    comp_filepath, coca_filepath, start_year, end_year = \
        args.compound_file, args.coca_filepath, args.start_year, args.end_year

    # figure out which dataset part we're working with
    if 'train' in comp_filepath:
        dataset = 'train'
    elif 'test' in comp_filepath:
        dataset = 'test'
    elif 'dev' in comp_filepath:
        dataset = 'dev'
    else:
        dataset = 'unknown'
        print('Compound file mentions no dataset type (train, dev, test)')

    with open(comp_filepath, 'r') as infile:
        compounds = [line.strip('\n\r') for line in infile]

    # get all unique words among compound constituents, both modifiers and heads
    unique_words = np.unique([comp.split()[0] for comp in compounds] + [comp.split()[1] for comp in compounds])

    counts_df = pd.DataFrame()
    counts_df['word'] = pd.Series(unique_words)
    print(counts_df.head())

    # go through each year and count all occurrences of each unique word for each year
    for year in range(start_year, end_year+1):
        filepath = path.join(coca_filepath, 'COCA_{}.txt'.format(year))
        with open(filepath, 'r') as infile:
            full_text = infile.read().lower()
            all_words = full_text.split()
            num_words = len(all_words)
            word_counts = Counter(all_words)
            word_rel_counts = {word : count/num_words for word, count in word_counts.items()}
            counts_df[str(year)] = counts_df['word'].map(word_rel_counts, na_action='ignore')
            del all_words

    print(counts_df.head(n=20))

    # words we don't have counts for in a given year get a count of 0
    counts_df = counts_df.fillna(0)

    # save the counts to a csv file
    counts_df.to_csv('COCA_word_freq_{}_{}_{}.csv'.format(dataset, start_year, end_year), sep='\t')


if __name__ == '__main__':
    main()


