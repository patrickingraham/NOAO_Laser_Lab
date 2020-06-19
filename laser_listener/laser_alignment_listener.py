import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import logging
from gpiozero import LED
from gpiozero import Button
from time import sleep

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.propagate = True

relay = LED(16)
# Switch goes from 3.3V to GPIO, so need to set pull_up = False
restart_button = Button(23, pull_up=False)

def record_data(duration, fs):
    logger.debug('Check input settings')
    sd.check_input_settings(device=input, samplerate=fs, channels=1)
    logger.debug(f'Starting to record for {duration} seconds')
    data = sd.rec(frames=int(duration * fs), samplerate=fs, channels=1, blocking=True)
    # sd.wait()
    return data


def analyze_data(data, fs):

    # average the tracks
#    a = (data.T[0] + data.T[1])/2.0
    a = data.T[0]
    # Make the array an even size
    if (len(a) % 2) != 0:
        logger.debug(f'Length of a is {len(a)}, removing last value')
        a = a[0:-1]
        logger.debug(f'Length of a is now {len(a)}')

    # sample points
    N = len(a)
    # sample spacing
    T = 1.0 / fs

    yf0 = fft(a)
    # but only need half the array
    yf = yf0[:N//2]
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    psd = abs((2.0/N)*yf) ** 2.0

    # Only plot in debug mode
    if logger.level >= logging.DEBUG:
        plot_data(data, fs, xf, yf, psd)

    # check if signal is detected
    # threshold is in sigma over the range of 950-1050 Hz
    threshold = 10

    logger.debug(f'Median of frequency vals are {(np.median(xf[(xf > 995) * (xf < 1005)])):0.2f}')
    psd_at_1kHz = np.max(psd[(xf > 995) * (xf < 1005)])
    bkg = np.median(psd[(xf > 950) * (xf < 1050)])

    logger.debug(f'PSD max value in frequency window of 995-1050 Hz is {(psd_at_1kHz / bkg):0.2f} sigma')

    logger.debug(f'Median value over range from 900-1000 Hz is {bkg:0.2E}')
    condition = (psd_at_1kHz) > threshold * bkg
    if condition:
        return True
    else:
        return False

def plot_data(data, fs, xf, yf, psd):

    length = data.shape[0] / fs

    plt.clf()
    time = np.linspace(0., length, data.shape[0])
    plt.subplot(1, 3, 1)
    plt.plot(time, data[:, 0], label="Left channel")
    plt.plot(time, data[:, 1], label="Right channel")
    plt.xlim(0, 1e-2)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")


    plt.subplot(1, 3, 2)
    plt.plot(xf, psd, '.-')
    plt.xlim(0, 1300)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD [units TBD]')
    plt.draw()
    plt.pause(0.001)

    plt.subplot(1, 3, 3)
    plt.plot(xf, psd, '.-')
    plt.xlim(900, 1100)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD [units TBD]')
    plt.draw()
    plt.pause(0.001)

def open_laser_interrupt():

    relay.off()
    logger.info('Laser interrupt opened')

def close_laser_interrupt():

    relay.on()
    logger.info('Laser Interrupt Activated, laser propagation disabled')
    
def restart():
    
    logger.info('Reset putton pushed')
    open_laser_interrupt()

def get_relay_status():
    
    # bits are flipped since relay.value returns a 0 when it's able to propagate
    status = not relay.value
    
    return status

def main(time, fs):
    logger.info('Starting monitoring loop')

    # Set a callback on the button such that when it is pushed the relay gets turned back on
    restart_button.when_pressed = restart
    
    # Declare how many iterations have to be above the threshold to shut off
    # the laser
    count_threshold = 10
    count = 0

    # Loop until broken
    while(count >= 0):
        
        if get_relay_status() is True:
            data = record_data(time, fs)
            result = analyze_data(data, fs)

            if result and count > count_threshold-1:
                logger.warning('Detected misalignment in audible safety circuit')
                close_laser_interrupt()
            elif result:
                logger.info(f'Experienced value above threshold {count+1} times')
                count += 1
            else:
                count = 0
        else:
            sleep(1)


if __name__ == "__main__":

    logger.debug(f'Available devices are: {sd.query_devices()}')

    input = 2
    output = 4
    # sd.default.device = (1, 2)              # 2 works for output with IC94 sound setup input never worked
    sd.default.device = (input, output)

    #print(sd.query_devices(input))
    fs = sd.query_devices(input)['default_samplerate']
    time = 0.1 #  time sampling

    logger.info(f'Using audio device is {sd.default.device}')
    logger.info(f'Samplerate set to {fs}')
    logger.info(f'Sample length is {time}')

    logger.info('Opening laser interrupt to enable operation')

    open_laser_interrupt()
    
    main(time, fs)
