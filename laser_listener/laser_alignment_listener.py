import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import logging
from gpiozero import LED, Button, Device, exc
from time import sleep
from gpiozero.pins.mock import MockFactory
import argparse

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.propagate = True


class LaserListener:

    def __init__(self):
        logger.debug('Initializing')

        # declare framerate
        self.fs = None
        # declare time sampling
        self.duration = None

        # Default setup to use raspberry pi and circuit
        # To use with a simulator
        # Set the default pin factory to a mock factory

        logger.debug(f'Argument passed from command line is {args.simulate}')
        if args.simulate:
            logger.warning('Running in Simulation Mode')
            Device.pin_factory = MockFactory()

        # declare pin settings
        try:
            self.relay = LED(16)
        except exc.BadPinFactory:
            logger.info('Caught BadPinFactory exception. This often results '
                        'when not running the program on a raspberry pi.'
                        'Did you mean to run this in simulation mode (-s) ?')

        self.status = None
        # Switch goes from 3.3V to GPIO, so need to set pull_up = False
        self.restart_button = Button(23, pull_up=False)

    def record_data(self):
        """Records data for a given interval"""
        logger.debug('Check input settings')
        sd.check_input_settings(device=sd.default.device[0],
                                samplerate=self.fs, channels=1)
        logger.debug(f'Starting to record for {self.time} seconds')
        data = sd.rec(frames=int(self.time * self.fs), samplerate=self.fs,
                      channels=1, blocking=True)
        # sd.wait()
        return data

    def analyze_data(self, data):
        """ Analyzes data from recording.
        Checks if PSD is above threshold """

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
        T = 1.0 / self.fs

        yf0 = fft(a)
        # but only need half the array
        yf = yf0[:N//2]
        xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

        psd = abs((2.0/N)*yf) ** 2.0

        # Only plot in debug mode
        if logger.level >= logging.DEBUG:
            self.plot_data(data, self.fs, xf, yf, psd)

        # check if signal is detected
        # threshold is in sigma over the range of 950-1050 Hz
        threshold = 10

        logger.debug('Median of frequency vals are '
                     f'{(np.median(xf[(xf > 995) * (xf < 1005)])):0.2f}')
        psd_at_1kHz = np.max(psd[(xf > 995) * (xf < 1005)])
        bkg = np.median(psd[(xf > 950) * (xf < 1050)])

        logger.debug('PSD max value in frequency window of 995-1050 Hz is '
                     f'{(psd_at_1kHz / bkg):0.2f} sigma')

        logger.debug(f'Median value over range from 900-1000 Hz is {bkg:0.2E}')
        condition = (psd_at_1kHz) > threshold * bkg
        if condition:
            return True
        else:
            return False

    def plot_data(self, data, xf, yf, psd):
        """ Plots the data from a recording """

        length = data.shape[0] / self.fs

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

    def open_laser_interrupt(self):
        """Opens the laser interrupt to allow propagation"""
        self.relay.off()
        logger.info('Laser interrupt opened, laser propagation permitted')

    def close_laser_interrupt(self):

        self.relay.on()
        logger.info('Laser Interrupt Activated, laser propagation disabled')

    def restart(self):
        """Restarts the monitor after a detection when the reset button is
         pushed"""

        logger.info('Reset putton pushed')
        self.open_laser_interrupt()

    def get_relay_status(self):
        """Reports the status of the relay"""
        # bits are flipped since relay.value returns a 0 when it's
        # able to propagate
        self.status = not self.relay.value

        return self.status

    def monitor_loop(self):
        logger.info('Starting monitoring loop')

        # Set a callback on the button such that when it is pushed the relay
        # gets turned back on
        self.restart_button.when_pressed = self.restart

        # Declare how many iterations have to be above the threshold
        # to shut off the laser
        count_threshold = 10
        count = 0

        # Loop until broken
        while(count >= 0):

            if self.get_relay_status() is True:
                data = self.record_data()
                result = self.analyze_data(data)

                if result and count > count_threshold-1:
                    logger.warning('Detected misalignment in '
                                   'audible safety circuit')
                    self.close_laser_interrupt()
                elif result:
                    logger.info('Experienced value above threshold'
                                f' {count+1} times')
                    count += 1
                else:
                    count = 0
            else:
                sleep(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Monitor laser to fiber '
                                                 'coupling using audio '
                                                 'feedback')
    parser.add_argument('-s', '--simulation', dest='simulate',
                        action='store_true',
                        default=False,
                        help='Run monitor in simulation mode '
                             '(without a raspberry pi)')

    args = parser.parse_args()

    # Instantiate the LaserListener Class
    laser_listener = LaserListener()

    logger.debug(f'Available devices are: {sd.query_devices()}')

    # # Raspberry Pi
    # input = 2
    # output = 4
    #
    # # Patrick Laptop on CentOS7 VM
    # input = 6
    # output = 6
    # sd.default.device = (input, output)

    # get framerate for input device
    laser_listener.fs = sd.query_devices(
        sd.default.device[0])['default_samplerate']

    laser_listener.time = 0.1  # time sampling for each measurement

    logger.info(f'Using audio device is {sd.default.device}')
    logger.info(f'Samplerate set to {laser_listener.fs}')
    logger.info(f'Sample length is {laser_listener.time}')

    logger.info('Opening laser interrupt to enable operation')
    laser_listener.open_laser_interrupt()

    # Start the monitor
    laser_listener.monitor_loop()
