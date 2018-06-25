#!/usr/bin/python
import os

text_file = 'data/train/text'
cmd = 'cp ' + text_file + ' /tmp/t'
os.system(cmd)

f = open('/tmp/t')
g = open('data/train/text_pruned','w')
for line_ in f:
   line = line_.split('\n')[0].split()
   if len(line) < 5:
      continue
   if 'xxx' in line:
      continue 
   if 'www' in line:
      continue
   g.write(line_)
g.close()

