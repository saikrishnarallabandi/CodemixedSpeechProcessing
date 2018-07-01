import numpy as np
import sys

'''
utt_name eng_spans spanish_spans num_words dom_lang
herring10_00001 9 6 15 eng
herring10_00002 5 0 5 eng
'''

class stats(object):

      def __init__(self, file):
          self.file = file
          self.accumulate_arrays()

      def accumulate_arrays(self):
          self.utts = []
          self.english_spans = []
          self.spanish_spans = []
          self.num_words = []
          self.dominant_language = []

          f = open(self.file)
          for ctr, line in enumerate(f):
           if ctr > 0 : 
               line = line.split('\n')[0].split()
               
               utt = line[0]
               english_span = int(line[1])
               spanish_span = int(line[2])
               num_words = int(line[3])
               dominant_language = line[4]

               if num_words > 0:
                 self.utts.append(utt)
                 self.english_spans.append(english_span)
                 self.spanish_spans.append(spanish_span)
                 self.num_words.append(num_words)
                 self.dominant_language.append(dominant_language)

      def get_elem_by_index(self, idx):
               return zip(self.utts[idx], self.english_spans[idx], self.spanish_spans[idx], self.num_words[idx], self.dominant_language[idx])

      def get_length(self):
               return len(self.utts)      

      def get_percentages(self): 
               self.dominant_percent = []
               length = self.get_length()
               for i in range(length):
                 if self.num_words[i] > 0: 
                    if self.dominant_language[i] == 'eng':
                          dominant_percent = float(self.english_spans[i]*1.0 / self.num_words[i]*1.0 )
                    elif self.dominant_language[i] == 'spa':
                          dominant_percent = float(self.spanish_spans[i]*1.0 / self.num_words[i]*1.0 )
                    else:
                          print "Okay. This is crazy"
                          sys.exit()
                    self.dominant_percent.append(dominant_percent)
                 else:
                    print " This utt is crazy: ", self.utts[i]
    
st = stats('../logs/stats.txt')
length = st.get_length()
st.get_percentages()
g = open('../logs/styles.txt','w')
h = open('../logs/styles_num.txt','w') 
for i in range(length):
    lang = st.dominant_language[i]
    percent = st.dominant_percent[i]
    if lang == 'eng' and percent > 0.99:
        g.write(st.utts[i] + ' mono_eng' + '\n')
        h.write(st.utts[i] + ' 0' + '\n')

    elif lang == 'eng' and percent > 0.7 and percent < 1.0:
                  g.write(st.utts[i] + ' dom_eng' + '\n')
                  h.write(st.utts[i] + ' 1' + '\n')

    elif lang == 'spa' and percent > 0.7 and percent < 1.0:
                  g.write(st.utts[i] + ' dom_spa' + '\n')
                  h.write(st.utts[i] + ' 2' + '\n')

    elif lang == 'eng' and percent > 0.99:
                  g.write(st.utts[i] + ' mono_spa' + '\n')
                  h.write(st.utts[i] + ' 3' + '\n')

    else:
                  g.write(st.utts[i] + ' mixed' + '\n')
                  h.write(st.utts[i] + ' 4' + '\n')

    
g.close() 
h.close()
