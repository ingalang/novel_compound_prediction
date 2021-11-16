import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', required=True, type=str)

    args = parser.parse_args()

    filename = args.infile
    print(filename)
    

if __name__ == '__main__':
    main()
