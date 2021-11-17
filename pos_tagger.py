import argparse
import spacy
import os

def tag_sentences(sentence_list, pos_tagger):
    tagged_sentences = []
    append = tagged_sentences.append
    for sentence in sentence_list:
        tags = pos_tagger(sentence)
        tagged_sent = ' '.join(['_'.join([word.text, word.tag_]) for word in tags])
        append(tagged_sent)
    return tagged_sentences

def join_compounds_in_sentence(sentence, pos_tagger):
    tags = pos_tagger(sentence)
    tagged_sentence = ""
    for i in range(len(tags)):
        current_token = tags[i]
        

def read_file(filename):
    with open(filename, 'r') as infile:
        text = infile.read()
    print(type(text))
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, type=str)

    args = parser.parse_args()

    filename = args.infile
    print(filename)

    test_text = read_file(filename)
    sentences = test_text.split('. ')
    print(sentences)
    print(test_text)

    pos_tagger = spacy.load('en_core_web_sm')

    tagged_sentences = tag_sentences(sentence_list=sentences, pos_tagger=pos_tagger)
    print(tagged_sentences)


if __name__ == '__main__':
    main()
