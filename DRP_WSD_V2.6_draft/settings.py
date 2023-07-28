# -*- coding: iso8859-15 -*-

INIT_SCREEN = 'home_screen'


DEVICES = ['LF', 'RF', 'LR', "RR"]
DEVICES_LONG = ['LEFT FRONT', 'RIGHT FRONT', 'LEFT REAR', 'RIGHT REAR']


MQTT_HOST = 'localhost'
MQTT_PORT = 1883

MONGO_HOST = MQTT_HOST

AD1230_RESOLUTION = 20      # Resolution of AD1230(20 bit).
MAX_WEIGHT = 5000           # Maximum possible weights using AD1230(5000lb).
RATE_KG2LBS = .453592
RATE_AD1230 = MAX_WEIGHT * RATE_KG2LBS / 2 ** 20

#passwords will be hashed during compilation.
#if skipping the compile step, replace the following passwords with their sha256 hash.
ADMIN_PASSWORD = "drp/wsd"
CONFIG_PASSWORD = "settings/drp"

INTERVAL = 1               # Saving interval of the sensor data(seconds)

DEBUG = False


# LPF parameters

LPF_ORDER = 6
LPF_FS = 80.0
LPF_CUTOFF = 10


# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
ADC_GAIN = 1


try:
    from local_settings import *
except ImportError:
    pass
