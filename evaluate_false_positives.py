from googlesearch import search
import googlesearch
import argparse
import time
import urllib
from urllib.error import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import json

def save_compound_hits(compound_hits_dict, filepath):
    with open(filepath, 'w') as outfile:
        json.dump(compound_hits_dict, outfile)
        print(f'Saved {filepath}')



def find_hits_for_compound(compound):
    response = search('"' + compound + '"', user_agent=googlesearch.get_random_user_agent(), stop=2000, pause=5.0)
    responses_list = [r for r in response]
    print(f'the compound \"{compound}\" got {len(responses_list)} hits on Google!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', required=False, default='test_COCA/COCA_dev.txt',
                        help='Path to the file of generated compounds '
                                    '(in .txt format, with one compound per line) that you want to check')

    args = parser.parse_args()
    filepath = args.f

    with open(filepath, 'r') as infile:
        compounds = [line.strip('\n\r') for line in infile]

    save_file_as = re.sub('.txt', '', filepath) + '_counts.json'

    compound_hits = {}
    compound_tries = {}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    search_num_reg = re.compile(r'\d+(?:[^a-zA-Z0-9_]*[\d])*')
    while len(compound_hits) < len(compounds):
        for compound in compounds:
            if compound not in compound_hits:
                if compound not in compound_tries or compound_tries[compound] < 3:
                    try:
                        mod, head = compound.split()
                        result = requests.get(f'https://www.google.com/search?q=%22{mod}+{head}%22', headers=headers)
                        soup = BeautifulSoup(result.content,
                                                 "html.parser")
                        try:
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
                    except(HTTPError):
                        print(f'Server interruption when searching for \"{compound}\".')
                        save_compound_hits(compound_hits, save_file_as)
                        time.sleep(300)





if __name__ == '__main__':
    main()