''' this script test datalib.py
    1> test readHrir(), use it read the hrir data and plot it out
    2> test addDirection(), add direction to the test.wav
'''

import matplotlib.pyplot as plt
import datalib
import wavlib

if __name__=='__main__':
  '''
  # test settings
  for azim in range(0,361,5):
    elev = 0
    dist = 160
    hrir_path = r'..\..\resources\hrir_txt'
  '''
  hrir_path = r'..\..\resources\hrir_txt'
  azim = 90
  elev = 0
  dist = 160
  # test readHrir()
  (hrir_r, hrir_l) = datalib.readHrir(hrir_path, azim, elev, dist)
  plt.subplot(211)
  plt.plot(hrir_r)
  plt.subplot(212)
  plt.plot(hrir_l)
  plt.show()
  
  '''
    # test addDirection
    (wave_data, params) = wavlib.audioRead('test.wav')
    (wave_data_new, params_new) = datalib.addDirection(\
      wave_data, params, azim, elev, dist, hrir_path)
    #wavlib.audioPlay(wave_data_new,params_new)
    wavlib.audioWrite('test_{0}.wav'.format(azim),params_new,wave_data_new)
  '''
  hrir_path = r'..\..\resources\hrir_txt'
  azim = 30
  elev = 0
  dist = 160
  (wave_data, params) = wavlib.audioRead('test.wav')
  wave_data_new, params_new = datalib.addDirection(wave_data, params, azim, elev, dist, hrir_path)
  wavlib.audioWrite('test_d.wav',params_new,wave_data_new)