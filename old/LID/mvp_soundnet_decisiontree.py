#from utils import *
from sklearn import tree
import numpy as np
import random
from keras.utils import to_categorical
from sklearn.metrics import recall_score, confusion_matrix, classification_report, accuracy_score
from keras.callbacks import *
import pickle, logging
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import sys
import random
from sklearn.model_selection import train_test_split

layer = 0

# Load the files
print("Loading Spanish")
f = open('files.spanish')
lines = f.readlines()
random.shuffle(lines)
train_input_array = []
train_output_array = []
for line in lines:
    line = line.split('\n')[0]
    input_file = '../features/soundnet_feats/' + line + '.npz'
    A = np.load(input_file)
    a = A['arr_0']
    inp = np.mean(a[layer],axis=0)
    train_input_array.append(inp)
    train_output_array.append(0)

print("Loading Spanglish")
f = open('files.spanglish')
lines = f.readlines()
random.shuffle(lines)
for line in lines:
    line = line.split('\n')[0]
    input_file = '../features/soundnet_feats/' + line + '.npz'
    A = np.load(input_file)
    a = A['arr_0']
    inp = np.mean(a[layer],axis=0)
    train_input_array.append(inp)
    train_output_array.append(1)

x_train = np.array(train_input_array)
y_train = np.array(train_output_array)
print "Counts are: ", np.bincount(y_train)

X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.33, random_state=42)

def get_uar(epoch):
   
   y_test_pred = clf.predict(X_test)

   print "UAR after epoch ", epoch, " is ", classification_report(y_test, y_test_pred)
   print confusion_matrix(y_test, y_test_pred)

print "Running SVM"
clf = SVC(kernel='rbf') #,class_weight='balanced')
clf = clf.fit(X_train, y_train)
get_uar(0)

print "Running Random Forest"
clf = RandomForestClassifier(n_estimators=10) #,conf=[0.95,0.95,0.95])
clf = clf.fit(X_train, y_train)
get_uar(0)
