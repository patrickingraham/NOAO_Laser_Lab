from gpiozero import LED
from time import sleep

led = LED(21)

while True:
    led.on()
    print('Now On')
    sleep(2)
    led.off()
    print('Now Off')
    sleep(2)