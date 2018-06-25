import os

lab_file = '../heering.labels'
spanish_spans = []
english_spans = []
f = open(lab_file)

for line in f:
    current_tag = 'this'
    english_span = 0
    spanish_span = 0
    line = line.split('\n')[0].split()
    for word in line:
        tag = word.split('_')[-1]
        if tag == 'spa':
          if current_tag == 'spanish':
             spanish_span += 1
          # This means english span has ended
          english_spans.append(english_span)
          spanish_span += 1
          current_tag = 'spanish'
        elif tag == 'eng':
          if current_tag == 'english':
             english_span += 1
          # This means spanish span has ended
          spanish_spans.append(spanish_span)
          english_span +=1
          current_tag = 'english'
        else:
          print "Ignoring", tag
               

import numpy as np
np.savetxt('english_spans.txt', english_spans,fmt='%2f') #[np.nonzero(english_spans)])
np.savetxt('spanish_spans', spanish_spans,fmt='%2f') #[np.nonzero(spanish_spans)]) 
  

