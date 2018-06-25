** Let us start with Miami corpus first. **

Corpus can be obtained here: http://bangortalk.org.uk/speakers.php?c=miami

We need to preprocess the data and divide it into multi speaker segments first. This was done based on the transcription. If you dont want to do this from scratch, you can download a copy from here: http://tts.speech.cs.cmu.edu/rsk/codemixed_stuff/data/Spanish_English_data_miami_25June2018.tar.gz

Then, run the following:

1) Segment data into individual files: python 01_segment_files.py
2) Get a txt.done.data file : python 01_get_txtdonedata.py
