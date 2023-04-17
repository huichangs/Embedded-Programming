import serial
import time


ser = serial.Serial("/dev/ttyS0")
ser.baudrate = 57600

try:
    while True:
        ser.write(bytes(b"hello\n"))
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing serial port...")
    ser.close()
    pass
