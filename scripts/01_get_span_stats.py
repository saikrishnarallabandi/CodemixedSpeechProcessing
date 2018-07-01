import os

lab_file = '../data/miami.tdd'
spanish_spans = []
english_spans = []
f = open(lab_file)
g = open('../logs/stats.txt','w')
g.write('utt_name eng_spans spanish_spans num_words dom_lang' + '\n')

for line in f:
    current_tag = 'this'
    english_span = 0
    spanish_span = 0
    num_words = 0
    fname = line.split('\n')[0].split()[0]
    line = line.split('\n')[0].split()[1:]
    print fname, line
    for word in line:
     if len(word.split('_')) > 1: 
        #print word
        num_words += 1
        tag = word.split('_')[-1]
        if tag == 'spa':
          if current_tag == 'spanish':
              spanish_span += 1
          elif current_tag == 'english':
              # This means english span has ended
              spanish_span += 1
          elif current_tag == 'this':
              # This is the first word
              spanish_span += 1
          current_tag = 'spanish'
        elif tag == 'eng':
           if current_tag == 'english':
              english_span += 1
           elif current_tag == 'spanish':
              # This means spanish span has ended
              english_span +=1
           elif current_tag == 'this':
              # This is the first word
              english_span += 1
           current_tag = 'english'
        else:
          print "Ignoring", tag
    if english_span > spanish_span:
        dom_lang = 'eng'
    else:
        dom_lang = 'spa'
    g.write(fname + ' ' + str(english_span) + ' ' + str(spanish_span) + ' ' + str(num_words) + ' ' + dom_lang + '\n')

g.close()


