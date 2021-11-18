#! /bin/sh
for i in {1999..2019}
do
   python3 preprocess_COCA.py --year $i --in_dir /idiap/resource/database/COCA --out_dir /idiap/temp/ilang/COCA_preprocessed
done