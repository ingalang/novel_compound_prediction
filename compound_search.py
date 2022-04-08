import argparse
import json
from gensim.models import Word2Vec

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_word', type=str, required=True)
    parser.add_argument('--constituent', type=str, required=False, default='mod')
    parser.add_argument('--top_n', type=int, required=False, default=10,
                        help='how many examples to return')
    parser.add_argument('--list', type=str, required=False, default='true_positives',
                        help='which list of compounds to search in: '
                             'true_positives, false_positives, true_negatives, false_negatives')

    args = parser.parse_args()
    target_word, constituent, top_n, list_name = args.target_word, args.constituent, args.top_n, args.list

    with open('results_300/cosine_novel/{}_cosine_{}s_300hidden_50e.txt'.format(list_name, constituent), 'r') as infile:
        compound_list = [line.strip('\r\n') for line in infile]

    with open('novel_compound_origin_dict_{}s.json'.format(constituent), 'rb') as infile:
        compound_origins = json.load(infile)

    embedding_model = Word2Vec.load('word2vec_2009.model')

    comp_similarity_to_target = {}

    for comp in compound_list:
        mod, head = comp.split()
        mod_sim = embedding_model.wv.similarity(target_word, mod)
        head_sim = embedding_model.wv.similarity(target_word, head)
        comp_similarity_to_target[comp] = (mod_sim, head_sim)

    sorted_comps = [(k, v) for k, v in sorted(comp_similarity_to_target.items(), key = lambda item: max(item[1]), reverse=True)]
    for comp in sorted_comps[:top_n]:
        print('{} comes from {}. Mod similarity to {}: {} ---- head similarity to {}: {}'
              .format(comp[0], compound_origins[comp[0]], target_word, comp[1][0], target_word, comp[1][1]))




if __name__ == '__main__':
    main()