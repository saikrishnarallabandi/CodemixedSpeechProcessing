import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

feats_dir='../feats'
train_files='../data/segments/labels.txt'
f=open(train_files)


def read_wav_file(fname):
   _,wav=wavfile.read(fname)
   wav=wav.astype(np.float32)/np.iinfo(np.int16).max
   return wav

def process_file(fname):
   wav=read_wav_file(fname)
   L=16000#1sec
   print len(wav)
   if len(wav)<500: 
      print "This is problematic"
      return None, None
   specgram=stft(wav,16000,nperseg=400,noverlap=240,nfft=512,padded=False,boundary=None)
   phase=np.angle(specgram[2])/np.pi
   amp=np.log1p(np.abs(specgram[2]))

   return phase,amp


for line in f:
    line=line.split('\n')[0].split()
    fname=line[0]
    label=line[1]
    print "Processing",fname
    output_fname=feats_dir+'/'+fname.split('.wav')[0]
    if os.path.exists(output_fname + '.amp'):
       continue
    wav_file='../data/segments/wav/'+fname+'.wav'
    try: 
       phase,amp=process_file(wav_file)
       g=open(output_fname+'.output','w')
       g.write(label+'\n')
       np.savetxt(output_fname+'.phase',phase,fmt='%.7f')
       np.savetxt(output_fname+'.amp',amp,fmt='%.7f')
    except IndexError:
       print "Something wrong with this"
