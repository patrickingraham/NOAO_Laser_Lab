from time import sleep
import time
import pigpio
import asyncio

def generate_ramp(ramp):
    """Generate ramp wave forms.
    ramp:  List of [Frequency, Steps]
    """
    pi.wave_clear()     # clear existing waves
    length = len(ramp)  # number of ramp levels
    wid = [-1] * length

    # Generate a wave per ramp level
    for i in range(length):
        frequency = ramp[i][0]
        micros = int(500000 / frequency)
        wf = []
        wf.append(pigpio.pulse(1 << STEP, 0, micros))  # pulse on
        wf.append(pigpio.pulse(0, 1 << STEP, micros))  # pulse off
        pi.wave_add_generic(wf)
        wid[i] = pi.wave_create()

    # Generate a chain of waves
    chain = []
    for i in range(length):
        steps = ramp[i][1]
        x = steps & 255
        y = steps >> 8
        chain += [255, 0, wid[i], 255, 1, x, y]

    return chain


DIR = 12     # Direction GPIO Pin
STEP = 18    # Step GPIO Pin

#Set switch to 13 but there is nothing plugged into it
SWITCH = 13  # GPIO pin of switch 

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set up input switch
pi.set_mode(SWITCH, pigpio.INPUT)
pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)


# Ramp up
chain = generate_ramp([[320, 200],
	       [500, 400],
	       [800, 500],
	       [1000, 700],
	       [1600, 900],
	       [2000, 10000]])

print(f'PWM frequency is {pi.get_PWM_frequency(STEP)} Hz')

# Command returns immediately!
pi.wave_chain(chain)  # Transmit chain 
sleep(4)
#pi.wave_tx_stop()

print('Chain Completed')
print(f'PWM frequency is {pi.get_PWM_frequency(STEP)} Hz')

# Set duty cycle and frequency
pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Off
pi.set_PWM_frequency(STEP, 500)  # 500 pulses per second

try:
    while True:
        pi.write(DIR, pi.read(SWITCH))  # Set direction
        sleep(.1)

except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
finally:
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off
    pi.stop()