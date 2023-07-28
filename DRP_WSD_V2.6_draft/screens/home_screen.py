from kivy.lang import Builder
from kivy.logger import Logger
from screens.base import BaseScreen
from settings import ADMIN_PASSWORD, DEBUG, DEVICES
from utils.common import is_rpi, get_config, update_config_file
from utils.db import get_sensor_data
from utils.constant import MQTT_ZERO
from widgets.dialog import PasswordDialog
from widgets.snackbar import Snackbar


Builder.load_file('screens/home_screen.kv')


class HomeScreen(BaseScreen):

    show_back_button = False

    def on_pre_enter(self, *args):
        super(HomeScreen, self).on_pre_enter(*args)
        if not get_config()['chart'] and 'btn_chart' in self.ids:
            self.ids.box_bottom.remove_widget(self.ids.btn_chart)
            self.ids.pop('btn_chart', None)

    def on_btn_weights(self):
        self.switch_screen('weight_screen')

    def on_logo_long_pressed(self):
        if is_rpi() or not DEBUG:
            dlg = PasswordDialog(pwd=ADMIN_PASSWORD)
            dlg.bind(on_success=self.on_pwd_correct)
            dlg.open()
        else:
            self.on_pwd_correct()

    def on_pwd_correct(self, *args):
        self.switch_screen('calibration_screen')

    def on_btn_chart(self):
        self.switch_screen('chart_screen')

    def on_btn_mass_center(self):
        self.switch_screen('center_of_mass_screen')

    def on_btn_settings(self):
        self.switch_screen('settings_screen')

    def show_long_press_toast(self):
        Snackbar(text="  Press and Hold button to confirm  ", background_color=(.3, .1, .8, .5), duration=1.5).show()

    def on_btn_zero_weights(self):
        Logger.info('WSD: Setting zero offset of all weights.')
        Snackbar(text="  Setting Zero Weight offset for all tires.  ", background_color=(.1, .6, .3, .5), duration=1.5).show()
        conf = get_config()
        for dev in DEVICES:
            data = self.app.state[dev] # most recent reading
            for _type in ['weight_wheel', 'weight_bs', ]:
                conf['zero'][dev][_type] = data[_type] + conf['zero'][dev][_type] # strip current zero offset to get raw reading
                #self.app.publish_mqtt_message(topic=MQTT_ZERO.format(device=dev, type=_type), payload='START')
        update_config_file(conf)

    def on_btn_zero_travel(self):
        Logger.info('WSD: Setting zero offset of all potentiometers.')
        Snackbar(text="  Setting Zero Travel offset for all tires.  ", background_color=(.1, .6, .3, .5), duration=1.5).show()
        conf = get_config()
        for dev in DEVICES:
            data = self.app.state[dev] # most recent reading
            conf['zero'][dev]['potentiometer'] = data['potentiometer'] + conf['zero'][dev]['potentiometer'] # strip current zero offset to get raw reading
            #self.app.publish_mqtt_message(topic=MQTT_ZERO.format(device=dev, type='potentiometer'), payload='START')
        update_config_file(conf)

