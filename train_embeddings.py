import argparse
import os
import gensim
from gensim.models import Word2Vec
import re

class SentenceReader(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def __iter__(self):
        regex = re.compile(r'[^\w\s]')
        with open(self.filepath, 'r') as infile:
            for line in infile:
                line = re.sub(regex, '', line).lower()
                yield line.split()

def train_model_on_year(top_dir, model_dir, year, dims):
    """
    Trains word2vec model on a given year's worth of data
    :param top_dir: directory in which all the text files are located
    :param model_dir: directory where the model is located
    :param year: year from which we are using text to train on
    :param dims: number of dims we want for our embeddings
    :return: trained word2vec model
    """
    print(f'Training model on {year} data')
    previous_model_name = f'word2vec_{year - 1}_{dims}.model'
    previous_model_dir = os.path.join(model_dir, previous_model_name)
    model_path = previous_model_dir if os.path.isfile(previous_model_dir) else None
    filepath = os.path.join(top_dir, f'COCA_{year}.txt')
    sentence_generator = SentenceReader(filepath)
    if model_path == None:
        print('model path is none')
        model = Word2Vec(sentence_generator, vector_size=dims, window=2, min_count=5, workers=3)
    else:
        print(f'loading model from: {model_path}')
        model = Word2Vec.load(model_path)
        model.train(sentence_generator, epochs=model.epochs, total_examples=model.corpus_count)
    return model

def train_years(start_year, end_year, data_dir, model_dir, dims):
    """
    Goes through all years from start year to end year (inclusive) and incrementally trains and saves a word2vec model.
    :param start_year: Year at which to start
    :param end_year: Year at which to end
    :param data_dir: Directory in which we load and save our text data
    :param model_dir: Directory in which we load and save our word2vec model
    :param dims: Dimensions that we want for our embedding vectors
    :return: None
    """
    for i in range(start_year, end_year + 1):
        model = train_model_on_year(top_dir=data_dir, model_dir=model_dir, year=i, dims=dims)
        model.save(os.path.join(model_dir, f'word2vec_{i}_{dims}.model'))
        del model
        print(f'Saved model trained on data from {i}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_dir', default='test_COCA', required=False)
    parser.add_argument('--start_year', default=1999, required=False, type=int,
                        help='Start of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--end_year', default=2000, required=False, type=int,
                        help='End of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--data_name', default='train', required=False)
    parser.add_argument('--model_dir', default='test_COCA', required=False,
                        help='Path to directory where you want to save the word2vec models')
    parser.add_argument('--dims', default=300, type=int,
                        help='How many dimensions you want the word2vec vectors to be')

    args = parser.parse_args()
    top_dir, start_year, end_year, data_name, model_dir, dims = \
        args.top_dir, args.start_year, args.end_year, args.data_name, args.model_dir, args.dims

    train_years(start_year=start_year, end_year=end_year, data_dir=top_dir, model_dir=model_dir, dims=dims)

if __name__ == '__main__':
    main()