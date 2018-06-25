#/bin/bash

# sh build_test_lm.sh full.txt lm.arpa 1000

# Shuffle and pick 1000 sentences randomly
input=$1
sort $input > t.txt
shuf -n $3 $input > test.txt
sort test.txt > test_sorted.txt
comm -23 t.txt test_sorted.txt  > train.txt

# Build and test LM
ngram-count  -order 3 -wbdiscount -interpolate -text train.txt -lm $2
ngram -lm $2 -ppl test.txt
ngram -lm mixlm.arpa -ppl test.txt
