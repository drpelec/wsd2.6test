import gc
import datetime
import subprocess
import traceback
import random
import time

# Import this before Kivy
import conf.config_before
from kivy.app import App
# Import after Kivy
import conf.config_kivy
import widgets.factory_reg

from ADS1x15 import ADS1115

from kivy.clock import mainthread, Clock
from kivy.logger import Logger
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import FadeTransition
from kivy.base import ExceptionHandler, ExceptionManager
from screens.screen_manager import screens, sm
from utils.common import is_rpi, get_free_gpu_size, disable_screen_saver, check_running_proc, get_config, \
    update_config_file
from utils.db import save_sensor_data
from settings import *
from paho.mqtt.client import Client
from utils.constant import MQTT_POTENTIOMETER, MQTT_WEIGHT_WHEEL, MQTT_WEIGHT_BS
from widgets.snackbar import Snackbar


mqtt_client = Client()


class WSDExceptionHandler(ExceptionHandler):

    def handle_exception(self, exception):
        Logger.exception(exception)
        _app = App.get_running_app()
        _app.save_exception(traceback.format_exc(limit=20))
        _app.switch_screen('error_screen')
        return ExceptionManager.PASS


ExceptionManager.add_handler(WSDExceptionHandler())


class WirelessScaleDisplayApp(App):

    current_screen = None
    exception = None
    state = {}
    conn_type = StringProperty()
    _clk_wired = ObjectProperty(None, allownone=True)
    _clk_store = ObjectProperty(None, allownone=True)

    is_recording = BooleanProperty(False)
    spinner = ObjectProperty()
    
    adc_dev = {}
    dev_err = {}

    average_reading_count = 5

    def build(self):
        for d in DEVICES:
            self.dev_err[d] = False
            self.state[d] = {
                'weight_wheel': 0.,
                'weight_bs': 0.,
                'potentiometer': 0.,
            }
            self.totals[d] = {
                'weight_wheel': 0.,
                'weight_bs': 0.,
                'potentiometer': 0.,
            }
            self.values[d] = {
                'weight_wheel': [],
                'weight_bs': [],
                'potentiometer': [],
            }
        mqtt_client.on_connect = on_mqtt_connected
        mqtt_client.on_message = self.on_mqtt_messaged
        mqtt_client.connect_async(MQTT_HOST, MQTT_PORT)
        mqtt_client.loop_start()

        self.set_connection_type(get_config()['mode'])
        adcLF = ADS1115(address=0x48, busnum=1)
        adcRF = ADS1115(address=0x49, busnum=1)
        adcLR = ADS1115(address=0x4a, busnum=1)
        adcRR = ADS1115(address=0x4b, busnum=1)

        self.adc_dev = { 'LF': adcLF, 'RF': adcRF, 'LR': adcLR, 'RR': adcRR }

        self.switch_screen(INIT_SCREEN)
        return sm

    def switch_screen(self, screen_name, duration=.3):
        s_time = time.time()
        if sm.has_screen(screen_name):
            sm.current = screen_name
        else:
            screen = screens[screen_name](name=screen_name)
            sm.transition = FadeTransition(duration=duration)
            sm.switch_to(screen)
            msg = ' :: GPU - {}'.format(get_free_gpu_size()) if is_rpi() else ''
            Logger.info('WSD: ===== Switched to {} screen {}, Elapsed: {} ====='.format(
                screen_name, msg, time.time() - s_time))
            #if self.current_screen:
                #sm.remove_widget(self.current_screen)
                #del self.current_screen
                #gc.collect()

    def on_mqtt_messaged(self, *args):
        topic = args[2].topic
        msg = args[2].payload.decode('utf-8')
        self.parse_mqtt_message(topic, msg)

    @mainthread
    def parse_mqtt_message(self, topic, value):
        Logger.debug('MQTT: {} :: New message - `{} - {}`'.format(datetime.datetime.now(), topic, value))
        t = topic.split('/')
        dev = t[0]
        msg_type = t[1]

        if msg_type.startswith('weight_'):
            val_ad1230 = float(value) * RATE_AD1230 * get_config()['calibrate'][dev][msg_type]
            self.state[dev][msg_type] = round(val_ad1230, 1)

        elif msg_type == 'potentiometer':
            milli_volt = float(value)
            val = milli_volt / 1000.0 * get_config()['calibrate'][dev][msg_type]
            self.state[dev][msg_type] = round(val, 3)
        else:
            return

        sm.current_screen.update_screen()

    def _store_sensor_data(self):
        for dev in DEVICES:
            if DEBUG:
                data = dict(
                    weight_wheel=random.randint(-100, 2000),
                    weight_bs=random.randint(-100, 750),
                    potentiometer=random.randint(0, 200)
                )
            else:
                data = {}
                for t in {'weight_wheel', 'weight_bs', 'potentiometer'}:
                    data[t] = self.state[dev][t]
            # Ignore invalid data
            if not all([v == 0 for v in data.values()]):
                save_sensor_data(device=dev, value=data)

    @staticmethod
    def publish_mqtt_message(topic, payload):
        Logger.info('MQTT: Publishing a message, topic: `{}`, payload: `{}`'.format(topic, payload))
        mqtt_client.publish(topic=topic, payload=payload)

    def save_exception(self, ex):
        self.exception = ex

    def get_exception(self):
        return self.exception

    def set_connection_type(self, conn_type):
        c = get_config()
        c['mode'] = conn_type
        update_config_file(c)
        if self.conn_type != conn_type:
            self.conn_type = conn_type
            Logger.info('WSD: Switched mode - {}'.format(self.conn_type.capitalize()))
            if self.conn_type == 'wifi':
                if self._clk_wired:
                    self._clk_wired.cancel()
                    self._clk_wired = None
            else:
                self._clk_wired = Clock.schedule_interval(lambda dt: self.read_wired_data(), 0.2)

    @mainthread
    def calibrate_sensor(self, direction, dev, new_val):
        conf = get_config()
        new_ratio = get_config()['calibrate'][direction][dev] * new_val / self.state[direction][dev]
        if new_ratio < 0.001:
            Snackbar(text="New Ratio is too small! ({})".format(new_ratio), background_color=(.8, 0, .3, .5)).show()
            return
        c = get_config()
        c['calibrate'][direction][dev] = new_ratio
        update_config_file(c)

    def rolling_average(self, dev, msg_type, new):
        if len(self.values[dev][msg_type]) >= self.average_reading_count:
         old = self.values[dev][msg_type].pop(0) # oldest reading
        self.totals[dev][msg_type] -= old # remove oldest reading from average

        self.values[dev][msg_type].append(new) # newest reading goes to end of the list
        self.totals[dev][msg_type] += new

        return (self.totals[dev][msg_type] / self.average_reading_count)
        

    def read_wired_data(self):
        conf = get_config()
        for d in DEVICES:
            adc = self.adc_dev[d]
            self.dev_err[d] = False
            if not adc: continue

            try:
                # read pot
                msg_type = 'potentiometer'
                pot = float(adc.read_adc(2)) # pot
                val = pot / 1000.0 * conf['calibrate'][d][msg_type]

                val = self.rolling_average(d, msg_type, val)

                self.state[d][msg_type] = round(val - conf['zero'][d][msg_type], 3)

                # read wheel weight
                msg_type = 'weight_wheel'
                ww = float(adc.read_adc(1)) # ww
                val_ad1230 = ww * RATE_AD1230 * conf['calibrate'][d][msg_type]
                #self.state[d][msg_type] = round(val_ad1230 - conf['zero'][d][msg_type], 1)

                val = self.rolling_average(d, msg_type, val)
                self.state[d][msg_type] = round(val_ad1230 - conf['zero'][d][msg_type])

                # read bump stop
                msg_type = 'weight_bs'
                ww = float(adc.read_adc(0)) # bs
                val_ad1230 = ww * RATE_AD1230 * conf['calibrate'][d][msg_type]
                #self.state[d][msg_type] = round(val_ad1230 - conf['zero'][d][msg_type], 1)

                val = self.rolling_average(d, msg_type, val)
                self.state[d][msg_type] = round(val_ad1230 - conf['zero'][d][msg_type])
            except IOError:
                self.dev_err[d] = True
                #Snackbar(text="IO Error: {}".format(d), background_color=(.8, 0, .3, .5)).show()
                

        sm.current_screen.update_screen()
    
    def zero_wheel(self, device, _type):
        conf = get_config()
        conf['zero'][device][_type] = self.state[device][_type] + conf['zero'][device][_type] # strip current zero offset to get raw reading
        update_config_file(conf)  
        
    def zero_all(self):
        conf = get_config()
        for dev in DEVICES:
            data = self.state[dev] # most recent reading
            for _type in ['weight_wheel', 'weight_bs', 'potentiometer' ]:
                conf['zero'][dev][_type] = data[_type] + conf['zero'][dev][_type] # strip current zero offset to get raw reading
        update_config_file(conf)  
    
    def start_recording(self):
        self.is_recording = True
        if self._clk_store is None:
            self._clk_store = Clock.schedule_interval(lambda dt: self._store_sensor_data(), INTERVAL)

    def stop_recording(self):
        self.is_recording = False
        if self._clk_store:
            self._clk_store.cancel()
            self._clk_store = None


def on_mqtt_connected(client, userdata, flags, rc):
    Logger.info('MQTT: Connected to the Broker, Host: {}, Port: {}, UserData: {}, Flags: {}, Result code: {}'.format(
        MQTT_HOST, MQTT_PORT, userdata, flags, rc))
    for dev in DEVICES:
        mqtt_client.subscribe(MQTT_WEIGHT_WHEEL.format(device=dev))
        mqtt_client.subscribe(MQTT_WEIGHT_BS.format(device=dev))
        mqtt_client.subscribe(MQTT_POTENTIOMETER.format(device=dev))


if __name__ == '__main__':
    app = WirelessScaleDisplayApp()
    app.run()
