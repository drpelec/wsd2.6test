"""
    Pre-configuration file to be used to setup Kivy configurations.
    This module must be called before executing a Kivy GUI app!
"""
import os
from kivy.clock import Clock
from kivy.config import Config
from utils.common import get_screen_resolution
from kivy.core.text import LabelBase


Config.read(os.path.expanduser('~/.kivy/config.ini'))

Config.set('kivy', 'log_dir', '/tmp')

w, h = get_screen_resolution()
Config.set('graphics', 'width', str(w))
Config.set('graphics', 'height', str(h))

Config.set('kivy', 'keyboard_mode', 'systemanddock')
Config.set('kivy', 'keyboard_layout', 'en_US')
Config.set('kivy', 'log_level', 'info')
Config.set('input', 'hid_%(name)s', 'probesysfs,provider=hidinput,select_all=1,param=rotation=90,param=min_abs_x=106,param=max_abs_x=3863,param=min_abs_y=107,param=max_abs_y=4045')
Config.remove_option('input', '%(name)s')

Clock.max_iteration = 20

LabelBase.register(name="Icon", fn_regular="assets/fonts/materialdesignicons-webfont.ttf")
