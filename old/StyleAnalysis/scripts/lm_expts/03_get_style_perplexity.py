import os

all_file = 'miami_filenames.txt'
styles_file = 'cmi_miami.styles'


styles_dict = {}
text_dict = {}

f = open(all_file)
for line in f:
   line = line.split('\n')[0]
   fname = line.split()[0]
   content = line.split()[1:]
   text_dict[fname] = content
f.close()

f = open(styles_file)
for line in f:
   line = line.split('\n')[0]
   fname = line.split()[0]
   content = line.split()[1]
   styles_dict[fname] = content
f.close()


for i in range(1,6):
    style_content = []
    g = open('styletext_cmi_' + str(i).zfill(3) + '.txt','w')
    for (k,v) in styles_dict.iteritems():
        if int(v) == i:
           try:
             style_content.append(text_dict[k])
             g.write(' '.join(k for k in text_dict[k]) + '\n')
           except KeyError:
             pass
    g.close()
    length = len(style_content)
    print "Processing CM Style ", i
    cmd = 'sh build_test_lm.sh ' +  'styletext_cmi_' + str(i).zfill(3) + '.txt ' + 'lm_styletext_cmi_' + str(i).zfill(3) + '.arpa ' + str(int(length/10))    
    print cmd
    os.system(cmd)
    print '\n'



cmd = 'ngram -order 3 -lm lm_styletext_cmi_001.arpa -mix-lm lm_styletext_cmi_002.arpa -mix-lm lm_styletext_cmi_003.arpa -mix-lm lm_styletext_cmi_004.arpa -mix-lm lm_styletext_cmi_005.arpa -write-lm mixlm.arpa'
os.system(cmd)

