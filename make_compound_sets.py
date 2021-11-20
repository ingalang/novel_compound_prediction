from compound_counts import load_compounds, singularize_heads
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_dir', default='test_COCA', required=False)
    parser.add_argument('--start_year', default=1999, required=False, type=int,
                        help='Start of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--end_year', default=2000, required=False, type=int,
                        help='End of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--save_dir', default='test_COCA', required=False,
                        help='Path to directory where you want to save the count & compound files')
    parser.add_argument('--data_name', required=True, type=str, help='What kind of dataset you are making (train, dev, test)')

    args = parser.parse_args()

    top_dir, start_year, end_year, save_dir, data_name = \
        args.top_dir, args.start_year, args.end_year, args.save_dir, args.data_name
    assert(data_name in ['train', 'dev', 'test']), "argument --data_name must be either train, dev, or test"

    all_compounds = []

    for year in range(start_year, end_year + 1):
        compound_list = load_compounds(top_dir, year)
        singularized_compounds = singularize_heads(compound_list)
        all_compounds.extend(singularized_compounds)

    compound_set = {*all_compounds}
    filepath = os.path.join(save_dir, f'COCA_{data_name}.txt')
    with open(filepath, 'w') as outfile:
        for compound in compound_set:
            outfile.write(f'{compound} \n')


if __name__ == '__main__':
    main()