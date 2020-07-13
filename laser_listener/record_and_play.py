# This is a test program to verify functionality of the library

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav


duration = 2.0  # seconds
fs=44100
#fs = 48000


# Patrick Laptop on CentOS7 VM
input=6
output=6
#sd.default.device = (1, 2)              # 2 works for output with IC94 sound setup input never worked
sd.default.device = (input, output)

print(sd.query_devices(input))
fs = sd.query_devices(input)['default_samplerate']


print(f'Default device is {sd.default.device}')
print(f'Default samplerate is {fs}')


if True:
      print('Check input settings')
      sd.check_input_settings(device=input, samplerate=fs, channels=2)
      print(f'Starting to record for {duration} seconds')
      data = sd.rec(frames=int(duration * fs), samplerate=fs, channels=2, blocking=True)
      # sd.wait()
      length = data.shape[0] / fs
      print(f"length = {length}s")

      time = np.linspace(0., length, data.shape[0])
      plt.plot(time, data[:, 0], label="Left channel")
      plt.plot(time, data[:, 1], label="Right channel")
      plt.xlim(0, 1e-2)
      plt.legend()
      plt.xlabel("Time [s]")
      plt.ylabel("Amplitude")
      plt.show()

      print(f'Median of channel 1 is {np.median(data[:,0])}')
      print(f'Median of channel 2 is {np.median(data[:,1])}')

      print('Done recording')

# now play it back
if False:
      print('Playing back')

      # fs, data = wav.read('1kHz_noise_1s.wav') # load the data

      print(f'Length of data to be played is {len(data)} with a median value '
            f'chan 1/2 is {np.median(data[:,0])}, {np.median(data[:,1])}')
      print(f'Framerate of data to be played is {len(data)}')

      sd.play(data, fs, blocking=True)

      print('Stopping')
      sd.stop()
