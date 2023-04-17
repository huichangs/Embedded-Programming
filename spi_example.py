import spidev
import time

spi = spidev.SpiDev()

spi.open(0, 0)

while True:
    try:
        response = spi.xfer2([0xAA, 0xFF])
        print(response)
        time.sleep(1)
    except KeyboardInterrupt:
        spi.close()
