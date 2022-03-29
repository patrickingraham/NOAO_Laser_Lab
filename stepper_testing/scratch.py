##        #pi.write(DIR, CW) # start rotating
##ramp_def = [[320, 20], [500, 40],[800, 50], [1000, 70],
##       [1600, 90],
##       [2000, 1000]]
##
##steps=0
##for speeds in ramp_def:
##    steps += speeds[1] 
##
##print(f'total steps is {steps}')

from gpiozero import Button
from signal import pause

def say_hello():
    print("Hello!")
    #print(f'Value of {value}')
    
def say_goodbye():
    print("Goodbye!")

button = Button(27, pull_up=True)

button.when_pressed = say_hello
button.when_released = say_goodbye

pause()