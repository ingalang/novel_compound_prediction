import argparse
import numpy as np
from os import path
from collections import Counter
import nltk
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

    with open(comp_filepath, 'r') as infile:
        compounds = [line.strip('\n\r') for line in infile]

    unique_words = np.unique([comp.split()[0] for comp in compounds] + [comp.split()[1] for comp in compounds])
    time_span = (end_year-start_year)+1

    counts_df = pd.DataFrame()
    counts_df['word'] = pd.Series(unique_words)
    print(counts_df.head())


    for year in range(start_year, end_year+1):
        filepath = path.join(coca_filepath, 'COCA_{}.txt'.format(year))
        with open(filepath, 'r') as infile:
            full_text = infile.read().lower()
            all_words = nltk.word_tokenize(full_text)
            num_words = len(all_words)
            word_counts = Counter(all_words)
            word_rel_counts = {word : count/num_words for word, count in word_counts.items()}
            counts_df[str(year)] = counts_df['word'].map(word_rel_counts, na_action='ignore')
            del all_words

    print(counts_df.head(n=20))

    counts_df = counts_df.fillna(0)
    print(counts_df.head(n=20))

    counts_df.to_csv('COCA_word_freq_{}_{}.csv'.format(start_year, end_year), sep='\t')


if __name__ == '__main__':
    main()


