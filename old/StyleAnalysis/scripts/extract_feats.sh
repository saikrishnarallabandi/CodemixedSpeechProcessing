#!/bin/bash

#### Create Stuff
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

#### Source stuff
. ./cmd.sh
. ./path.sh

# Text
python2 copy_text.py

rm -f data/train/wav.scp
for file in /home3/srallaba/projects/codeswitchedspeechprocessing/style_analysis/cmu_us_miami/wav/*
  do 
     fname=$(basename "$file" .wav) 
     echo miami-$fname $file >> data/train/wav.scp
  done
echo "Generated wav.scp"

# Generate utt2spk
cut -d ' ' -f 1 data/train/text > utterances.train
cut -d ' ' -f 1 data/train/text | cut -d '-' -f 2 > speakers.train
paste utterances.train speakers.train > data/train/utt2spk

# Generate spk2utt
./utils/utt2spk_to_spk2utt.pl data/train/utt2spk > data/train/spk2utt 

# Check for errors
./utils/fix_data_dir.sh data/train 

# Split into train and test
# Make subset of data
utils/subset_data_dir.sh data/train 1000 data/train.1k 
utils/subset_data_dir.sh data/train 100 data/test.100 
