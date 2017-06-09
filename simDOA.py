# -*- coding:utf-8 -*-

''' ����ű���������GCC��MacDonald2005������
'''

from localization import *
import random
import os
import numpy as np
import re

def _angStr(ang):
  if ang<10:
    return '00'+str(ang)
  elif ang<100:
    return '0'+str(ang)
  else:
    return str(ang)
    
def _getAzimFromFilename(file_name):
  pattern = re.compile(r'*s(\d+)_*')
  match = pattern.match(file_name)
  num = None
  if match:
    num = int(match.group())
  return num

def dataGen():
  # ��������
  target_dir = r'.\test_data\ideal'
  n_each_direction = 5
  elev = 0
  dist = 160
  hrir_path = r'..\resources\hrir_txt'
  
  # Ԥ��ȡ���п���ԭʼ�������γ�list
  origin_wav_path = r'..\resources\TIMIT'
  wav_list = wavlib.listWavFile(origin_wav_path)
  origin_wav_file_num = len(wav_list)
  
  # ��ÿ������5��һ���������ɷ���������
  for azim in range(0,359,5):
    print('azim = {0}'.format(azim))
    for i in range(n_each_direction):
      # ���ѡ��ԭʼ�����ź�
      wav_index = random.randint(0,origin_wav_file_num)
      origin_wav_file_path = wav_list[wav_index]
      sig_single, params = wavlib.audioRead(origin_wav_file_path)
      alpha = 0.2/np.max(np.abs(sig_single))
      sig_single = alpha*sig_single
      sig_dual, params_dual = datalib.addDirection(sig_single, params, azim, elev, dist, hrir_path)
      new_file_name = 's{0}_0{1}.wav'.format(_angStr(azim), i)
      new_file_path = os.path.join(target_dir, new_file_name)
      wavlib.audioWrite(new_file_path, params_dual, sig_dual)

def testGCC():
  # ��������
  target_dir = r'.\test_data\ideal'
  
  # �ҵ���Ƶ�ļ��γ�list
  wav_list = wavlib.listWavFile(target_dir)
  file_num = len(wav_list)
  
  # ����¼list
  error = []
  
  # �ж����
  for 
  

if __name__=='__main__':
  dataGen()