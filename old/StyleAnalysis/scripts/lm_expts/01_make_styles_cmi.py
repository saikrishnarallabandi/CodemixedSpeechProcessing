import os
import scipy.stats as stats
import numpy as np

segments_folder = '/home2/srallaba/data/Spanglish/segments_lab'
files = sorted(os.listdir(segments_folder))


def get_cmi(sentence):
    
   w = len(sentence.split())
   count_A = 0
   count_B = 0
   n = 0
   for word in sentence.split():
     print word
     if word == 'eng':
        count_A += 1
     elif word == 'spa':
        count_B += 1
     else:
        n += 1  
   max_w = max(count_A, count_B)
   print sentence, w, max_w
   if w == n:
     return 0
   return ( w - max_w ) * 1.0 / (w )
   #return ( w - max_w ) * 1.0 / (w - n)

cmi_array = []
g = open('cmi_miami.txt','w')
for file in files:
    print 'Processing ', file
    with open(segments_folder + '/' + file) as f:
        lines = f.readlines()
    line = lines[0].split('\n')[0]
    s = ' ' 
    for word in line.split():
        if '_' in word:
           s += ' ' + word.split('_')[-1]
    if len(s) > 1:
      cmi = get_cmi(s)
      print s, cmi
      cmi_array.append(float(cmi))
      g.write(file + ' ' + str(cmi) + '\n')
g.close()    
    

grps2 = [0, 0.05, 0.15, 0.30, 1]
cmi_array_sorted = np.array(sorted(cmi_array))
cmi_array_grouped = np.digitize(cmi_array_sorted, grps2)
print cmi_array_grouped[0:200]
np.savetxt('cmi_miami.styles',cmi_array_grouped)

unique, counts = np.unique(cmi_array_grouped, return_counts=True)
for u,c in zip(unique,counts):
     print u, c

'''
cmi_array_sorted = np.array(sorted(cmi_array))
fit = stats.norm.pdf(cmi_array_sorted, np.mean(cmi_array_sorted), np.std(cmi_array_sorted))  #this is a fitting indeed
plt.plot(cmi_array_sorted,fit,'-o')
plt.hist(h,normed=True)      #use this to draw histogram of your data
fig.savefig('cmi_distribution.png') 
'''
