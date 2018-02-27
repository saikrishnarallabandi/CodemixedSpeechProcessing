import numpy as np
from tensorflow.python.keras.utils import to_categorical


def pad_nparray(nparray, window):
    initial = []
    for i in range((window-1)/2):
       initial.append(nparray[0])

    final = []
    for i in range((window-1)/2):
       final.append(nparray[len(nparray)-1])
    
    #print np.asarray(initial).shape , nparray.shape, np.asarray(final).shape
    nparray = np.concatenate((initial, nparray,  final)) 
    return nparray



def get_contexts(nparray, window=11):
   context_frames = np.asarray(zip(*[nparray[n:] for n in range(window)]))
   temp = []
   for f in context_frames:
       temp.append(np.concatenate(([f[n] for n in range(window)])))
   return np.asarray(temp)



def get_xy(A,B, window, categorical_flag):
   ### A is the input file and B is the output file

   # First read the files
   input_all = np.load(A)
   output_decimal = np.load(B)

   # Pad the data to account for contexts 
   input_padded = input_all
   output_padded = output_decimal

   count_input = 0
   for i,d in enumerate(input_all):
     input_padded[i] = pad_nparray(d, window)
     count_input += len(input_padded[i]) 

   count_output = 0
   for i,d in enumerate(output_decimal):
     output_padded[i] = pad_nparray(d,window)
     count_output += len(output_padded[i]) 
   
   # Get the contexts
   input_contexts = []
   output_contexts = []

   for c, (i,o) in enumerate(zip(input_padded, output_padded)):
      k = get_contexts(i,window)
      for kk in k: 
         input_contexts.append(kk)

      k = o[(window-1)/2:-(window-1)/2]
      for kk in k:
         output_contexts.append(kk)
   del input_padded, output_padded , input_all, output_decimal      
   
   num_phonemes = 2
   num_train = len(input_contexts)

   x = input_contexts
   if categorical_flag:
      y = np.zeros(
         (num_train, num_phonemes),
         dtype='float32')
      for i,k in enumerate(output_contexts):
         y[i] = to_categorical(k, num_phonemes)
   else:
       y = output_contexts
  
   return x,y


#dev_input_file = '../data/dev.npy'
#dev_output_file = '../data/dev_labels.npy'
#get_xy(dev_input_file, dev_output_file, 5, 1)


def get_batches(A,B,batch_size):
   ### A is an n dim list while B is a one dimensional list
   A = np.array(A)
   B = np.array(B)
   num_batches = len(A)/batch_size

   for i in range(num_batches):
       A_batch, B_batch = A[i*batch_size: i*batch_size + batch_size], B[i*batch_size: i*batch_size + batch_size]   
       yield A_batch, B_batch


