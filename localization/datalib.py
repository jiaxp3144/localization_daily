''' This module performs the following functions:
		1) read the HRIR files
		2) generate the directional speech signal
'''

import os
import numpy as np

#############################
##	assistant functions 
#############################
def _Line2NumList(line):
  # convert the line of the HRIR.txt to a float list
  # used only inside this module
  str_list = line[0:-1].split()
  return [float(x) for x in str_list]

def _ReadHrir(root, azim, elev, dist):
  # read the HRIR.txt according to the (azim,elev,dist) in 'root' dir
  filename = 'azi'+str(azim)+'_elev'+str(elev)+'_dist'+str(dist)+'.txt'
  filepath = os.path.join(root,filename)
  with open(filepath,'r') as f:
    hrir_r = line2numList(f.readline())
  
  filename = 'azi'+str(360-azim)+'_elev'+str(elev)+'_dist'+str(dist)+'.txt'
  filepath = os.path.join(root,filename)
  with open(filepath,'r') as f:
    hrir_l = line2numList(f.readline())
  
  return (hrir_l, hrir_r)