import argparse
import random
from itertools import chain
import os
import copy

def corrupt_compound(compound, new_constituent, new_constituent_type):
    """
    Corrupts a compound by swapping one constituent with another given word
    :param compound: The compound to corrupt
    :param new_constituent: The new word to put in as a substitute of one of the constituents
    :param new_constituent_type: Which constituent to change (mods, heads)
    :return: The corrupted compound, or False if it couldn't be corrupted
    """
    assert new_constituent_type in ['mods', 'heads'], 'constituent_type must be either mods or heads'
    mod, head = compound.split()

    # if corrupting the compound would result in a double constituent compound (like "shirt shirt"), return False
    if mod == new_constituent or head == new_constituent:
        return False

    # swap the right constituent for the new word, and return corrupted compound
    if new_constituent_type == 'mods':
        return ' '.join((new_constituent, head))
    else:
        return ' '.join((mod, new_constituent))

def generate_corruped_samples(compound, n, constituent_type, constituent_list, attested_compounds, generated_compounds):
    """
    For an attested compound, make n corrupted compounds by swapping modifiers or heads with other words
    :param compound: compound to make corrupted samples for
    :param n: number of corrupted samples to create
    :param constituent_type: type of constituent we are corrupting (mods or heads)
    :param constituent_list: list of other words, within the constituent category,
    to replace with (for example, if constituent_type is mods, then this is a list of all other modifiers in data
    :param attested_compounds: set of already attested compounds
    :param generated_compounds: dict of already generated corrupted compounds
    :return: dict containing corrupted compounds
    """
    assert constituent_type in ['mods', 'heads'], 'constituent_type must be either mods or heads'
    corrupted_samples_complete = False
    num_new_compounds = 0
    const_dict = {word : 0 for word in copy.deepcopy(constituent_list)}

    # Determining which word to delete from our collection of possible swaps
    # (so we don't end up with the same word that we started with)
    if constituent_type == 'mods':
        constituent_to_delete = compound.split()[1]
    else:
        constituent_to_delete = compound.split()[0]

    const_dict.pop(constituent_to_delete, None)

    while not corrupted_samples_complete:
        # get a random sample of the other constituents we have to choose from, n*2 to have a generous selection
        new_constituents = random.sample(const_dict.keys(), n * 2)

        # go through the selection of random constituents to swap with, and check if swapping
        # with each of them would create an already seen compound. If not, add to dict of generated compounds.
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

    # getting our list of constituents to swap with, which depends on whether we're swapping mods or heads
    if constituent == 'mods':
        constituent_list = [comp.split()[0] for comp in compound_list]
    else:
        constituent_list = [comp.split()[1] for comp in compound_list]

    print('Generating corrupted compounds...')
    corrupted_compounds = {}

    # generating n corrupted samples for each of our compounds
    for compound in compound_list:
        corrupted_compounds = generate_corruped_samples(compound, n, constituent, constituent_list, compound_dict, corrupted_compounds)

    corrupted_compounds = list(corrupted_compounds.keys())

    # dividing our compounds into n lists, so that each list has one corrupted version of each original
    # compound. For example, for "cat food", list 1 would have "dog food", list 2 would have "elephant food",  etc.
    compound_lists_divided = [corrupted_compounds[i: len(corrupted_compounds): n] for i in range(0, n)]

    # saving each list as a separate file
    for i in range(len(compound_lists_divided)):
        filename = 'corrupted_{}_{}_{}.txt'.format(constituent, n, i)
        filepath = os.path.join(out_dir, filename)
        with open(filepath, 'w') as outfile:
            for comp in compound_lists_divided[i]:
                outfile.write(comp + '\n')


if __name__ == '__main__':
    main()