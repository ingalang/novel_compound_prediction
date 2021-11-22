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

def train_model_on_year(top_dir, model_dir, year):
    print(f'Training model on {year} data')
    previous_model_name = f'word2vec_{year - 1}.model'
    previous_model_dir = os.path.join(model_dir, previous_model_name)
    model_path = previous_model_dir if os.path.isfile(previous_model_dir) else None
    filepath = os.path.join(top_dir, f'COCA_{year}.txt')
    sentence_generator = SentenceReader(filepath)
    if model_path == None:
        print('model path is none')
        model = Word2Vec(sentence_generator, vector_size=300, window=2, min_count=5, workers=3)
    else:
        print(f'loading model from: {model_path}')
        model = Word2Vec.load(model_path)
        model.train(sentence_generator, epochs=model.epochs, total_examples=model.corpus_count)
    return model

def train_years(start_year, end_year, data_dir, model_dir):
    for i in range(start_year, end_year + 1):
        model = train_model_on_year(top_dir=data_dir, model_dir=model_dir, year=i)
        model.save(os.path.join(model_dir, f'word2vec_{i}.model'))
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

    args = parser.parse_args()
    top_dir, start_year, end_year, data_name, model_dir = \
        args.top_dir, args.start_year, args.end_year, args.data_name, args.model_dir

    train_years(start_year=start_year, end_year=end_year, data_dir=top_dir, model_dir=model_dir)

if __name__ == '__main__':
    main()