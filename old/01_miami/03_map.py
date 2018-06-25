import os
import random
import numpy as np
from tensorflow.python.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import Bidirectional
from keras.callbacks import *
import pickle, logging
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

train_files='../data/segments/labels.txt'
f=open(train_files)
speakers_array = []
feats_dir='../feats'

input = []
output_temp = []

limit = 3000
i = 0
max_len = 0
for line in f:
    i += 1
    if i > limit:
       continue
    line=line.split('\n')[0].split()
    fname=line[0]
    label=line[1]
    print "Processing",fname
    output_fname=feats_dir+'/'+fname.split('.wav')[0]
    mag_file = output_fname+'.amp'
    speakers_array.append(label)
    mag = np.loadtxt(mag_file)
    if mag.shape[1] > max_len:
        max_len = mag.shape[1]
    input.append(np.transpose(mag))
    output_temp.append(label)

speakers = set(speakers_array)
id2name = {i: name for i, name in enumerate(speakers)}
name2id = {name: i for i, name in id2name.items()}

output = []
for spk in output_temp:
    output.append(to_categorical(name2id[spk], num_classes = len(speakers)))
    
units_input = 257
units_output = len(speakers)

train_input = np.zeros(
    (len(input), max_len, units_input),
    dtype='float32')

train_output = np.zeros(
    (len(output), units_output),
    dtype='float32')

for i, (s,t) in enumerate(zip(input, output)):
    length = len(s)
    kk = np.zeros((max_len-length,units_input))  
    train_input[i] = np.concatenate((s, kk),axis=0)
    train_output[i] = t


X_train, X_test, y_train, y_test = train_test_split(train_input, train_output, test_size=0.33)



hidden = 512
global model
model = Sequential()
model.add(LSTM(hidden, return_sequences=True, input_shape=(None, units_input)))
model.add(LSTM(hidden, return_sequences=True))
model.add(LSTM(hidden))
model.add(Dense(hidden, activation='selu')) 
model.add(Dense(len(speakers), activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
model.summary()
model.fit(X_train, y_train, batch_size=64, epochs=60, validation_data=(X_test, y_test),shuffle=True)
