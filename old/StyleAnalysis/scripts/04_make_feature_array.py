import numpy as np
import os


mfcc_folder = '/home3/srallaba/projects/codeswitchedspeechprocessing/style_analysis/cmu_us_miami/mcep_ascii'
langID_folder = '/home3/srallaba/projects/codeswitchedspeechprocessing/style_analysis/cmu_us_miami/lang_wav'

mfcc_files = sorted(os.listdir(mfcc_folder))
LID_files = sorted(os.listdir(langID_folder))

inputs = []
outputs = []

for LF in LID_files:
    mfcc_file = mfcc_folder + '/' + LF.split('.')[0] + '.mcep'
    lang_file = langID_folder + '/' + LF
    input = np.loadtxt(mfcc_file)
    output = np.loadtxt(lang_file)
    print mfcc_file, lang_file
    assert len(input) == len(output)   
    inputs.append(input)
    outputs.append(output)
    np.save('../mcep_ascii_npy/'+ LF.split('.')[0] + '.mcep', input)

np.save('inputs.npy',inputs)
np.save('outputs.npy', outputs)    
