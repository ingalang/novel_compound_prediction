from compound_counts import load_compounds, singularize_heads
import argparse
import os
import numpy as np

def load_dataset(dir, data_name):
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
                        help='Path to directory where you want to save the count & compound files')
    parser.add_argument('--data_name', required=True, type=str, help='What kind of dataset you are making (train, dev, test)')

    args = parser.parse_args()

    top_dir, start_year, end_year, save_dir, data_name = \
        args.top_dir, args.start_year, args.end_year, args.save_dir, args.data_name
    assert(data_name in ['train', 'dev', 'test']), "argument --data_name must be either train, dev, or test"

    all_compounds = []

    for year in range(start_year, end_year + 1):
        print(f'Processing compounds from year {year}')
        compound_list = load_compounds(top_dir, year)
        singularized_compounds = singularize_heads(compound_list)
        all_compounds.extend(singularized_compounds)

    unique_compounds = list({*all_compounds})

    if data_name == 'dev':
        train_data = load_dataset(save_dir, 'train')
        print('Making train dict...')
        train_dict = {word.strip('\n\r') : 0 for word in train_data}
        print('Making set of compounds for dev set that are not in train set...')
        unique_compounds = [comp for comp in unique_compounds if comp not in train_dict]
    elif data_name == 'test':
        print('Making train dict...')
        train_data = load_dataset(save_dir, 'train')
        train_dict = {word.strip('\n\r'): 0 for word in train_data}

        print('Making dev dict...')
        dev_data = load_dataset(save_dir, 'dev')
        dev_dict = {word.strip('\n\r'): 0 for word in dev_data}

        unique_compounds = [compound.strip() for compound in unique_compounds
                        if compound.strip() not in train_dict and compound not in dev_dict]
    print(f'Saving file as: COCA_{data_name}.txt')
    filepath = os.path.join(save_dir, f'COCA_{data_name}.txt')
    with open(filepath, 'w') as outfile:
        for compound in unique_compounds:
            outfile.write(f'{compound}\n')


if __name__ == '__main__':
    main()