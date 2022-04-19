from googlesearch import search
import googlesearch
import argparse
import time
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import json
import random

def save_compound_hits(compound_hits_dict, filepath):
    with open(filepath, 'w') as outfile:
        json.dump(compound_hits_dict, outfile)
        print(f'Saved {filepath}')


def find_hits_for_compound(compound):
    """
    :param compound: compound to search for
    :return: number of hits on Google
    """
    response = search('"' + compound + '"', user_agent=googlesearch.get_random_user_agent(), stop=2000, pause=5.0)
    responses_list = [r for r in response]
    print(f'the compound \"{compound}\" got {len(responses_list)} hits on Google!')
    return len(responses_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', required=False, default='results_300/cosine_novel/false_positives_cosine_mods_300hidden_50e.txt',
                        help='Path to the file of generated compounds '
                                    '(in .txt format, with one compound per line) that you want to check')
    parser.add_argument('--n', required=False, default=100, help='Number of compounds to evaluate.', type=int)

    args = parser.parse_args()
    filepath, n = args.filepath, args.n

    with open(filepath, 'r') as infile:
        compounds = [line.strip('\n\r') for line in infile]

    # get a random sample of n compounds to perform google searches on
    compound_subset = random.sample(compounds, n)
    for c in compound_subset:
        print(c)
    save_file_as = re.sub('.txt', '', filepath) + '_counts.json'

    compound_hits = {}
    compound_tries = {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    search_num_reg = re.compile(r'\d+(?:[^a-zA-Z0-9_]*[\d])*')
    while len(compound_hits) < len(compound_subset):
        for compound in compound_subset:
            # only search for compounds we haven't gotten hits for yet
            if compound not in compound_hits:
                # only try a compound 3 times, otherwise consider it not found
                if compound not in compound_tries or compound_tries[compound] < 3:
                    try:
                        mod, head = compound.split()
                        # search for the compound and parse the resulting html page
                        result = requests.get(f'https://www.google.com/search?q=%22{mod}+{head}%22', headers=headers)
                        soup = BeautifulSoup(result.content,
                                                 "html.parser")
                        try:
                            # find the place where it says the number of hits for the search phrase (our compound)
                            total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False)
                        except:
                            print(f'could not parse results for this compound: {compound}')
                            if compound in compound_tries:
                                compound_tries[compound] += 1
                                print(f'tried {compound} {compound_tries[compound]} time(s)')
                            else:
                                compound_tries[compound] = 1
                                print(f'tried {compound} {compound_tries[compound]} time(s)')
                            save_compound_hits(compound_hits, save_file_as)
                            time.sleep(300)
                            continue
                        match = re.findall(search_num_reg, total_results_text)
                        result_int = int(re.sub('\D+', '', match[0]))
                        compound_hits[compound] = result_int
                    # if we get an HTTPError, it's because we're sending too many requests.
                    # Save, sleep, and try again later.
                    except(HTTPError):
                        print(f'Server interruption when searching for \"{compound}\".')
                        save_compound_hits(compound_hits, save_file_as)
                        time.sleep(300)


if __name__ == '__main__':
    main()