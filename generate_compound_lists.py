import os
import spacy
import argparse
import multiprocessing as mp
import re
import tqdm

def get_compounds(text, pos_tagger):
    """
    Returns all noun compounds found in a text, as determined by some heuristics using a POS tagger and regex
    :param text: The text to search in (string)
    :param pos_tagger: spaCy Language object
    :return: list of compounds found in the input text
    """
    # process the text with the spaCy Language object
    tags = pos_tagger(text)

    # join all tokens to their POS tag, like cat_NN
    tagged_text = ' '.join(['_'.join((token.text, token.tag_)) for token in tags])

    # regex to find compounds where both words are tagged NN or NNS, & surrounding words don't have noun-like tags
    regex = r"(?<!(_NN|NNS)) ((\w+)_NN[S]?(?!P) (\w+)_NN(?!P))(?!( [\w]+?_NN(?!P)))"

    # look for word pairs that match our noun compound criteria
    compounds = [' '.join((match.group(3), match.group(4))) for match in re.finditer(regex, tagged_text) if (match.group(3) != match.group(4))]

    return compounds

def find_and_save_compounds(top_dir, save_dir, year):
    """
    Finds all compounds in a file given a year (year is contained in filename)
    :param top_dir: Directory where text file is
    :param save_dir: Directory where we want to save the text file with compounds
    :param year: Year for which we want to find compounds
    :return: None
    """
    all_compounds = []
    pos_tagger = spacy.load('en_core_web_sm')
    print(f'Starting compound extraction for year {year}')
    filename = f'COCA_{year}.txt'
    filepath = os.path.join(top_dir, filename)

    # find compounds in each line of the text file
    with tqdm.tqdm(total=os.path.getsize(filepath)) as pbar:
        for line in open(filepath, 'r'):
            all_compounds.extend(get_compounds(line, pos_tagger))
            pbar.update(len(line.encode('utf-8')))
    filename = f'COCA_{year}_all_compound_tokens.txt'
    filepath = os.path.join(save_dir, filename)

    # save compounds, one on each line, in text file
    with open(filepath, 'w') as outfile:
        for compound in all_compounds:
            outfile.write(f'{compound} \n')
    print(f'Saved file: {filepath}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_dir', default='test_COCA', required=False)
    parser.add_argument('--start_year', default=1999, required=False, type=int,
                        help='Start of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--end_year', default=2000, required=False, type=int,
                        help='End of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--data_name', default='train', required=False)
    parser.add_argument('--save_dir', default='test_COCA', required=False,
                        help='Path to directory where you want to save the count & compound files')

    args = parser.parse_args()

    top_dir, start_year, end_year, data_name, save_dir = \
        args.top_dir, args.start_year, args.end_year, args.data_name, args.save_dir

    print(f'cpu count: {mp.cpu_count()}')

    pool_args = ((top_dir, save_dir, year) for year in range(start_year, end_year + 1))

    # we use multiprocessing to speed up the compound search process
    with mp.Pool(mp.cpu_count()-1) as pool:
        pool.starmap(find_and_save_compounds, pool_args)

if __name__ == '__main__':
    main()