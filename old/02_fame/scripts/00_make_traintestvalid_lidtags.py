import os

# The idea  is to use the train devel test split provided by the corpus and make train.csv and test.csv with the language ids

# FR
train_fr_file = '../corpus/data/train_fr/wav.scp'
valid_fr_file = '../corpus/data/devel_fr/wav.scp'
test_fr_file = '../corpus/data/test_fr/wav.scp'

# NL
train_nl_file = '../corpus/data/train_nl/wav.scp'
valid_nl_file = '../corpus/data/devel_nl/wav.scp'
test_nl_file = '../corpus/data/test_nl/wav.scp'

f_train = open('../train.csv', 'w')
f_valid = open('../valid.csv', 'w')
f_test = open('../test.csv', 'w')

# Get the train data
f = open(train_fr_file)
for line in f:
	 line = line.split('\n')[0]
	 fname = line.split()[0]
	 f_train.write(fname + ' 1' + '\n')
f = open(train_nl_file)
for line in f:
	 line = line.split('\n')[0]
	 fname = line.split()[0]
	 f_train.write(fname + ' 2' + '\n')

f_train.close()     

     
# Get the valid data
f = open(valid_fr_file)
for line in f:
	 line = line.split('\n')[0]
	 fname = line.split()[0]
	 f_valid.write(fname + ' 1' + '\n')
f = open(valid_nl_file)
for line in f:
	 line = line.split('\n')[0]
	 fname = line.split()[0]
	 f_valid.write(fname + ' 2' + '\n') 
f_valid.close()

# Get the test data
f = open(test_fr_file)
for line in f:
	 line = line.split('\n')[0]
	 fname = line.split()[0]
	 f_test.write(fname + ' 1' + '\n')
f = open(test_nl_file)
for line in f:
	 line = line.split('\n')[0]
	 fname = line.split()[0]
	 f_test.write(fname + ' 2' + '\n') 
f_test.close()




