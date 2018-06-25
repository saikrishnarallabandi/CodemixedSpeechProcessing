import os
import scipy.stats as stats
import numpy as np

segments_folder = '/home2/srallaba/data/Spanglish/segments_lab'
files = sorted(os.listdir(segments_folder))


text_array = []
g = open('miami.txt','w')
h = open('miami_filenames.txt','w')
for file in files:
    print 'Processing ', file
    with open(segments_folder + '/' + file) as f:
        lines = f.readlines()
    line = lines[0].split('\n')[0]
    print line 
    s = ' ' 
    for word in line.split():
        if '_' in word:
           s += ' ' + word.split('_')[0]
    print s, len(s.split())
    if len(s.split()) > 3:
      g.write(s + '\n')
      h.write(file + ' ' + s + '\n')
      print "Written"
g.close()    
    
