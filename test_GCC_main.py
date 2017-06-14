# -*- coding=utf-8 -*-

''' TEST GCC'''

from localization import *
import re

def _num2str(num):
  if num<10:
    return '00'+str(num)
  elif num<100:
    return '0'+str(num)
  else:
    return str(num)

def getMatchFileList(org_list, noise_types, SNRs, index):
  # get re strs
  name_strs = []
  if noise_types:
    for noise_type in noise_types:
      name_strs.append(r'.*'+noise_type+'_')
  else:
    name_strs.append(r'.*_')
  
  name_strs_2 = []
  if SNRs:
    for snr in SNRs:
      for prestr in name_strs:
        name_strs_2.append(prestr+'snr'+str(snr)+r'_')
  else:
    for prestr in name_strs:
      name_strs_2.append(prestr+r'snr\d+_')
      
  name_strs_3 = []
  if index:
    for i in index:
      for prestr in name_strs_2:
        name_strs_3.append(prestr+r'.*_'+_num2str(i)+r'\..*')
  else:
    for prestr in name_strs_2:
      name_strs_3.append(prestr+r'\..*')
    
  # re match
  pattern_list = []
  for re_str in name_strs_3:
    print re_str
    pattern_list.append(re.compile(re_str))
  
  test_list = []
  for file in org_list:
    for pattern in pattern_list:
      if pattern.match(file):
        test_list.append(file)
        break
  
  return test_list

def testGCC(dataset_dir=r'.\test_data\noise_test', SNRs=None, noise_types=None, \
            index=None, frame_len=512, ref_power=None, weight_fun=None):
  # according SNRs and noise_types find test dataset
  all_files = wavlib.listWavFile(dataset_dir)
  test_files = getMatchFileList(all_files, noise_types, SNRs, index)
  
  for i in test_files:
    print i
    

if __name__=='__main__':
  SNRs = [20]
  noise_types = []
  index = []
  testGCC(SNRs=SNRs, noise_types=noise_types, index=index)
  