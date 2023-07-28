import Adafruit_ADS1x15
from settings import ADC_GAIN


adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)  # Create an ADS1115 ADC (16-bit) instance.


def get_adc_value(channel=0, gain=ADC_GAIN):
    return adc.read_adc(channel, gain=gain)
