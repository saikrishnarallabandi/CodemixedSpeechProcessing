#!/bin/bash

#### Source stuff
. ./cmd.sh
. ./path.sh

#### Create Stuff
rm -r data
mkdir -p data/train data/test
mkdir -p local

#### Copy stuff
ln -s ../../wsj/s5/steps/
ln -s ../../wsj/s5/utils/
cp ../../wsj/s5/cmd.sh .
cp ../../wsj/s5/path.sh .
cp -r ../../wsj/s5/conf/ .
cp ../../voxforge/s5/conf/decode.config conf
cp ../../yesno/s5/local/score.sh local/
cp -r ../../gale_arabic/s5/local/nnet local



# Copy text
python2 copy_text.py
python2 prune_text.py
iconv -f utf8 -t ascii//TRANSLIT//IGNORE data/train/text_pruned > data/train/text || exit 0
#unaccent ISO-8859-1 < data/train/text_pruned > data/train/text || exit 0
echo "Copied text"


# Copy wav info # Copy only if length of wav is > 1 sec
rm -rf data/train/wav.scp
cat data/train/text | awk '{print $1}'| cut -d'-' -f 2 | while read line; 
do 
  echo miami-$line /home3/srallaba/data/Spanish_English_data/segments_wav/$line.wav >> data/train/wav.scp
done

# Prune based on wav too
python2 prune_wav.py || exit 0
cp data/train/wav.scp_pruned data/train/wav.scp

# Generate utt2spk
cut -d ' ' -f 1 data/train/text > utterances.train
cut -d ' ' -f 1 data/train/text  > speakers.train
paste utterances.train speakers.train > data/train/utt2spk

# Generate spk2utt
./utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt 

# Verify that things are ok
./utils/fix_data_dir.sh data/train 

# Split the data into train and test
utils/subset_data_dir_tr_cv.sh --cv-spk-percent 5 data/train data/train_tr95 data/train_cv05

# Okay. Lets extract features
mfccdir=mfcc

# Generate the fbank features; by default 40-dimensional fbanks on each frame
for set in train_tr95 train_cv05; do
  steps/make_mfcc.sh --cmd "run.pl" --nj 20 data/$set exp/make_mfcc/$set $mfccdir || exit 1;
  utils/fix_data_dir.sh data/$set || exit;
  steps/compute_cmvn_stats.sh data/$set exp/make_mfcc/$set $mfccdir || exit 1;
done

# Test the language model
mkdir -p data/local/tmp
cut -f2- -d' ' < data/train_tr95/text > data/local/tmp/corpus.txt
#ngram-count  -order 3 -write-vocab data/local/vocab-full.txt -wbdiscount -text data/local/tmp/corpus.txt -lm data/local/lm.arpa
ngram-count -order 3 -write-vocab data/local/vocab-full.txt -text data/local/tmp/corpus.txt -prune 0.0000001 -map-unk "<UNK>" -kndiscount -interpolate -lm data/local/lm.arpa

cut -f2- -d' ' < data/train_cv05/text > test_corpus.txt
ngram -lm data/local/lm.arpa -ppl test_corpus.txt

