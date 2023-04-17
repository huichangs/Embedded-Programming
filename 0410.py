import smbus
import time
import RPi.GPIO as gpio

is_pin_on = 0

gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.IN)
gpio.setup(17, gpio.OUT)

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)
A1 = 0x41
x_value = 0
y_value = 0

try:
    while True:
        bus.write_byte(address,A0)
        x_value = bus.read_byte(address)
        bus.write_byte(address,A1)
        y_value = bus.read_byte(address)
        print(x_value, y_value)
        
        is_pin_on = gpio.input(4)
        if is_pin_on == 0:
            print('on')
        else:
            print('off')
                
        time.sleep(0.1)
except KeyboardInterrupt:
    gpio.cleanup()
