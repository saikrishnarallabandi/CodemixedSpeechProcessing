import os
import  numpy as np

mfcc_dir = '/home3/srallaba/projects/Lang_ID/fame/corpus/kaldi/s5/mfcc_ascii/cleaned'
train_file = '../train.csv'
valid_file = '../valid.csv'
test_file = '../test.csv'

'''
train_array = []
train_label = []
# Load train
f = open(train_file)
for line in f:
   line = line.split('\n')[0]
   fname = line.split(',')[0]
   label = line.split(',')[1]
   mfcc_fname = mfcc_dir + '/' + fname + '.mfcc'
   train_array.append(np.loadtxt(mfcc_fname))
   train_label.append(label)

train_array = np.asarray(zip(train_array, train_label))
print train_array.shape 
np.save('train.npy', train_array)

valid_array = []
valid_label = []
# Load valid
f = open(valid_file)
for line in f:
   line = line.split('\n')[0]
   fname = line.split(',')[0]
   label = line.split(',')[1]
   mfcc_fname = mfcc_dir + '/' + fname + '.mfcc'
   valid_array.append(np.loadtxt(mfcc_fname))
   valid_label.append(label)

valid_array = np.asarray(zip(valid_array, valid_label))
print valid_array.shape
np.save('valid.npy', valid_array)
'''

test_array = []
test_label = []
fname_array = []
# Load test
f = open(test_file)
for line in f:
   line = line.split('\n')[0]
   fname = line.split(',')[0]
   label = line.split(',')[1]
   mfcc_fname = mfcc_dir + '/' + fname + '.mfcc'
   test_array.append(np.loadtxt(mfcc_fname))
   test_label.append(label)
   fname_array.append(fname)

test_array = np.asarray(zip(test_array, test_label, fname_array))
print test_array.shape
np.save('test.npy', test_array)



