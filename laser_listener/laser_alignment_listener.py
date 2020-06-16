import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import logging
from gpiozero import LED

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.propagate = True

def record_data(duration, fs):
    logger.debug('Check input settings')
    sd.check_input_settings(device=input, samplerate=fs, channels=2)
    logger.debug(f'Starting to record for {duration} seconds')
    data = sd.rec(frames=int(duration * fs), samplerate=fs, channels=2, blocking=True)
    # sd.wait()
    return data


def analyze_data(data, fs):

    # average the tracks
    a = (data.T[0] + data.T[1])/2.0

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

    logger.debug(f'Median of frequency vals are {np.median(xf[(xf > 995) * (xf < 1005)])}')
    psd_at_1kHz = np.max(psd[(xf > 995) * (xf < 1005)])
    bkg = np.median(psd[(xf > 950) * (xf < 1050)])

    logger.debug(f'PSD max value in frequency window of 995-1050 Hz is {psd_at_1kHz / bkg} sigma')

    logger.debug(f'Median value over range from 900-1000 Hz is {bkg}')
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

def open_laser_interrupt(relay):

    relay.on()
    logger.info('Laser interrupt opened')

def close_laser_interrupt(relay):

    relay.off()
    logger.info('Laser Interrupt Activated, laser propagation disabled')


def main(time, fs):
    logger.info('Starting monitoring loop')

    # Declare how many iterations have to be above the threshold to shut off
    # the laser
    count_threshold = 10
    count = 0

    # Loop until broken
    while(count >= 0):
        data = record_data(time, fs)
        result = analyze_data(data, fs)

        if result and count > count_threshold-1:
            logger.warning('Detected misalignment in audible safety circuit')
            turn_off_laser()
            break
        elif result:
            logger.info(f'Experienced value above threshold {count+1} times')
            count += 1
        else:
            count = 0


if __name__ == "__main__":

    logger.debug(f'Available devices are: {sd.query_devices()}')

    input = 6
    output = 6
    # sd.default.device = (1, 2)              # 2 works for output with IC94 sound setup input never worked
    sd.default.device = (input, output)

    #print(sd.query_devices(input))
    fs = sd.query_devices(input)['default_samplerate']
    time = 0.1 #  time sampling

    logger.info(f'Using audio device is {sd.default.device}')
    logger.info(f'Samplerate set to {fs}')
    logger.info(f'Sample length is {time}')

    logger.info('Opening laser interrupt to enable operation')
    relay = LED(16)
    open_laser_interrupt(relay)

    main(time, fs)