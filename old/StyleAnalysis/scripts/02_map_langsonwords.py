import os, sys


word_labs_dir = '../word_labs'
lang_labs_dir = '../lang_labs'
transcript_file = '../herring.labels'


f = open(transcript_file)
for line in f:
  try:
    line = line.split('\n')[0].split()
    fname = line[0]
    content = ' '.join(k for k in line[1:]).split()
    words = []
    h = open(word_labs_dir + '/' + fname + '.lab')
    for line in h:
        line = line.split('\n')[0].split()
        words.append(' '.join(k for k in line))
    g = open(lang_labs_dir + '/' + fname + '.lab','w')
    for (c,w) in zip(content, words):
        if c.split('_')[0] == w.split()[0]:
             g.write(c + ' ' + ' '.join(k for k in w.split()[1:]) + '\n')
        else:
             print "Something wrong Fname:", fname, "Content: ",  c, "Words: ", w
             
    g.close()
  except IOError:
    print "File seems missing", fname          

    
