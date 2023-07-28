from datetime import datetime
from functools import partial
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.logger import Logger
from kivy.lang import Builder
from screens.base import BaseScreen
from settings import DEVICES, DEBUG, CONFIG_PASSWORD
from utils.common import is_rpi
from utils.constant import MQTT_CALIBRATE, MQTT_ZERO
from widgets.dialog import InputDialog, PasswordDialog
from widgets.date_time_dialog import DateTimeDialog
from widgets.snackbar import Snackbar


Builder.load_file('screens/calibration_screen.kv')


class CalibrationScreen(BaseScreen):
    CurrentTime = StringProperty("")
    _clk_update = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        self.CurrentTime = datetime.now().strftime('%Y-%m-%d %I:%M %p')
        super(CalibrationScreen, self).__init__(**kwargs)
        for dev in DEVICES:
            self.ids[dev].bind(on_calibrate=self._on_calibrate)
            self.ids[dev].bind(on_zero=self._on_zero)

    def on_enter(self, *args):
        super(CalibrationScreen, self).on_enter(*args)
        self._clk_update = Clock.schedule_interval(lambda dt: self._update_time(), 1)
        self._update_time()

    def on_pre_leave(self, *args):
        super(CalibrationScreen, self).on_pre_leave(*args)
        if self._clk_update:
            self._clk_update.cancel()
            self._clk_update = None

    def update_screen(self):
        state = self.app.state
        for dev in state.keys():
            for _type in state[dev].keys():
                if _type in self.ids[dev].ids:
                    self.ids[dev].ids[_type].text = str(state[dev][_type])
        self.CurrentTime = datetime.now().strftime('%Y-%m-%d %I:%M %p')
        self.ids['CurrentTime'].text = self.CurrentTime

    def _on_calibrate(self, *args):
        """
        Callback when the `Calibrate` button of a WSDCalibrateItem widget is pressed.
        :param args: (WSDCalibrateItem, sensor_type)
        :return:
        """
        direction = args[0].direction
        dev = args[1]
        title = 'Please input current {}'.format(
            'travel value in inches' if dev == 'potentiometer' else 'weight in pounds')
        dlg = InputDialog(title=title, input_filter='float')
        dlg.bind(on_confirm=partial(self._on_calibrate_dlg_confirm, direction, dev))
        dlg.open()

    def _on_calibrate_dlg_confirm(self, direction, dev, dlg, value):
        if self.app.state[direction][dev] == 0:
            Snackbar(text="  Can't Calibrate while its reading value is 0!  ", background_color=(.8, 0, .3, .5)).show()
        else:
            Logger.info('WSD: Calibrating `{}`/`{}`, new val: {}'.format(direction, dev, value))
            #self.app.publish_mqtt_message(topic=MQTT_CALIBRATE.format(device=direction, type=dev), payload='START')
            self.app.calibrate_sensor(direction=direction, dev=dev, new_val=float(value))

    def _on_zero(self, *args):
        """
        Callback when the `Zero` button of a WSDCalibrateItem widget is pressed.
        :param args: (WSDCalibrateItem, sensor_type)
        :return:
        """
        direction = args[0].direction
        dev = args[1]
        Logger.info('WSD: Setting zero offset of `{}`/`{}`'.format(direction, dev))
        self.app.publish_mqtt_message(topic=MQTT_ZERO.format(device=direction, type=dev), payload='START')
        self.app.zero_wheel(direction, dev)

    def on_btn_zero_all(self):
        Logger.info('WSD: Setting zero offset of all sensors.')
        self.app.zero_all()
        #for dev in DEVICES:
        #    for _type in ['weight_wheel', 'weight_bs', 'potentiometer']:
        #        self.app.publish_mqtt_message(topic=MQTT_ZERO.format(device=dev, type=_type), payload='START')

    def on_btn_settings(self):
        if is_rpi() or not DEBUG:
            dlg = PasswordDialog(pwd=CONFIG_PASSWORD)
            dlg.bind(on_success=self._on_settings_pwd_correct)
            dlg.open()
        else:
            self._on_settings_pwd_correct()

    def _on_settings_pwd_correct(self, *args):
        self.switch_screen('settings_screen')

    def on_btn_back(self):
        self.switch_screen('home_screen')

    def _update_time(self):
        self.CurrentTime = datetime.now().strftime('%Y-%m-%d %I:%M %p')
        self.ids['CurrentTime'].text = self.CurrentTime

    def on_btn_set_time(self):
        dlg = DateTimeDialog()

        now = datetime.now()
        dlg.year = str(now.year)
        dlg.month = str(now.month)
        dlg.date = str(now.day)
        dlg.hour = str(now.strftime("%I"))
        dlg.minute = str(now.minute)
        dlg.ampm = str(now.strftime("%p"))

        dlg.bind(on_ok=self._update_time)
        dlg.open()
