import RPi.GPIO as gpio
import time

is_pin_on = 0

gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.OUT)

gpio.output(4, gpio.LOW)

try:
    while 1:
        if is_pin_on == 0:
            gpio.output(4, gpio.HIGH)
            is_pin_on = 1
        else:
            gpio.output(4, gpio.LOW)
            is_pin_on = 0
        time.sleep(1)
except KeyboardInterrupt:
    gpio.output(4, gpio.LOW)
    gpio.cleanup()

