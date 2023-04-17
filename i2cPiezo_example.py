import RPi.GPIO as gpio
import smbus
import time

is_pin_on = 0
pwm_pin = 7

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)

gpio.setmode(gpio.BOARD)
gpio.setup(pwm_pin, gpio.OUT)

pi_pwm = gpio.PWM(pwm_pin, 100)
pi_pwm.start(50)


try:
    while 1:
        bus.write_byte(address,A0)
        value = bus.read_byte(address)
        pi_pwm.ChangeFrequency(value)
        print(value)
        time.sleep(0.5)
except KeyboardInterrupt:
    gpio.output(pwm_pin, gpio.LOW)
    gpio.cleanup()

