''' This module performs the following functions:
    1) listWavFile() find all the wav files in the path(& subpath)
    2) audioRead() read wav file
    3) audioWrite() write wav file
    4) audioPlay() play the read wav data
'''
import os
import wave
import numpy as np
import winsound

def listWavFile(root_path='.', search_log=True):
  ''' find all the wav file in the path (including sub-directories)
      return in a string list(filename with abs path)
  '''
  log_path = os.path.join(root_path, '_log.txt')
  if search_log:
    if os.path.exists(log_path) and os.path.getsize(log_path):
      with open(log_path,'r') as f:
        wav_list = f.readlines()
        for i in range(len(wav_list)):
          wav_list[i] = wav_list[i][0:-1]
      return wav_list
  # get absolute path
  root_path = os.path.abspath(root_path)
  # get the files and directories in current path
  temp_list = os.listdir(root_path)
  # list of wav file
  wav_list = []
  
  for name in temp_list:
    name = os.path.join(root_path,name)
    # if is dir, check the files in it 
    if os.path.isdir(name):
      wav_list.extend(listWavFile(name))
    # if is file, check whether it is wav file
    elif os.path.isfile(name):
      if name[-4:].lower()=='.wav':
        wav_list.append(name)
  with open(log_path, 'w') as f:
    for line in wav_list:
      f.write(line+'\n')
  return wav_list
  
def audioRead(filename):
  ''' (wave_data_float, params) = audioread(filename)
  '''
  f = wave.open(filename,'r')
  params = f.getparams()
  # read data as string, length of params[3]
  str_data = f.readframes(params[3])
  f.close()
  # from string construct short number list
  wave_data = np.fromstring(str_data,dtype=np.short)
  # convert to float
  wave_data_f = np.array([float(i)/(2**(params[1]*8-1)) for i in wave_data])
  # if dual-channel, one channel's data in a column
  if params[0] == 2:
    wave_data_f.shape = -1,2
  return (wave_data_f, params)
  
def audioWrite(filename, params, wave_data):
  ''' audioWrite(filename, params, wave_data_float)
  '''
  # convert to numpy array
  if type(wave_data)!=type(np.array([])):
    wave_data = np.array(wave_data)
  # open the target file
  f = wave.open(filename,'w')
  f.setparams(params)
  # convert to short
  if wave_data.dtype == np.float64:
    wave_data = np.array([i*(2**(params[1]*8-1)) for i in wave_data],\
      dtype=np.short)
  # write data as string
  f.writeframes(wave_data.tostring())
  f.close()

def audioPlay(wave_data, params):
  ''' audioPlay(wave_data_float, params)
  '''
  filename = '~temp_for_play_1243213512.wav'
  audioWrite(filename, params, wave_data)
  winsound.PlaySound(filename, winsound.SND_NODEFAULT)
  os.remove(filename)  