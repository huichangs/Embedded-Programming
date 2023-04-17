import RPi.GPIO as gpio
import time

is_pin_on = 0
pwm_pin = 7

gpio.setmode(gpio.BOARD)
gpio.setup(pwm_pin, gpio.OUT)

pi_pwm = gpio.PWM(pwm_pin, 100)
pi_pwm.start(50)

frequency_list = [16.35, 261.63, 293.66, 329.63, 349.23, 392.00, 392.00, 440.00, 493.88, 523.25, 16.35]

len_frequency_list = len(frequency_list)
idx = 0

try:
    while 1:
        pi_pwm.ChangeFrequency(frequency_list[idx])
        time.sleep(1)
        idx += 1
        idx %= len_frequency_list
        print(frequency_list[idx])
except KeyboardInterrupt:
    gpio.output(pwm_pin, gpio.LOW)
    gpio.cleanup()

