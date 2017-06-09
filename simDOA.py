# -*- coding:utf-8 -*-

''' 这个脚本用来测试GCC和MacDonald2005的性能
'''

from localization import *
import random
import os
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy import optimize

def _angStr(ang):
  if ang<10:
    return '00'+str(ang)
  elif ang<100:
    return '0'+str(ang)
  else:
    return str(ang)
    
def _getAzimFromFilename(file_name):
  pattern = re.compile(r'.*s(\d+)_.*')
  match = pattern.match(file_name)
  num = None
  if match:
    num = int(match.group(1))
  return num

def dataGen():
  # 参数设置
  target_dir = r'.\test_data\ideal'
  n_each_direction = 5
  elev = 0
  dist = 160
  hrir_path = r'..\resources\hrir_txt'
  
  # 预读取所有可用原始语音，形成list
  origin_wav_path = r'..\resources\TIMIT'
  wav_list = wavlib.listWavFile(origin_wav_path)
  origin_wav_file_num = len(wav_list)
  
  # 对每个方向（5°一个方向）生成方向性语音
  for azim in range(0,359,5):
    print('azim = {0}'.format(azim))
    for i in range(n_each_direction):
      # 随机选择原始语音信号
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
  # 参数设置
  target_dir = r'.\test_data\ideal'
  
  # 找到音频文件形成list
  wav_list = wavlib.listWavFile(target_dir)
  file_num = len(wav_list)
  
  # 误差记录list
  error = []
  
  # 预测时延
  dp_num = []
  dp_azim = []
  dp = []
  dp_real = []
  for file_name in wav_list:
    azim = _getAzimFromFilename(file_name)
    if azim>90 and azim<270:
      continue
    wave_data, params = wavlib.audioRead(file_name)
    delay_point = tdoalib.GCC(wave_data, params, weight_fun='phat')
    print azim, delay_point
    if azim>180:
      azim = azim-360
    if file_name[-6:-4]=='00':
      dp_azim.append(azim)
      dp_num.append(delay_point)
    else:
      dp.append(delay_point)
      dp_real.append(azim)
    
  # 构建时延点数到角度的映射
  def fmax(x,a,b):
    return a*x+b
  fit_a, fit_b = optimize.curve_fit(fmax, dp_num,dp_azim,[1,1])
  # [10.07, 0.27]
  '''
  print fit_a
  plt.stem(dp_num,dp_azim)
  plt.xlabel('delay_points')
  plt.ylabel('azim')
  x = np.arange(-10,10,0.1)
  plt.plot(x, fmax(x,fit_a[0],fit_a[1]))
  plt.show()
  '''
  dp_estimate = fmax(np.array(dp), fit_a[0], fit_a[1])
  print(np.mean(np.abs(dp_estimate-dp_real)))
  err = dp_estimate-dp_real
  for i in range(len(err)):
    if err[i]>10:
      err[i] = 10
  plt.hist(err)
  plt.show()
  
def testCrossChannel():
  # 参数设置
  target_dir = r'.\test_data\ideal'
  hrir_path = r'..\resources\hrir_txt'
  
  # 找到音频文件形成list
  wav_list = wavlib.listWavFile(target_dir)
  file_num = len(wav_list)
  
  # 误差记录list
  error = []
  
  # 预测时延
  azim_est = []
  azim_real = []
  for file_name in wav_list:
    azim = _getAzimFromFilename(file_name)
    if azim>90 and azim<270:
      continue
    wave_data, params = wavlib.audioRead(file_name)
    azim_estimate, pcc = tdoalib.macdonald2005(wave_data, params,hrir_path)
    print azim, azim_estimate
    azim_real.append(azim)
    azim_est.append(azim_estimate)
  print(np.mean(np.abs(azim_est-azim_real)))
  err = azim_est-azim_real
  plt.hist(err)
  plt.show()  
  
if __name__=='__main__':
  testCrossChannel()