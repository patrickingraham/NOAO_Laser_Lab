from time import sleep
import time
import RPi.GPIO as GPIO

DIR = 22   # Direction GPIO Pin (Direction)
STEP = 27  # Step GPIO Pin (Pulse)
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

# driver set to 1600 pulses per revolution
pulses_per_rotation = 1600
gearbox_ratio = 20
rot_time = 10 # seconds per rotation  

# Counts required to do a rotation
step_count = pulses_per_rotation * gearbox_ratio
delay = rot_time / step_count /2 # 

start_time = time.time()
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
end_time = time.time()

# Because the sleep is inaccurate this
# time won't match the anticipated time 
print(f'Completed rotation in {end_time-start_time} seconds')
sleep(.5)

#GPIO.output(DIR, CCW)
#for x in range(step_count):
#    GPIO.output(STEP, GPIO.HIGH)
#    sleep(delay)
#    GPIO.output(STEP, GPIO.LOW)
#    sleep(delay)

GPIO.cleanup()