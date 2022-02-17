import os
import spacy
import argparse
import multiprocessing as mp
import re
import tqdm

def get_compounds(text, pos_tagger):
    tags = pos_tagger(text)
    tagged_text = ' '.join(['_'.join((token.text, token.tag_)) for token in tags])
    regex = r"(?<!(_NN|NNS)) ((\w+)_NN[S]?(?!P) (\w+)_NN(?!P))(?!( [\w]+?_NN(?!P)))"
    compounds = [' '.join((match.group(3), match.group(4))) for match in re.finditer(regex, tagged_text) if (match.group(3) != match.group(4))]
    return compounds

def find_and_save_compounds(top_dir, save_dir, year):
    all_compounds = []
    pos_tagger = spacy.load('en_core_web_sm')
    print(f'Starting compound extraction for year {year}')
    filename = f'COCA_{year}.txt'
    filepath = os.path.join(top_dir, filename)
    with tqdm.tqdm(total=os.path.getsize(filepath)) as pbar:
        for line in open(filepath, 'r'):
            all_compounds.extend(get_compounds(line, pos_tagger))
            pbar.update(len(line.encode('utf-8')))
    filename = f'COCA_{year}_all_compound_tokens.txt'
    filepath = os.path.join(save_dir, filename)
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

    with mp.Pool(mp.cpu_count()-1) as pool:
        pool.starmap(find_and_save_compounds, pool_args)

if __name__ == '__main__':
    main()