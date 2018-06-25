import torch
from utils import *
import numpy as np
import random
from torch.autograd import Variable
import torch.nn.functional as F

window = 15
num_phonemes = 138
input_dim = 40*window
hidden = 16



# Process the dev
print("Processing Dev")
dev_input_file = 'inputs.npy'
dev_output_file = 'outputs.npy'
train_x , train_y = get_xy(dev_input_file, dev_output_file, window, 0)

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.hidden2 = torch.nn.Linear(n_hidden, n_hidden)
         
        self.out = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        x = F.relu(self.hidden1(x))      # activation function for hidden layer
        x = F.dropout(x, training=self.training)
        x = F.relu(self.hidden2(x))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.hidden2(x))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.hidden2(x))
        x = F.dropout(x, training=self.training)
        x = F.relu(self.hidden2(x))
       	x = F.dropout(x, training=self.training)
        x = F.relu(self.hidden2(x))
       	x = F.dropout(x, training=self.training)
        x = F.relu(self.hidden2(x))
       	x = F.dropout(x, training=self.training)
        x = self.out(x)
        return F.log_softmax(x, dim=1)

net = Net(n_feature=input_dim, n_hidden=1024, n_output=num_phonemes)     # define the network
print(net)  # net architecture

optimizer = torch.optim.SGD(net.parameters(), lr=0.02)
loss_func = F.nll_loss



def train(epoch):
    net.train()
    for data,target in get_batches(train_x, train_y, 256):

       train_inputs_torch, train_outputs_torch = torch.from_numpy(data), torch.from_numpy(target)
       data, target = Variable(train_inputs_torch), Variable(train_outputs_torch)

       out = net(data.float())     
       loss = F.nll_loss(out, target)

       optimizer.zero_grad()
       loss.backward()       
       optimizer.step()       

       

    print ("Loss after epoch ", epoch, " : ", loss.data[0])    

def test():
    net.eval()
    test_loss = 0
    correct = 0
    
    yTrue = []
    yPred = []

    for data, target in get_batches(valid_x,valid_y, 256):
        ops = target
        valid_inputs_torch, valid_outputs_torch = torch.from_numpy(data), torch.from_numpy(target)
        data, target = Variable(valid_inputs_torch, volatile=True), Variable(valid_outputs_torch)
        #data = data.cuda()
        #target = target.cuda()
        output = net(data)

        _, predicted = torch.max(output.data, 1)
        for (ytrue, ypred) in zip(ops, predicted):
             yTrue.append(ytrue)
             yPred.append(ypred)



        test_loss += F.nll_loss(output, target, size_average=False).data[0] # sum up batch loss
        pred = output.data.max(1, keepdim=True)[1] # get the index of the max log-probability
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(valid_x)
    print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(valid_x),
        100. * correct / len(valid_x)))

    print classification_report(yTrue, yPred)



for epoch in range(1, 20):
    train(epoch)
    test()
