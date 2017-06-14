''' this script test datalib.py
    1> test readHrir(), use it read the hrir data and plot it out
    2> test addDirection(), add direction to the test.wav
'''

import matplotlib.pyplot as plt
import datalib
import wavlib

def testReadHrir():
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
  
def testAddDirection():
  # test settings
  for azim in [30]:#range(0,361,5):
    elev = 0
    dist = 160
    hrir_path = r'..\..\resources\hrir_txt'
    # test addDirection
    (wave_data, params) = wavlib.audioRead('test.wav')
    (wave_data_new, params_new) = datalib.addDirection(\
      wave_data, params, azim, elev, dist, hrir_path)
    #wavlib.audioPlay(wave_data_new,params_new)
    wavlib.audioWrite('test_{0}.wav'.format(azim),params_new,wave_data_new)
    
def testAddNoise():
  file_name = 'test_90.wav'
  noise_file_path = r'..\..\resources\noiseX\white.wav'
  snr = 0
  wave_data, params = wavlib.audioRead(file_name)
  sig_n = datalib.addNoise(wave_data, params, snr, noise_file_path)
  #wavlib.audioPlay(sig_n, params)
  wavlib.audioWrite('test_90_n.wav', params, sig_n)

if __name__=='__main__':
  testAddDirection()