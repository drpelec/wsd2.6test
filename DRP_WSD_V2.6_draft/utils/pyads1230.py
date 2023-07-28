"""
    Python Wrapper for the ADS1230 Load Cell Board for Raspberry Pi:
        https://www.tindie.com/products/EletroShields/load-cell-nanoshield-ads1230-load-cell-module/

    Connection Guide

    |   RPi    | Load Cell |
     -----------------------
    |   3V3    |    VCC    |
    |   GND    |    GND    |
    |  GPIO8   |    D8     |
    |  GPIO9   |    SDO    |
    |  GPIO11  |    SCK    |

"""
import copy
import threading
import time

try:
    import RPi.GPIO as GPIO
    import spidev
except ImportError:
    print('Failed to import libraries, please install them now')
    exit(-1)


class PyADS1230:

    capacity = 0
    sensitivity = 2
    cs_pin = 8
    miso_pin = 9
    high_gain = True
    mode = 1
    speed = 4000000
    bus = 0
    device_num = 0

    _lock = threading.RLock()
    _val = None
    _stop = threading.Event()

    def __init__(self, capacity=5000, sensitivity=2, cs_pin=8, miso_pin=9,
                 high_gain=True, mode=1, speed=400000, bus=0, device_num=0):
        """
        :param capacity:        Load cell capacity, in gram.
        :param sensitivity:     Load cell sensitivity, in mV/V.
        :param cs_pin:          Chip Select Pin matching the jumper selected on the board.
        :param miso_pin:        MISO pin
        :param high_gain:       True if operating in high gain mode, false if in low gain mode.
        :param mode:            SPI mode
        :param speed:           SPI clock
        :param bus:             SPI bus number
        :param device_num:      SPI device number
        """
        self.capacity = capacity
        self.sensitivity = sensitivity
        self.cs_pin = cs_pin
        self.miso_pin = miso_pin
        self.high_gain = high_gain
        self.mode = mode
        self.speed = speed
        self.bus = bus
        self.device_num = device_num
        self.initialize_gpio()
        self._stop.clear()

    def initialize_gpio(self):
        """
        Initialize GPIO of RPi
        :return:
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.output(self.cs_pin, True)
        GPIO.setup(self.miso_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        return True

    def start(self):
        _spi = spidev.SpiDev()
        _spi.open(self.bus, self.device_num)
        _spi.mode = self.mode
        _spi.lsbfirst = False
        _spi.max_speed_hz = self.speed

        while not self._stop.isSet():
            s_time = time.time()
            GPIO.output(self.cs_pin, False)
            while True:
                if not GPIO.input(self.miso_pin):
                    d = _spi.xfer2([0, 0, 0])
                    break
                if time.time() - s_time > 1:
                    print('Timeout!')
                    return
            GPIO.output(self.cs_pin, True)
            elapsed = time.time() - s_time
            with self._lock:
                self._val = d
            print(d, elapsed)
            time.sleep(max(1 / 80. - elapsed, 0))

    def get_value(self):
        with self._lock:
            val = copy.deepcopy(self._val)
        return val

    def stop(self):
        self._stop.set()


if __name__ == '__main__':

    ads = PyADS1230()

    ads.start()

    try:
        while True:
            ads.get_value()
            time.sleep(.1)
    except KeyboardInterrupt:
        pass
    ads.stop()
