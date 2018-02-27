import os
from scipy.io import wavfile as wf
import numpy as np

wav_dir = '../f0_ascii'
lang_wav_dir = '../lang_wav'
lang_lab_dir = '../lang_labs'

lab_files = sorted(os.listdir(lang_lab_dir))

for lab_file in lab_files:
  try:
    fname = lab_file.split('.')[0]
    print fname
    wav_fname = wav_dir + '/' + fname + '.f0'
    y = np.loadtxt(wav_fname)
    f = open(lang_lab_dir + '/' + lab_file)
    for line in f:
      line = line.split('\n')[0].split()
      lang = line[0]
      start_frame = int(float(line[1]) * 200)
      end_frame = int(float(line[2]) * 200)
      if '_eng' in lang:
          y[start_frame:end_frame] = 0
      else:
          y[start_frame:end_frame] = 1    
      y[y > 0.0] = 1           
      y[y< 0] = 0
      np.savetxt(lang_wav_dir + '/' + fname + '.txt' , y, fmt='%2f')         

  except IOError:
     print "Failed at ", lab_file
