import argparse
import os
import gensim
from gensim.models import Word2Vec

class SentenceReader(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def __iter__(self):
        with open(self.filepath, 'r') as infile:
            for line in infile:
                yield line

def load_model(year):
    pass

def train_model_on_year(top_dir, year, model_path=None):
    filepath = os.path.join(top_dir, f'COCA_{year}.txt')
    sentence_generator = SentenceReader(filepath)
    if model_path == None:
        model = Word2Vec(sentences=sentence_generator, size=100, window=5, min_count=5, workers=3)

def save_model(model, save_dir):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top_dir', default='test_COCA', required=False)
    parser.add_argument('--start_year', default=1999, required=False, type=int,
                        help='Start of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--end_year', default=2000, required=False, type=int,
                        help='End of the year range you want to collect compounds from (inclusive)')
    parser.add_argument('--data_name', default='train', required=False)
    parser.add_argument('--save_dir', default='test_COCA', required=False,
                        help='Path to directory where you want to save the count & compound files')

