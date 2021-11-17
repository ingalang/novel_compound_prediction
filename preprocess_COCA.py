import argparse
import os
import re

def iter_files(top_dir, year):
    join = os.path.join
    for name in os.listdir(top_dir):
        if str(name).startswith('text_') and os.path.isdir(join(top_dir, name)):
            subdir = join(top_dir, name)
            for filename in os.listdir(subdir):
                if year in filename:
                    with open(join(subdir, filename)) as infile:
                        yield (join(subdir, filename))

class CorpusReader(object):
    def __init__(self, top_dir, year):
        self.top_dir = top_dir
        self.year = year

    def __iter__(self):
        for filepath in iter_files(self.top_dir, self.year):
            with open(filepath, 'r') as infile:
                yield infile.read()

def get_preprocessed_sentences(text):
    url_reg = re.compile('(http [\s\W]*|www [\s\W]*)\S+|<p>|[@]+\w*|^\s+')
    whitespace_reg = re.compile('\s+')
    sentences = text.split(' . ')
    return [re.sub(whitespace_reg, ' ', re.sub(url_reg, '', sent)) for sent in sentences]

def save_sentences_to_file(sentences, year, out_dir):
    filename = f'COCA_{year}.txt'
    print(f'Saving sentences to file {filename} ...')
    filepath = os.path.join(out_dir, filename)
    if os.path.exists(filepath):
        mode = 'a'
    else:
        mode = 'w'
    with open(filepath, mode) as outfile:
        for i in range(len(sentences)):
            if i == len(sentences) - 1:
                outfile.write(sentences[i] + ' \n')
            else:
                outfile.write(sentences[i] + ' . \n')
    print(f'Successfully saved all sentences to {filepath}')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', required=True, help='What year from COCA to process')
    parser.add_argument('--in_dir', required=False, default='test_COCA',
                        help='Directory to read COCA files from')
    parser.add_argument('--out_dir', required=True, type=str, help='Directory to store pre-processed files to')
    parser.add_argument('--join_compounds', action='store_true',
                        help='Whether or not to join compounds into one N_N construction after pre-processing')


    args = parser.parse_args()
    year, in_dir, out_dir = args.year, args.in_dir, args.out_dir

    coca_files = CorpusReader(in_dir, year)

    for text in coca_files:
        sentences = get_preprocessed_sentences(text)
        save_sentences_to_file(sentences, year, out_dir)


if __name__ == '__main__':
    main()