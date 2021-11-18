from compound_joiner import get_compounds_from_sentence
import os
import spacy
import itertools
import argparse
from collections import Counter
import json

class SentenceReader(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        with open(self.filename, 'r') as infile:
            for line in infile:
                yield line

def get_compound_generator(top_dir, start_year, end_year, separate_years=False):
    """
    :param top_dir:
    :param start_year:
    :param end_year:
    :param data_name:
    :return:
    """
    pos_tagger = spacy.load('en_core_web_sm')
    #compounds = []
    for year in range(start_year, end_year + 1):
        print(f'Processing year: {year}')
        filepath = os.path.join(top_dir, f'COCA_{year}.txt')
        sentence_reader = SentenceReader(filepath)
        for sentence in sentence_reader:
            sentence_compounds = get_compounds_from_sentence(sentence, pos_tagger, toggle_lowercase=True)
            if separate_years:
                pass
            else:
                yield sentence_compounds
        if separate_years:
            #TODO save files & counts for separate years
            pass
    #return compounds

def save_dataset(compounds, save_dir, start_year, end_year, data_name, separate_years=False):
    if separate_years:
        pass
    else:
        compound_set = {*compounds}
        filename = f'COCA_{start_year}-{end_year}_{data_name}_all.txt'
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'w') as outfile:
            for compound in compound_set:
                outfile.write(f'{compound} \n')
        print(f'Saved file {filepath}')

def incrementally_store_compounds(top_dir, save_dir, start_year, end_year, data_name, separate_years=False):
    filename = f'COCA_{start_year}-{end_year}_{data_name}_all.txt'
    filepath = os.path.join(save_dir, filename)
    print(f'Starting saving compounds to file: {filepath}')
    with open(filepath, 'w') as outfile:
        for compound in get_compound_generator(top_dir, start_year, end_year):
            outfile.write(f'{compound} \n')
    print(f'Successfully saved file: {filepath}')

def save_compound_counts(compounds, save_dir, start_year, end_year, data_name, separate_years=False):
    if separate_years:
        filename = 'placeholder.txt' #TODO
        count_dict = {} #TODO
    else:
        assert isinstance(compounds, list), 'If separate_years=False, the compounds argument must be of type list'
        counter = Counter(compounds)
        count_dict = dict(counter)
        filename = f'COCA_compound_counts_{start_year}-{end_year}_{data_name}_merged_all.txt'
    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'w') as outfile:
        json.dump(count_dict, outfile)
    print(f'Saved compound counts to file: {filepath}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_dir', default='test_COCA', required=False)
    parser.add_argument('--start_year', default=1990, required=False, type=int,
                        help='Start of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--end_year', default=1991, required=False, type=int,
                        help='End of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--data_name', default='train', required=False)
    parser.add_argument('--save_dir', default='test_COCA', required=False,
                        help='Path to directory where you want to save the count & compound files')

    args = parser.parse_args()

    top_dir, start_year, end_year, data_name, save_dir = \
        args.top_dir, args.start_year, args.end_year, args.data_name, args.save_dir

    incrementally_store_compounds(top_dir, save_dir, start_year, end_year, data_name)

    # compounds = get_compound_generator(top_dir, start_year, end_year)
    # compounds = list(compounds)
    # print(compounds)
    # save_dataset(compounds=compounds,
    #              save_dir=save_dir,
    #              start_year=start_year,
    #              end_year=end_year,
    #              data_name=data_name)

    # save_compound_counts(compounds=compounds,
    #                      save_dir=save_dir,
    #                      start_year=start_year,
    #                      end_year=end_year,
    #                      data_name=data_name)

if __name__ == '__main__':
    main()



