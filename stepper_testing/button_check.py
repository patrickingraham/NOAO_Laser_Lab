from gpiozero import LED, Button
from signal import pause

GPIO_PIN=21 # Motor Top
#GPIO_PIN=20 # Idler Top

def pressed():
    print(f'Pressed {GPIO_PIN}')
    
def released():
    print(f'Released {GPIO_PIN}')

button = Button(GPIO_PIN, pull_up=False)

button.when_pressed = pressed
button.when_released = released


    
pause()