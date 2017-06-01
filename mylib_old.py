import os

import wave
import numpy as np
import winsound

import random

import re

#################################################
# ------------find wavfile in resources dir------
#################################################
# need os
def listWavFile(root_path):
  root_path = os.path.abspath(root_path)
  temp_list = os.listdir(root_path)
  wav_list = []
  for name in temp_list:
    name = os.path.join(root_path,name)
    if os.path.isdir(name):
      wav_list.extend(listWavFile(name))
    elif os.path.isfile(name):
      if name[-4:].lower()=='.wav':
        wav_list.append(name)
  return wav_list


#################################################
# ------------Read HRIR--------------------------
#################################################
# need os, numpy(np)

def line2numList(line):
  # convert the line of the HRIR.txt to a float list
  str_list = line[0:-1].split()
  return [float(x) for x in str_list]

def readtxt(root, azim, elev, dist):
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

#################################################
# ------------wave file processing---------------
#################################################
# need os, wave, numpy(np), winsound
def audioread(filename):
  f = wave.open(filename,'r')
  params = f.getparams()
  str_data = f.readframes(params[3])
  f.close()
  wave_data = np.fromstring(str_data,dtype=np.short)
  wave_data_f = np.array([float(i)/(2**(params[1]*8-1)) for i in wave_data])
  if params[0] == 2:
    wave_data.shape = -1,2
  return (wave_data_f, params)

def audiowrite(filename, params, wave_data):
  if type(wave_data)!=type(np.array([])):
    wave_data = np.array(wave_data)
  f = wave.open(filename,'w')
  f.setparams(params)
  if wave_data.dtype == np.float64:
    wave_data = np.array([i*(2**(params[1]*8-1)) for i in wave_data],\
      dtype=np.short)
  f.writeframes(wave_data.tostring())
  f.close()
  
def audioplay(wave_data, params):
  if type(wave_data)!=type(np.array([])):
    wave_data = np.array(wave_data)
  filename = 'temp_for_play_1111.wav'
  f = wave.open(filename,'w')
  f.setparams(params)
  if wave_data.dtype == np.float64:
    wave_data = np.array([i*(2**(params[1]*8-1)) for i in wave_data],\
      dtype=np.short)
  f.writeframes(wave_data.tostring())
  f.close()
  winsound.PlaySound(filename, winsound.SND_NODEFAULT)
  os.remove(filename)
  
#################################################
# ------------direction generation---------------
#################################################
# need numpy(np), os
def filenameGenerator(filename_org, azim, elev, distance):
  filename_org = os.path.basename(filename_org)
  return "azim{0}_elev{1}_dist{2}_{3}".format(azim,elev,distance,filename_org)


def directionGenerator(filename_org, azim, dist, target_dir='.'):
  (wave_data_org, params) = audioread(filename_org)
  HRIR_root = r'.\HRIR_txt'
  (HRIR_L, HRIR_R) = readtxt(HRIR_root, azim, 0, dist)
  wave_data_new = np.array(\
    [np.convolve(wave_data_org,HRIR_L),np.convolve(wave_data_org, HRIR_R)]).T
  params_new = (2, params[1], params[2], params[3]*2, params[4], params[5])
  filename_gen = filenameGenerator(filename_org,azim,0,dist)
  filename_gen = os.path.join(target_dir, filename_gen)
  audiowrite(filename_gen, params_new, wave_data_new)
  return filename_gen
  
#################################################
# ------------data generation--------------------
#################################################
# need all above, random
def createDir(dir_path):
  dir_path = os.path.abspath(dir_path)
  if not os.path.isdir(os.path.dirname(dir_path)):
    createDir(os.path.dirname(dir_path))
  os.mkdir(dir_path)

def datasetGenerator(org_dir, target_dir, azims, elevs, dists, n_each):
  # **************use absolute path**************
  org_dir = os.path.abspath(org_dir)
  target_dir = os.path.abspath(target_dir)
  # ********make sure the params are OK**********
  for azim in azims:
    if azim%5!=0 or azim>360 or azim<0:
      print("ERROR: azims {0} is not right.".format(azim))
      return -1
  if elevs != [0]:
    print("ERROR: elev is only allowed to be 0!")
    return -1
  DISTS = [20,30,40,50,75,100,130,160]
  for distance in dists:
    if distance not in DISTS:
      print("ERROR: distance {0} is not allowed.".format(distance))
      print("distance is only allowed to be {}.".format(str(DISTS)))
      return -1
  # ********check the target_dir*****************
  if os.path.isdir(target_dir):
    print("ERROR: target_dir already exists!")
    return -1
  createDir(target_dir)
  # ********get the wav file list****************
  org_file_list = listWavFile(org_dir)
  if n_each > len(org_file_list):
    print("WARNING: n_each is too large, using a smaller one instead.")
    n_each = len(org_file_list)
  # ********generate*****************************
  for azim in azims:
    for elev in elevs:
      for distance in dists:
        for file_name in random.sample(org_file_list,n_each):
          directionGenerator(file_name, azim, distance, target_dir)
  return 1

#################################################
# ------------extract the azim-------------------
#################################################
def getAzim(str):
  m = re.match(r'.*azim(\d+)_.*', str)
  return int(m.group(1))
  
  
#################################################
# ------------main function----------------------
#################################################
if __name__=='__main__':
  org_dir = 'TIMIT\\train'
  target_dir = 'DIRECTION\\train'
  azims = [0,30,60,90]
  elevs = [0]
  dists = [100, 160]
  n_each = 20
  datasetGenerator(org_dir, target_dir,azims,elevs,dists,n_each)
  
  
  
  