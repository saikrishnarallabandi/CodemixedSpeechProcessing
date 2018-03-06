from utils import *
import numpy as np
import random
#import librosa
from sklearn.model_selection import train_test_split

window = 5
num_phonemes = 2
input_dim = 50*window
hidden = 16



# Process the dev
print("Processing Dev")
dev_input_file = 'inputs.npy'
dev_output_file = 'outputs.npy'
train_x , train_y = get_xy(dev_input_file, dev_output_file, window, 1)


train_inputs = np.array(train_x)
train_outputs = np.array(train_y)


X_train, X_test, y_train, y_test = train_test_split(train_inputs, train_outputs)
print X_train.shape

import keras
from sklearn import preprocessing
import numpy as np
from tensorflow.python.keras.utils import to_categorical
import sys
from keras.models import Sequential
from keras.layers import Dense, AlphaDropout
from keras.callbacks import *
import pickle, logging
from keras import regularizers



global model
model = Sequential()
model.add(Dense(input_dim, kernel_initializer='lecun_normal', activation='selu', input_shape=(input_dim,)))
#model.add(AlphaDropout(0.2))
model.add(Dense(hidden, kernel_initializer='lecun_normal', activation='selu'))
#model.add(AlphaDropout(0.2))
model.add(Dense(hidden, kernel_initializer='lecun_normal', activation='selu'))
#model.add(AlphaDropout(0.2))
model.add(Dense(hidden, kernel_initializer='lecun_normal', activation='selu'))
#model.add(AlphaDropout(0.2))
model.add(Dense(hidden, kernel_initializer='lecun_normal', activation='selu'))
#model.add(AlphaDropout(0.2))
model.add(Dense(num_phonemes, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
model.summary()
model.fit(X_train, y_train, batch_size=64, epochs=6, shuffle=True, validation_data=(X_test,y_test))

def test_model():
 for ctr, file in enumerate(sorted(os.listdir('../mcep_ascii'))):
  try:
    g = open('../langID_prediction/' + file, 'w')
    print '../mcep_ascii_npy/' + file+ '.npy'
    test_inputs = np.array(get_xy('../mcep_ascii_npy/' + file+ '.npy', '../mcep_ascii_npy/' + file+ '.npy', window, 0, 1))
    pred = model.predict(test_inputs, int(np.ceil(len(test_inputs))))
    print "Writing predictions"
    for p in pred:
      classes = np.argmax(p)
      g.write(str(classes) + '\n')
    g.close()    
    print "Write Predictions"
  except IOError:
    print "Failed for file ", file

test_model()
