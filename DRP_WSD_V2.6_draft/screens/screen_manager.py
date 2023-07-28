# -*- coding: iso8859-15 -*-
from kivy.uix.screenmanager import ScreenManager
from screens.chart_screen import ChartScreen
from screens.error_screen import ErrorScreen
from screens.home_screen import HomeScreen
from screens.weight_screen import WeightScreen
from screens.calibration_screen import CalibrationScreen
from screens.mass_center_screen import CenterOfMassScreen
from screens.settings_screen import SettingsScreen


screens = {
    'home_screen': HomeScreen,
    'weight_screen': WeightScreen,
    'calibration_screen': CalibrationScreen,
    'chart_screen': ChartScreen,
    'center_of_mass_screen': CenterOfMassScreen,
    'error_screen': ErrorScreen,
    'settings_screen': SettingsScreen,
}


sm = ScreenManager()
