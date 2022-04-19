import json
import pandas as pd
import numpy as np
import random

def main():
    # define the constituent we are looking at
    constituent = 'mod'
    with open(f'results_300/cosine_novel/false_positives_cosine_{constituent}s_300hidden_50e.txt', 'r') as infile:
        fps = [line.strip('\n\r') for line in infile]

    with open(f'results_300/cosine_novel/false_negatives_cosine_{constituent}s_300hidden_50e.txt', 'r') as infile:
        fns = [line.strip('\n\r') for line in infile]

    with open(f'results_300/cosine_novel/true_positives_cosine_{constituent}s_300hidden_50e.txt', 'r') as infile:
        tps = [line.strip('\n\r') for line in infile]

    with open(f'results_300/cosine_novel/true_negatives_cosine_{constituent}s_300hidden_50e.txt', 'r') as infile:
        tns = [line.strip('\n\r') for line in infile]


    print(len(fps))
    print(len(tps))
    print(len(tns))
    print(len(fns))

    print()
    print(len(tps)+len(fps))
    print(len(tns)+len(fns))
    print(len(np.concatenate((fns, tns), 0)))

    print('random sample of positively classified compounds:')
    random_pos = random.sample(tps+fps, 100)
    for comp in random_pos:
        print(comp)

    print('random sample of negatively classified compounds:')
    random_pos_n = random.sample(tns+fns, 100)
    for comp in random_pos_n:
        print(comp)

if __name__ == '__main__':
    main()