''' This module performs the following functions:
    1) GCC() estimate the time delay of the wav signal
'''


def GCC(wave_data, params, weight_fun=None, frame_len=512):
  x1 = wave_data[:,0]
  x2 = wave_data[:,1]
  freq = params[2]
  