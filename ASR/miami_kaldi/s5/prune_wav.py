#!/usr/bin/python
import os

cmd = 'wav-to-duration scp:data/train/wav.scp ark,t:- > /tmp/wav_dur'
os.system(cmd)

durations = {}
f = open('/tmp/wav_dur')
for line in f:
   line = line.split('\n')[0].split()
   durations[line[0]] = float(line[1])


f = open('data/train/wav.scp')
g = open('data/train/wav.scp_pruned', 'w')
for line in f:
 try:
   ln = line.split('\n')[0].split()
   fname = ln[0]
   loc = ln[1]
   if durations[fname] > 1:
      g.write(line)
 except KeyError:
   print "Pruning failed for ", line

f.close()
g.close()

