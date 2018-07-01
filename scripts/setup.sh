
# Setup the directory structure
mkdir -p data  feats  kitchen  logs  repos  scripts  tools

# Download the repo
cd repos
git clone https://github.com/saikrishnarallabandi/CodemixedSpeechProcessing
cd ../scripts

# Populate the scripts folder
cp ../repos/scripts/01_get_span_stats.py .
cp ../repos/scripts/02_seggregate_span_classes.py .
cd ..

# Download data
wget http://tts.speech.cs.cmu.edu/rsk/codemixed_stuff/data/miami.tdd
cd ../scripts

# Run it!!
python2 01_get_span_stats.py
python2 02_seggregate_span_classes.py

# Look at the files stats.txt, styles.txt and styles_num.txt


