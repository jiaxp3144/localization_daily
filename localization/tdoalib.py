''' This module performs the following functions:
    1) GCC() estimate the time delay of the wav signal
'''
import numpy as np
from scipy import signal
from scipy import ifft

# test only
import wavlib

def GCC(wave_data, params, weight_fun=None, frame_len=512):
  x1 = wave_data[:,0]
  x2 = wave_data[:,1]
  freq = params[2]
  
  # calc stft-->X1,X2
  win = np.ones(frame_len)
  f,t,X1 = signal.stft(x1, freq, window=win, nperseg=frame_len)
  f,t,X2 = signal.stft(x2, freq, window=win, nperseg=frame_len)
  [a, frame_num] = X1.shape
  # calc Gx1x2
  X = X1*(X2.conjugate())
  if weight_fun.lower() == 'scot':
    X11 = X1 * (X1.conjugate())
    X22 = X2 * (X2.conjugate())
    Y = np.sqrt(X11*X22)
  elif weight_fun.lower() == 'roth':
    Y = np.abs(X1 * (X1.conjugate()))
  elif weight_fun.lower() == 'phat':
    Y = np.abs(X)
  elif weight_fun==None:
    Y = 1
  else:
    print('ERROR: unrecognised weight function for GCC!')
    return
  Gxx = ifft(X/Y,axis=0).real()
  
  
  
  

if __name__=='__main__':
  filename = 'test_d.wav'
  wave_data, params = wavlib.audioRead(filename)
  print(wave_data.shape)
  print(params)
  GCC(wave_data, params)