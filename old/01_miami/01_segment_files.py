import os,sys

data_folder = '/home/srallaba/data/Spanish_English_data/train/'
destination_folder = '../data/segments'


files = sorted(os.listdir(data_folder))
label_filename = destination_folder + '/labels.txt'
g = open(label_filename, 'w')

for file in files:
   if file.endswith('_parsed.txt'):
      print "Processing " , file
      fname = file.split('_parsed.txt')[0] 
      wave_filename = data_folder + '/' + fname + '.wav'
      text_filename = data_folder  + '/' + fname  + '_parsed.txt'
      f = open(text_filename)
      count = 1
      for line in f:
          line = line.split('\n')[0].split()
          speaker = line[2]
          dest_fname_input = destination_folder  + '/wav/' + fname + '_' +  speaker + '_' + str(count).zfill(4) + '.wav'
          start_time = float(line[0])
          end_time = float(line[1])
          duration = end_time - start_time
          g.write(fname + '_' +  speaker + '_' + str(count).zfill(4) + ' ' + speaker + '\n')
          #cmd = 'sox ' + wave_filename + ' ' + dest_fname_input + ' trim ' + str(start_time) + ' ' + str(duration)
          #os.system(cmd)
          count += 1
g.close()            


