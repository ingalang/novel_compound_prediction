import argparse
import random
from itertools import chain
import os
import copy

def corrupt_compound(compound, new_constituent, new_constituent_type):
    assert new_constituent_type in ['mods', 'heads'], 'constituent_type must be either mods or heads'
    mod, head = compound.split()
    if mod == new_constituent or head == new_constituent:
        return False
    if new_constituent_type == 'mods':
        return ' '.join((new_constituent, head))
    else:
        return ' '.join((mod, new_constituent))

def generate_corruped_samples(compound, n, constituent_type, constituent_list, attested_compounds, generated_compounds):
    assert constituent_type in ['mods', 'heads'], 'constituent_type must be either mods or heads'
    corrupted_samples_complete = False
    num_new_compounds = 0
    const_dict = {word : 0 for word in copy.deepcopy(constituent_list)}

    if constituent_type == 'mods':
        constituent_to_delete = compound.split()[1]
    else:
        constituent_to_delete = compound.split()[0]

    const_dict.pop(constituent_to_delete, None)

    while not corrupted_samples_complete:
        new_constituents = random.sample(const_dict.keys(), n * 2)
        for word in new_constituents:
            new_compound = corrupt_compound(compound, word, constituent_type)
            if new_compound \
                    and new_compound not in attested_compounds \
                    and new_compound not in generated_compounds:
                generated_compounds[new_compound] = 0
                num_new_compounds += 1
                if num_new_compounds >= n:
                    corrupted_samples_complete = True
                    break
    return generated_compounds

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_path', type=str, required=True,
                        help='Path to .txt file with original compound list to make corrupted samples from')
    parser.add_argument('--n', type=int, default=10,
                        help='Number of corrupted samples to make per compound')
    parser.add_argument('--out_dir', type=str, required=True,
                        help='Directory where you want to save the files containing the corrupted samples')
    parser.add_argument('--constituent', type=str, required=True, choices=['mods', 'heads'],
                        help='Which constituent to corrupt (mods or heads)')

    args = parser.parse_args()

    in_path, n, out_dir, constituent = args.in_path, args.n, args.out_dir, args.constituent

    with open(in_path, 'r') as infile:
        compound_list = [line.strip('\n\r') for line in infile]

    compound_dict = {comp : 0 for comp in compound_list}

    if constituent == 'mods':
        constituent_list = [comp.split()[0] for comp in compound_list]
    else:
        constituent_list = [comp.split()[1] for comp in compound_list]

    print('Generating corrupted compounds...')
    corrupted_compounds = {}
    for compound in compound_list:
        corrupted_compounds = generate_corruped_samples(compound, n, constituent, constituent_list, compound_dict, corrupted_compounds)

    corrupted_compounds = list(corrupted_compounds.keys())

    compound_lists_divided = [corrupted_compounds[i: len(corrupted_compounds): n] for i in range(0, n)]

    for i in range(len(compound_lists_divided)):
        filename = 'corrupted_{}_{}_{}.txt'.format(constituent, n, i)
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'w') as outfile:
            for comp in compound_lists_divided[i]:
                outfile.write(comp + '\n')


if __name__ == '__main__':
    main()