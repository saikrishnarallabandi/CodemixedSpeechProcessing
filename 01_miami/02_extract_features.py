import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

feats_dir = '../feats'
train_files = '../data/segments/labels.txt'
f = open(train_files)


def read_wav_file(fname):
    _, wav = wavfile.read(fname)
    wav = wav.astype(np.float32) / np.iinfo(np.int16).max
    return wav

def process_file(fname):
    wav = read_wav_file(fname)
    L = 16000  # 1 sec

    '''
    if len(wav) > L:
        i = np.random.randint(0, len(wav) - L)
        wav = wav[i:(i+L)]
    elif len(wav) < L:
        rem_len = L - len(wav)
        i = np.random.randint(0, len(silence_data) - rem_len)
        silence_part = silence_data[i:(i+L)]
        j = np.random.randint(0, rem_len)
        silence_part_left  = silence_part[0:j]
        silence_part_right = silence_part[j:rem_len]
        wav = np.concatenate([silence_part_left, wav, silence_part_right])
    '''

    specgram = stft(wav, 16000, nperseg = 400, noverlap = 240, nfft = 512, padded = False, boundary = None)
    phase = np.angle(specgram[2]) / np.pi
    amp = np.log1p(np.abs(specgram[2]))
    
    return phase, amp


for line in f:
    line = line.split('\n')[0].split()
    fname = line[0]
    label = line[1]
    print "Processing ", fname
    output_fname = feats_dir + '/' + fname.split('.wav')[0]
    wav_file = '../data/segments/wav/' + fname + '.wav'
    phase, amp = process_file(wav_file)
    np.savetxt(output_fname + '.phase' , phase, fmt='%.7f')
    np.savetxt(output_fname + '.amp', amp, fmt = '%.7f')    
