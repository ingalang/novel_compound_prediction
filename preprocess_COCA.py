import argparse
import os
import re

def iter_files(top_dir, year):
    join = os.path.join
    for name in os.listdir(top_dir):
        if str(name).startswith('text_') and os.path.isdir(join(top_dir, name)):
            subdir = join(top_dir, name)
            for filename in os.listdir(subdir):
                print(subdir)
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
    url_reg = re.compile('(http [\s\W]*|www [\s\W]*)\S+|<p>|[@]+\w*')
    whitespace_reg = re.compile('\s+')
    sentences = text.split(' . ')
    return [re.sub(whitespace_reg, ' ', re.sub(url_reg, '', sent)) for sent in sentences]

def save_sentences_to_file(sentences, year, out_dir):
    filename = f'COCA_{year}.txt'
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

    test_text = '<p> She has lost some friends over the Knicks , when she turned down invitations to weddings and ' \
                'graduations because they conflicted with the playoffs . These sacrifices , however , have repaid her , ' \
                'she says , with new friends who share her obsession : sports writers , team officials , season ' \
                'ticket-holders and other fans . <p> " What has happened through the years is that the Knicks have ' \
                'become my social life , " she said . <p> http : //www.nytimes.com @@3000697 <p> Like a generation ' \
                'of baby boomers celebrating their 50th birthdays , the Ladies Professional Golf Association has ' \
                'taken a hard look in the mirror and , for the most part , likes the image it sees . <p> It ' \
                'is bigger than ever , financially strong , still attractive to sponsors and the object of ' \
                'unprecedented exposure in the news media . Total prize money grew from $17.1 million in 1990 ' \
                'to more than $36.2 million in 1999 . <p> At the same time , tour events rose from 38 to 43 and ' \
                'televised coverage increased from 15 events in 1990 to 35 in 1999 . <p> \" We \'re on television more ' \
                'than 250 hours ; that \'s more than any other women \'s pro sport , \" said Ty Votaw , ' \
                'the L.P.G.A. commissioner .'

    for text in coca_files:
        sentences = get_preprocessed_sentences(text)
        save_sentences_to_file(sentences, year, out_dir)


if __name__ == '__main__':
    main()