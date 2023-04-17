import RPi.GPIO as gpio
import time

pin_list = ['abcdef', 'bc', 'abged', 'abcdg', 'fgdbc', 'afgcd']

port_list = [4, 17, 27, 22,5, 6, 13]
port_table = {'a' : 4, 'b' : 17, 'c' : 27, 'd' : 22, 'e': 5, 'f' : 6, 'g':13}

def light_number(t_str):
    for t_port_num in port_list:
        gpio.output(t_port_num, gpio.LOW)
    for elem in t_str:
        t_number = port_table[elem]
        gpio.output(t_number, gpio.HIGH)

is_pin_on = 0

gpio.setmode(gpio.BCM)

curr_num = 0

for t_port_num in port_list:
    gpio.setup(t_port_num, gpio.OUT)
    gpio.output(t_port_num, gpio.LOW)

try:
    while 1:
        curr_str = pin_list[curr_num]
        light_number(curr_str)
        curr_num += 1
        curr_num = curr_num % 10
        time.sleep(1)
except KeyboardInterrupt:
    gpio.cleanup()

