import RPi.GPIO as gpio
import time

is_pin_on = 0
pwm_pin = 12

gpio.setmode(gpio.BCM)
gpio.setup(pwm_pin, gpio.OUT)

pi_pwm = gpio.PWM(pwm_pin, 1000)
pi_pwm.start(0)

try:
    while 1:
        for duty in range(0, 101, 1):
            pi_pwm.ChangeDutyCycle(duty)
            time.sleep(0.01)
        time.sleep(0.5)
        
        for duty in range(100, -1, -1):
            pi_pwm.ChangeDutyCycle(duty)
            time.sleep(0.01)
        time.sleep(0.5)
except KeyboardInterrupt:
    gpio.cleanup()

