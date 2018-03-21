import os
#import _dynet
#import dynet_config
#dynet_config.set(mem=2048, requested_gpus=0, autobatch=1)
import dynet as dy
import numpy as np
import  random
from sklearn.metrics import accuracy_score, classification_report

class EncoderBiLSTM(object):

  def __init__(self, model, num_input, num_hidden, num_output, act=dy.tanh):
    self.num_input = int(num_input)
    self.num_hidden = int(num_hidden)
    self.num_out = int(num_output)
    self.model = model
    print "Loaded params"

    # LSTM Parameters
    self.enc_lstm_fwd_builder = dy.LSTMBuilder(1, self.num_input, num_hidden, model)  
    self.enc_lstm_bwd_builder = dy.LSTMBuilder(1, self.num_input, num_hidden, model)
 
    # MLP Parameters
    self.W_mlp = self.model.add_parameters((self.num_out, self.num_hidden*2))
    self.b_mlp = self.model.add_parameters((num_output))

  def mlp(self,x, W, b):
       return dy.tanh( W * x + b)

  def calculate_loss(self, nparray , label):

    # Renew the computation graph
    dy.renew_cg()

    # Initialize LSTMs
    enc_init_state_fwd = self.enc_lstm_fwd_builder.initial_state()
    enc_init_state_bwd = self.enc_lstm_bwd_builder.initial_state()

    # Initialize MLP
    w_mlp = dy.parameter(self.W_mlp)
    b_mlp = dy.parameter(self.b_mlp)    

    input_frames = dy.inputTensor(nparray)
    input_frames_reverse = dy.inputTensor(np.flipud(nparray))

    # Get the LSTM embeddings
    fwd_output = enc_init_state_fwd.add_inputs([frame for frame in input_frames])[-1].output()
    bwd_output = enc_init_state_bwd.add_inputs([frame for frame in input_frames_reverse])[-1].output()    

    # Concatenate
    bilstm_embeddings = dy.concatenate([fwd_output, bwd_output])

    # Predict the label score
    pred_score = self.mlp(bilstm_embeddings, w_mlp, b_mlp)
    return dy.pickneglogsoftmax(pred_score, label)

  def predict_label(self, nparray):

    # Renew the computation graph
    dy.renew_cg()

    # Initialize LSTMs
    enc_init_state_fwd = self.enc_lstm_fwd_builder.initial_state()
    enc_init_state_bwd = self.enc_lstm_bwd_builder.initial_state()

    # Initialize MLP
    w_mlp = dy.parameter(self.W_mlp)
    b_mlp = dy.parameter(self.b_mlp)

    input_frames = dy.inputTensor(nparray)
    input_frames_reverse = dy.inputTensor(np.flipud(nparray))

    # Get the LSTM embeddings
    fwd_output = enc_init_state_fwd.add_inputs([frame for frame in input_frames])[-1].output()
    bwd_output = enc_init_state_bwd.add_inputs([frame for frame in input_frames_reverse])[-1].output()

    # Concatenate
    bilstm_embeddings = dy.concatenate([fwd_output, bwd_output])

    # Predict the label score
    pred_score = self.mlp(bilstm_embeddings, w_mlp, b_mlp)
    return np.argmax(dy.softmax(pred_score).value())


valid_arr = 'valid.npy'
valid_data = np.load(valid_arr)

train_arr = 'train.npy'
train_data = np.load(train_arr)

test_arr = 'test.npy'
test_data = np.load(test_arr)

# Hyperparameters 
units_input = 39
units_hidden = int(512)
units_output = 2
units_latent = int(16)

# Instantiate and define the loss
m = dy.Model()
model = EncoderBiLSTM(m, units_input, units_hidden, units_output,  dy.rectify)
trainer = dy.AdamTrainer(m)
update_params = 32


def get_acc(arr):
   yTrue = []
   yPred = []
   for (A,B) in arr:
       yPred.append(model.predict_label(A))
       yTrue.append(int(B)-1)
   print classification_report(yTrue, yPred)
   return accuracy_score(yTrue, yPred)

train_data = valid_data
c = len(train_data)
print "Number of files: ", c

for epoch in range(30):
  print "Epoch: ", epoch
  train_loss = 0
  count = 1
  random.shuffle(train_data)
  for (a,b) in train_data:
     count += 1
     loss = model.calculate_loss(a,int(b)-1)
     train_loss += loss.value()
     loss.backward()
     trainer.update()
    
     if count % 1000 == 1:
         print "   Training loss after ", count, " files: ", train_loss/count
     
  print "After epoch ", epoch, " train error: ", train_loss/count 
  #train_acc = get_acc(train_data)
  val_acc = get_acc(valid_data)
  #print "Train acc: ", train_acc
  print "Validation acc: ", val_acc         
  


# Test
cc = 1
f = open('submission.csv','w')
f.write('fname,id' + '\n')
yPred = []
yTrue = []
for (a,b,fname) in test_data:
   b_pred = model.predict_label(a)
   f.write(fname + ',' + str(b_pred) + '\n')
   yPred.append(b_pred)
   yTrue.append(int(b)-1)
f.close()

print "Test Accuracy: ", accuracy_score(yTrue, yPred)

