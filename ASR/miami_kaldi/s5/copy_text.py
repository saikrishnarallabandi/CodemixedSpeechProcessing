import os

# Copy Text
transcription_file = '/home3/srallaba/data/Spanish_English_data/segments.txt'
f = open(transcription_file)
g = open('data/train/text','w')
for line in f:
    line = line.split('\n')[0]
    filenum = line.split()[0]
    duration = float(line.split()[2]) - float(line.split()[1])
    if duration > 3.0:
      content = ' '.join(k.split('_')[0] for k in line.split()[4:])
      g.write( 'miami-' + filenum + ' '  + content + '\n')
g.close()








