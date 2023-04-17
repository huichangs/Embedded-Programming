import RPi.GPIO as gpio
import time

is_pin_on = 0

gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.IN)


try:
    while 1:
        is_pin_on = gpio.input(4)
        if is_pin_on == 0:
            print('off')
        else:
            print('on')
        time.sleep(0.1)
except KeyboardInterrupt:
    gpio.cleanup()

