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

def get_compounds_from_sentence(sentence, pos_tagger, toggle_lowercase=False):
    #TODO bør du bruke TrueCase eller noe for å fikse setninger som er i all caps??? (det er noen)
    tags = pos_tagger(sentence)
    tagged_sent = ' '.join(['_'.join([word.text, word.tag_]) for word in tags])
    print(tagged_sent)
    noun_tags = ['NN', 'NNS']
    compounds = []
    for i in range(len(tags)-1):
        first_token = tags[i]
        second_token = tags[i+1]
        if first_token.tag_ in noun_tags and second_token.tag_ in noun_tags:
            previous_token = tags[i-1].tag_ if i > 0 else 0
            next_token = tags[i+2].tag_ if i < len(tags)-2 else 0
            left_side, right_side = False, False
            if previous_token:
                if previous_token not in noun_tags:
                    left_side = True
            else:
                left_side = True
            if next_token:
                if (next_token not in noun_tags):
                    right_side = True
            else:
                right_side = True
            if left_side and right_side:
                compound = f'{first_token} {second_token}'.lower() if toggle_lowercase else f'{first_token} {second_token}'
                compounds.append(compound)
    return compounds

def read_file(filename):
    with open(filename, 'r') as infile:
        text = infile.read()
    print(type(text))
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=False, type=str, default='test.txt')

    args = parser.parse_args()

    filename = args.infile
    print(filename)

    test_text = read_file(filename)
    sentences = test_text.split('.')
    print(sentences)
    print(test_text)



    pos_tagger = spacy.load('en_core_web_sm')

    for sent in sentences:
        print("SENTENCE")
        compounds = get_compounds_from_sentence(sentence=sent, pos_tagger=pos_tagger)
        print(sent)
        print(compounds)

    tagged_sentences = tag_sentences(sentence_list=sentences, pos_tagger=pos_tagger)
    print(tagged_sentences)


if __name__ == '__main__':
    main()
