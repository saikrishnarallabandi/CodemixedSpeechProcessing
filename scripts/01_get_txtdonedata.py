

transcript = '../herring.done.data'
g = open('../etc/txt.done.data','w')
f = open(transcript)
for line in f:
    line = line.split('\n')[0].split()
    fname = line[0]
    content = ' '.join(k for k in line[1:])
    g.write('( ' + fname + ' " ' + content + ' " )' + '\n')
g.close()  
