import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_path', type=str, required=True,
                        help='Path to .txt file with original compound list to make corrupted samples from')
    parser.add_argument('--n', type=int, default=10, help='Number of corrupted samples to make per compound')
    parser.add_argument('--out_dir', type=str, required=True,
                        help='Directory where you want to save the files containing the corrupted samples')

if __name__ == '__main__':
    main()