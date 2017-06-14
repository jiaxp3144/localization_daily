from wavlib import *

if __name__ == '__main__':
  path = 'F:\direction_gen\matlab'
  wav_list = listWavFile(path)
  for item in wav_list:
    print(item)
  
  if wav_list:
    print('Testing audioRead...')
    (wave_data, params) = audioRead(wav_list[0])
    print('Testing audioWrite...')
    filename = 'testfile.wav'
    if os.path.isfile(filename):
      os.remove(filename)
    audioWrite(filename, params, wave_data)
    print('Testing audioPlay...')
    audioPlay(wave_data, params)