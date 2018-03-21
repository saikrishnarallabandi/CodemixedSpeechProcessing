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
iconv -f utf8 -t ascii//TRANSLIT//IGNORE data/train/text_pruned | tr '?' ' ' > data/train/text || exit 0
#unaccent ISO-8859-1 < data/train/text_pruned > data/train/text || exit 0
echo "Copied text"


# Copy wav info # Copy only if length of wav is > 1 sec
rm -rf data/train/wav.scp
cat data/train/text | awk '{print $1}'| cut -d'-' -f 2 | while read line; 
do 
  echo miami-$line /home3/srallaba/data/Spanish_English_data/segments_wav/$line.wav >> data/train/wav.scp
done

# Prune based on wav too
wav-to-duration --read-entire-file scp:data/train/wav.scp ark,t:- > /tmp/wav_dur || exit 0
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
rm -r data/local
mkdir -p data/local/tmp
cut -f2- -d' ' < data/train_tr95/text > data/local/tmp/corpus.txt
#ngram-count  -order 3 -write-vocab data/local/vocab-full.txt -wbdiscount -text data/local/tmp/corpus.txt -lm data/local/lm.arpa
ngram-count -order 3 -write-vocab data/local/vocab-full.txt -text data/local/tmp/corpus.txt -prune 0.0000001 -map-unk "<UNK>" -kndiscount -interpolate -lm data/local/lm.arpa

cut -f2- -d' ' < data/train_cv05/text > test_corpus.txt
ngram -lm data/local/lm.arpa -ppl test_corpus.txt

mkdir -p data/local/dict
cp spanish_cmudict.txt data/local/dict/dict.txt

# OOV words
awk 'NR==FNR{words[$1]; next;} !($1 in words)' data/local/dict/dict.txt data/local/vocab-full.txt | egrep -v '<.?s>' > data/local/dict/vocab-oov.txt
awk 'NR==FNR{words[$1]; next;} ($1 in words)' data/local/vocab-full.txt data/local/dict/dict.txt | egrep -v '<.?s>' > data/local/dict/lexicon-iv.txt

# Lexicon
# Handle OOVs
cat data/local/dict/vocab-oov.txt | sed 's/-pau-//' | sed 's/<UNK>//' > oovs
rm -f pron_oovs
sed -i '/^$/d'  oovs
cat oovs | while read line; do pron=`./festival2spanishphones $line`; echo $line $pron >> pron_oovs; done
cat pron_oovs data/local/dict/lexicon-iv.txt | sort > data/local/dict/lexicon.txt

( echo SIL; echo SPN ) > data/local/dict/silence_phones.txt
echo SIL > data/local/dict/optional_silence.txt

grep -v -w sil data/local/dict/lexicon.txt | awk '{for(n=2;n<=NF;n++) { p[$n]=1; }} END{for(x in p) {print x}}'  | sort > data/local/dict/nonsilence_phones.txt

echo "--- Adding SIL to the lexicon ..."
echo -e "!SIL\tSIL" >> data/local/dict/lexicon.txt
echo -e '-pau-	SIL' >> data/local/dict/lexicon.txt
echo -e '<unk>	SPN' >> data/local/dict/lexicon.txt

./utils/prepare_lang.sh data/local/dict '<unk>' data/local/lang data/lang || exit 0
touch  data/local/dict/extra_questions.txt

# FST
test=data/lang_test
mkdir -p $test
for f in phones.txt words.txt phones.txt L.fst L_disambig.fst phones; do     cp -r data/lang/$f $test; done
cat data/local/lm.arpa | arpa2fst --disambig-symbol=#0 --read-symbol-table=data/lang_test/words.txt - data/lang_test/G.fst
fstisstochastic data/lang_test/G.fst 


. ./train_acousticmodels.sh

