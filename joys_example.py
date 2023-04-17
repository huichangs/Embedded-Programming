import smbus
import time

address = 0x48
A0 = 0x40
bus = smbus.SMBus(1)
A1 = 0x41
x_value = 0
y_value = 0

while True:
    bus.write_byte(address,A0)
    x_value = bus.read_byte(address)
    bus.write_byte(address,A1)
    y_value = bus.read_byte(address)
    print(x_value, y_value)
    time.sleep(0.5)
