import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import time
from torch.autograd import Variable
import torch.nn as nn
import random


train_file = '../dataset/wiki.train.npy'
valid_file = '../dataset/wiki.valid.npy'

# Some stupid way to load. Use dataloader instead of  this
train_text = []
A = np.load(train_file)
batch_size = 32
for a in A:
   for aa in a:
       train_text.append(aa)

print(len(train_text))

valid_text = []
A = np.load(valid_file)
for a in A:
    for aa in a:
        valid_text.append(aa)

print(len(valid_text))



import torch.nn as nn
from torch.autograd import Variable

class RNNLM(nn.Module):
    """Container module with an encoder, a recurrent module, and a decoder."""

    def __init__(self, ntoken, ninp, nhid, nlayers, dropout=0.05, tie_weights=False):
        super(RNNLM, self).__init__()
        self.drop = nn.Dropout(dropout)
        self.encoder = nn.Embedding(ntoken, ninp)
        self.rnn = nn.GRU(ninp, nhid, nlayers, dropout=dropout)
        self.decoder = nn.Linear(nhid, ntoken)
        self.inp_layer = nn.Linear(1, nhid)
        

        if tie_weights:
            if nhid != ninp:
                raise ValueError('When using the tied flag, nhid must be equal to emsize')
            self.decoder.weight = self.encoder.weight

        self.init_weights()
        self.nhid = nhid
        self.nlayers = nlayers

    def init_weights(self):
        initrange = 0.01
        self.encoder.weight.data.uniform_(-initrange, initrange)
        self.decoder.bias.data.fill_(0)
        self.decoder.weight.data.uniform_(-initrange, initrange)

    def forward(self, input):
        emb = self.drop(self.encoder(input))
        output, hidden = self.rnn(emb, None)
        output = self.drop(output)
        decoded = self.decoder(output.view(output.size(0)*output.size(1), output.size(2)))
        return decoded
        return decoded.view(output.size(0), output.size(1), decoded.size(1)), hidden

    def init_hidden(self, bsz):
        weight = next(self.parameters()).data
        return (Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()),
                    Variable(weight.new(self.nlayers, bsz, self.nhid).zero_()))




train_text = np.array(train_text)
valid_text = np.array(valid_text)

batch_len = len(train_text) / batch_size 
train_batches = np.array_split(train_text, batch_len)
batch_len = len(valid_text) / batch_size 
valid_batches = np.array_split(valid_text, 32)



model = RNNLM(33278, 256, 256, 1, 0.3, True)
#model.load_state_dict(torch.load('model.pkl'))
model.cuda()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
from torch.optim.lr_scheduler import ReduceLROnPlateau
scheduler = ReduceLROnPlateau(optimizer, mode='min')

g = open('logfile','w')
g.close()


def evaluate():
      model.eval()
      total_loss = 0
      for i, t in enumerate(valid_batches):

            # Get it in the right shape
            inp = torch.from_numpy(t[:-1]).unsqueeze_(0)
            tar = torch.from_numpy(t[1:]).unsqueeze_(0)
            inp = Variable(inp).cuda().long()
            targets = Variable(tar).cuda().long()
            outputs = model(inp)
            targets.squeeze_(0)
            outputs.squeeze_(0)
            loss = criterion(outputs, targets)
            total_loss += loss.data[0]
       
      model.train()
      return total_loss / (1.0 * i)


def train(epoch):
        total_loss = 0
        random.shuffle(train_batches)
        for i, t in enumerate(train_batches):

            # Get it in the right shape
            inp = torch.from_numpy(t[:-1]).unsqueeze_(0)
            tar = torch.from_numpy(t[1:]).unsqueeze_(0)
            inp = Variable(inp).cuda().long()
            targets = Variable(tar).cuda().long()
            outputs = model(inp)
            #print(outputs)
            #print(targets)
            targets.squeeze_(0)
            outputs.squeeze_(0)


            optimizer.zero_grad()
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            total_loss += loss.data[0]

            if i % 10000 == 1:
                g = open('logfile','a')
                g.write("  Training Loss after " + str(i) +  " sequences is : " + str(float(total_loss/(i+0.0001))) + '\n')
                g.close()


        print("Loss after epoch", epoch, ": ", total_loss/float(i))
        g = open('logfile','a')
        g.write("  Training Loss after " + str(epoch) +  " epoch : " + str(float(total_loss/(i+0.0001))) + '\n')
        g.close()

      
for epoch in range(15):
    train(epoch)
    val_loss = evaluate()
    scheduler.step(val_loss)

    g = open('logfile','a')
    g.write("Validation Loss after " + str(epoch) +  "  is : " + str(val_loss) + '\n')
    g.close()

    model_name = 'model_epoch' + str(epoch).zfill(2) + '.pt'
    torch.save(model, model_name)
    torch.save(model.state_dict(), 'model.pkl')
