# -*- coding: iso8859-15 -*-
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.spinner import Spinner
from widgets.button import DRPButton


Builder.load_file('widgets/kv/spinner.kv')


class DRPSpinnerOption(DRPButton):
    pass


class DRPSpinner(DRPButton, Spinner):
    option_cls = ObjectProperty(DRPSpinnerOption)

    def __init__(self, **kwargs):
        super(DRPSpinner, self).__init__(**kwargs)
        self.register_event_type('on_changed')

    def _on_dropdown_select(self, *args):
        super(DRPSpinner, self)._on_dropdown_select(*args)
        self.dispatch('on_changed')

    def get_value(self):
        return self.text

    def set_value(self, val):
        self.text = val

    def on_changed(self):
        pass
