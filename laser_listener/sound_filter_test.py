import numpy as np
import sounddevice as sd

tmp=sd.query_devices()

print(f'This is a test and the tmp variable {tmp}')

print(sd.query_devices())

import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft


fs, data = wav.read('1kHz_noise_1s.wav') # load the data
print(f"number of channels = {data.shape[1]}")

length = data.shape[0] / fs
print(f"length = {length}s")

time = np.linspace(0., length, data.shape[0])
# plt.plot(time, data[:, 0], label="Left channel")
# # plt.plot(time, data[:, 1], label="Right channel")
# # plt.xlim(0, 1e-2)
# # plt.legend()
# # plt.xlabel("Time [s]")
# # plt.ylabel("Amplitude")
# # plt.show()

a = data.T[0] # this is a two channel soundtrack, I get the first track

# Make the array an even size
if (len(a) % 2) != 0:
    print(f'Length of a is {len(a)}, removing last value')
    a = a[0:-1]
    print(f'Length of a is {len(a)}')

# sample points
N = len(a)
# sample spacing
T = 1.0/fs

yf = fft(a)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.xlim(0,2000)
plt.show()

psd = abs(yf)**2.0



