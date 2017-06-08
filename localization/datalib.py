''' This module performs the following functions:
		1) read the HRIR files
		2) generate the directional speech signal
'''

import os
import numpy as np
import random
import wavlib
from scipy.signal import resample

#############################
##	assistant functions 
#############################
def _Line2NumList(line):
  # convert the line of the HRIR.txt to a float list
  # used only inside this module
  str_list = line[0:-1].split()
  return [float(x) for x in str_list]



#############################
##  main functions
#############################
def readHrir(root, azim, elev, dist):
  # read the HRIR.txt according to the (azim,elev,dist) in 'root' dir
  # get filename from azim, elev, dist
  filename = 'azi'+str(azim)+'_elev'+str(elev)+'_dist'+str(dist)+'.txt'
  # add abs path to filename
  filepath = os.path.join(os.path.abspath(root),filename)
  # read the first line of the txt file, corresponding to the hrir_l
  with open(filepath,'r') as f:
    hrir_l = _Line2NumList(f.readline())
  
  # read the opposite txt file to get the hrir_r
  filename = 'azi'+str(360-azim)+'_elev'+str(elev)+'_dist'+str(dist)+'.txt'
  filepath = os.path.join(root,filename)
  with open(filepath,'r') as f:
    hrir_r = _Line2NumList(f.readline())
  
  return (hrir_r, hrir_l)

def addDirection(sig, params, azim, elev, dist, hrir_path):
  ''' process the sig to the direction of (azim, elev, dist)
      make sure the sig in monaural, params[0]=1
  '''
  if params[0] != 1:
    print("Use monaural sig!")
    return
  # get the hrir
  (hrir_r, hrir_l) = readHrir(hrir_path, azim, elev, dist)
  # resample the hrir
  if params[2] != 44100:
    hrir_len = int(len(hrir_l)/44100.0*params[2])
    hrir_r = resample(hrir_r, hrir_len)
    hrir_l = resample(hrir_l, hrir_len)
  # add direction
  sig_out = np.array([np.convolve(sig, hrir_r),np.convolve(sig, hrir_l)]).T
  params_out = (2, params[1], params[2], params[3]*2, params[4], params[5])
  return (sig_out, params_out)
  
def addNoise(sig, params, snr, noise_file_path):
  ''' add noise according to the noise type and snr
  '''
  # if dual channel
  if params[0]==2:
    params_single = list(params)
    params_single[0] = 1
    params_single[2] = params[2]/2
    sig_r = sig[:,0]
    sig_l = sig[:,1]
    sig_r_n = addNoise(sig_r,params_single,snr,noise_file_path)
    sig_l_n = addNoise(sig_l,params_single,snr,noise_file_path)
    return np.array([sig_r_n, sig_l_n]).T
  # if single channel
  else:
    # read noise file
    noise, params_n = wavlib.audioRead(noise_file_path)
    # resample to fs
    if params_n[2]!=params[2]:
      noise_len = int(len(noise)/params_n[2]*params[2])
      noise = resample(noise, noise_len)
    # random to start index
    noise_len = len(noise)
    sig_len = len(sig)
    if noise_len <= 5*sig_len:
      print('ERROR: noise file length is too short for the signal!')
      return
    start_index = random.randint(0, noise_len-len(sig))
    noise_slice = noise[start_index:start_index+sig_len]
    # decided by snr
    signal_power = np.sum(sig**2)/sig_len
    noise_var = signal_power/(10**(snr/10.0))
    noise_slice = np.sqrt(noise_var)/np.std(noise_slice)*noise_slice
    sig_n = sig+noise_slice
    return sig_n
    
    
