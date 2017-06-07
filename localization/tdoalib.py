''' This module performs the following functions:
    1) GCC() estimate the time delay of the wav signal
'''
import numpy as np
from scipy import signal
from scipy import ifft
from scipy.stats import mode
import datalib

# test only
import wavlib
import matplotlib.pyplot as plt

def GCC(wave_data, params, weight_fun=None, frame_len=512, ref_power=None):
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
  if weight_fun==None:
    Y = 1
  elif weight_fun.lower() == 'scot':
    X11 = X1 * (X1.conjugate())
    X22 = X2 * (X2.conjugate())
    Y = np.sqrt(X11*X22)
  elif weight_fun.lower() == 'roth':
    Y = np.abs(X1 * (X1.conjugate()))
  elif weight_fun.lower() == 'phat':
    Y = np.abs(X)
  else:
    print('ERROR: unrecognised weight function for GCC!')
    return
  Gxx = ifft(X/(Y+1e-15),axis=0).real
  
  # calc ref_power
  if not ref_power:
    X11 = X1 * (X1.conjugate())
    ref_power = np.sum(X11)/(frame_num*5.0)
  
  time_delay = []
  for i in range(frame_num):
    if np.sum(X11[:,i])<ref_power:
      continue
    time_delay.append(np.argmax(Gxx[:,i]))
    
  # use the most frequently appeared value as the estimated value
  delay = mode(time_delay).mode[0]
  # if r is after l, the delay should be minus
  if delay > 128:
    delay = delay-257
  return delay

''' using cross channel method to find doa
		don't take elev and dist into consideration
'''    
def macdonald2005(wave_data,params,hrir_path):
  sig_r = wave_data[:,0]
  sig_l = wave_data[:,1]
  pcc = []
  elev = 0
  dist = 160
  params = list(params)
  params[0] = 1
  for azim in range(0,359,5):
    [temp, useless] = datalib.addDirection(sig_r, params, azim, elev, dist, hrir_path)
    temp_r = temp[:,1]
    [temp, useless] = datalib.addDirection(sig_l, params, azim, elev, dist, hrir_path)
    temp_l = temp[:,0]
    pcc.append(np.corrcoef(temp_r, temp_l)[0,1])
  return [np.argmax(pcc)*5,pcc]
	
  
  

if __name__=='__main__':
  '''
  # test GCC
  
  for azim in range(0,361,5):d
    filename = 'test_{0}.wav'.format(azim)
    wave_data, params = wavlib.audioRead(filename)
    time_delay = GCC(wave_data, params,weight_fun=None)
    print("azim={0},delay point={1}".format(azim,time_delay))
  '''
  
  # test macdonald2005
  filename = 'test_d.wav'
  wave_data, params = wavlib.audioRead(filename)
  hrir_path = r'..\..\resources\HRIR_txt'
  ang,pcc =  macdonald2005(wave_data, params, hrir_path)
  print(ang)
  plt.plot(pcc)
  plt.show()
