# -*- coding=utf-8 -*-

''' This script tests the performance of GCC with noise.
    gen data
    run tests
'''

import os
import re
import random
from localization import *

import datetime

def _num2str(num):
  if num<10:
    return '00'+str(num)
  elif num <100:
    return '0' + str(num)
  else:
    return str(num)

def getNoiseTypesAvailable(noise_file_dir):
  # get noise files
  noise_file_list = wavlib.listWavFile(noise_file_dir)
  # extract noise types available
  pattern = re.compile(r'^.*\\(\w+)\.wav$')
  noise_type_available = {}
  for file in noise_file_list:
    match = pattern.match(file)
    if match:
      noise_type_available[match.group(1)] = file
  return noise_type_available
  

def dataGenGCC(target_dir, origin_file_dir, noise_file_dir, hrir_dir, \
                noise_types, SNRs, filenum_each):
  ''' generate data for the tests.
  '''
  # set azim data
  azims = range(0,91,5)
  azims.extend(range(270,359,5))
  elev = 0
  dist = 160
  
  
  # get noise info, noise_type_available is a dict
  noise_type_available = getNoiseTypesAvailable(noise_file_dir)
  
  # get origin wav file
  origin_file_list = wavlib.listWavFile(origin_file_dir)
  
  # generate data
  for noise_type in noise_types:
    noise_sig, temp_p = wavlib.audioRead(noise_type_available[noise_type])
    for snr in SNRs:
      print('{0}_{1}dB'.format(noise_type, snr))
      for azim in azims:
        # get filenum_each files randomly
        files = random.sample(origin_file_list, filenum_each)
        index = 0
        for file in files:
          #t1 = datetime.datetime.now()
          sig, params = wavlib.audioRead(file)
          #t2 = datetime.datetime.now()
          #time_read = t2-t1
          #t1 = datetime.datetime.now()
          sig, params = datalib.addDirection(sig, params, azim, elev, dist, hrir_dir)
          #t2 = datetime.datetime.now()
          #time_direction = t2-t1
          #t1 = datetime.datetime.now()
          sig = datalib.addNoiseFromSig(sig, params, snr, noise_sig)
          #t2 = datetime.datetime.now()
          #time_noise = t2-t1
          #t1 = datetime.datetime.now()
          new_file_name = '{0}_snr{1}_azim{2}_elev{3}_dist{4}_{5}.wav'.format(\
                          noise_type, snr, azim, elev, dist, _num2str(index))
          new_file_name = os.path.join(target_dir,new_file_name)
          wavlib.audioWrite(new_file_name, params, sig)
          #t2 = datetime.datetime.now()
          #time_write = t2-t1
          #print('time_read={0},time_direction={1},time_noise={2},time_write={3}'.format(\
          #      time_read,time_direction,time_noise,time_write))
          index = index + 1
          


if __name__=='__main__':
  # params
  target_dir = r'.\test_data\noise_test'
  origin_file_dir = r'..\resources\TIMIT'
  noise_file_dir = r'..\resources\noiseX_16k'
  hrir_dir =  r'..\resources\hrir_txt'
  noise_types = ['babble','f16','factory1','factory2','leopard','m109','machinegun','volvo','white','pink']
  SNRs = [-10, -5, 0, 5, 10, 15, 20]
  filenum_each = 10
  
  # data gen
  if not os.path.isdir(target_dir):
    print('ERROR: target_dir not exist!')
    exit()
  if not os.listdir(target_dir):
    dataGenGCC(target_dir, origin_file_dir, noise_file_dir, hrir_dir, \
               noise_types, SNRs, filenum_each)
  else:
    print('dataset already exists, use it to test.')
  

  
  