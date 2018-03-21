#!/bin/bash

. ./cmd.sh
. ./path.sh



# Monophone system
#steps/train_mono.sh --nj 20 --cmd "run.pl" data/train_tr95 data/lang exp/mono
#utils/mkgraph.sh data/lang_test exp/mono exp/mono/graph
#steps/decode.sh --config conf/decode.config --nj 100 --cmd "run.pl" exp/mono/graph data/train_cv05 exp/mono/decode
steps/align_si.sh --nj 100 --cmd "run.pl" data/train_tr95 data/lang exp/mono/ exp/mono_ali

# Triphone
steps/train_deltas.sh --cmd "run.pl" 2000 11000 data/train_tr95/ data/lang exp/mono_ali exp/tri1
utils/mkgraph.sh data/lang_test exp/tri1 exp/tri1/graph 
steps/decode.sh --config conf/decode.config --nj 100 --cmd "run.pl" exp/tri1/graph data/train_cv05 exp/tri1/decode
steps/align_si.sh --nj 100 --cmd "run.pl"  --use-graphs true data/train_tr95 data/lang exp/tri1 exp/tri1_ali || exit 1;

# Tri2a [delta+delta-deltas]
steps/train_deltas.sh --cmd "run.pl" 2000 11000 data/train_tr95 data/lang exp/tri1_ali exp/tri2a || exit 1;
utils/mkgraph.sh data/lang_test exp/tri2a exp/tri2a/graph 
steps/decode.sh --config conf/decode.config --nj 100 --cmd "run.pl" exp/tri2a/graph data/train_cv05 exp/tri2a/decode

