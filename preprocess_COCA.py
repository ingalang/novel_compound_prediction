import argparse
import os

def iter_files(top_dir, year):
    join = os.path.join
    for name in os.listdir(top_dir):
        if str(name).startswith('text_') and os.path.isdir(join(top_dir, name)):
            subdir = join(top_dir, name)
            for filename in os.listdir(subdir):
                if year in filename:
                    with open(join(subdir, filename)) as infile:
                        print(join(subdir, filename))
                        yield infile.read()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', required=True, help='What year from COCA to process')
    parser.add_argument('--in_dir', required=False, default='/idiap/resource/database/COCA',
                        help='Directory to read COCA files from')
    parser.add_argument('--out_dir', required=True, type=str, help='Directory to store pre-processed files to')
    parser.add_argument('--join_compounds', action='store_true',
                        help='Whether or not to join compounds into one N_N construction after pre-processing')


    args = parser.parse_args()
    year, indir = args.year, args.in_dir

    iter_files(indir, year)

if __name__ == '__main__':
    main()