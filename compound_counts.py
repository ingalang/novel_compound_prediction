from collections import Counter
import json
import os
import inflect
import argparse

def singularize_heads(compounds: list):
    p = inflect.engine()
    singularized_compounds = []
    for comp in compounds:
        mod, head = comp.lower().split()
        singular_head = p.singular_noun(head)
        head = singular_head if singular_head else head
        singularized_compounds.append(' '.join((mod, head)))
    return singularized_compounds

def count_compounds(compounds: list):
    compound_counter = Counter(compounds)
    return dict(compound_counter)

def save_compound_counts_for_year(compounds, year, save_dir):
    singularized_compounds = singularize_heads(compounds)
    counts = count_compounds(singularized_compounds)
    with open(os.path.join(save_dir, f'compound_counts_{year}.json'), 'w') as outfile:
        json.dump(counts, outfile)

def load_compounds(top_dir, year):
    filepath = os.path.join(top_dir, f'COCA_{year}_all_compound_tokens.txt')
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
                        help='Path to directory where you want to save the count & compound files')

    args = parser.parse_args()

    top_dir, start_year, end_year, save_dir = \
        args.top_dir, args.start_year, args.end_year, args.save_dir

    for year in range(start_year, end_year + 1):
        print(f'Processing {year} data...')
        compound_list = load_compounds(top_dir, year)
        save_compound_counts_for_year(compound_list, year, save_dir)


if __name__ == '__main__':
    main()