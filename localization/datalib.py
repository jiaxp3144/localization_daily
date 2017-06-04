''' This module performs the following functions:
		1) read the HRIR files
		2) generate the directional speech signal
'''

import os
import numpy as np
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
  # read the first line of the txt file, corresponding to the hrir_r
  with open(filepath,'r') as f:
    hrir_l = _Line2NumList(f.readline())
  
  # read the opposite txt file to get the hrir_l
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
  (hrir_l, hrir_r) = readHrir(hrir_path, azim, elev, dist)
  # resample the hrir
  if params[2] != 44100:
    hrir_len = int(len(hrir_l)/44100.0*params[2])
    hrir_r = resample(hrir_r, hrir_len)
    hrir_l = resample(hrir_l, hrir_len)
  # add direction
  sig_out = np.array([np.convolve(sig, hrir_r),np.convolve(sig, hrir_l)]).T
  params_out = (2, params[1], params[2], params[3]*2, params[4], params[5])
  return (sig_out, params_out)
