import argparse
import random
from itertools import chain
import os

def corrupt_compound(compound, new_constituent, new_constituent_type):
    assert new_constituent_type in ['mods', 'heads'], 'constituent_type must be either mods or heads'
    mod, head = compound.split()
    if new_constituent_type == 'mods':
        return ' '.join((new_constituent, head))
    else:
        return ' '.join((mod, new_constituent))

def generate_corruped_samples(compound, n, constituent_type, constituent_list, attested_compounds):
    assert constituent_type in ['mods', 'heads'], 'constituent_type must be either mods or heads'
    corrupted_samples = []
    corrupted_samples_complete = False

    while not corrupted_samples_complete:
        new_constituents = random.sample(constituent_list, n*2)
        for word in new_constituents:
            new_compound = corrupt_compound(compound, word, constituent_type)
            if new_compound not in attested_compounds:
                corrupted_samples.append(new_compound)
                if len(corrupted_samples) >= n:
                    corrupted_samples_complete = True
                    break
    return corrupted_samples

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_path', type=str, required=True,
                        help='Path to .txt file with original compound list to make corrupted samples from')
    parser.add_argument('--n', type=int, default=5,
                        help='Number of corrupted samples to make per compound')
    parser.add_argument('--out_dir', type=str, required=True,
                        help='Directory where you want to save the files containing the corrupted samples')
    parser.add_argument('--constituent', type=str, required=True, choices=['mods', 'heads'],
                        help='Which constituent to corrupt (mods or heads)')

    args = parser.parse_args()

    in_path, n, out_dir, constituent = args.in_path, args.n, args.out_dir, args.constituent

    with open(in_path, 'r') as infile:
        compound_list = [line.strip('\n\r') for line in infile]

    print(compound_list)
    compound_dict = {comp : 0 for comp in compound_list}

    if constituent == 'mods':
        constituent_list = [comp.split()[0] for comp in compound_list]
    else:
        constituent_list = [comp.split()[1] for comp in compound_list]

    print('Generating corrupted compounds...')
    corrupted_compounds = list(chain.from_iterable([generate_corruped_samples(compound, n, constituent, constituent_list, compound_dict)
                                 for compound in compound_list]))
    print(len(corrupted_compounds))
    print(corrupted_compounds)

    compound_lists_divided = [corrupted_compounds[i: len(corrupted_compounds): n] for i in range(0, n)]

    for i in range(len(compound_lists_divided)):
        filename = f'corrupted_{constituent}_{n}_{i}.txt'
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'w') as outfile:
            for comp in compound_lists_divided[i]:
                outfile.write(comp + '\n')


if __name__ == '__main__':
    main()