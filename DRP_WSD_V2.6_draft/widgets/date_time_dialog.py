from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.modalview import ModalView
from widgets.dialog import DRPModalView
from datetime import datetime
from utils.common import set_system_time

Builder.load_file('widgets/kv/date_time_dialog.kv')

class DateTimeDialog(DRPModalView):
    year = StringProperty('2019')
    month = StringProperty('01')
    date = StringProperty('01')
    hour = StringProperty('12')
    minute = StringProperty('00')
    ampm = StringProperty('AM')

    has_error = BooleanProperty(False)
    dt = None

    def on_open(self):
        super(DateTimeDialog, self).on_open()
        self.ids.txt_year.focus = True
        self.ids.txt_year.bind(text=self._on_text_change)
        self.ids.txt_month.bind(text=self._on_text_change)
        self.ids.txt_date.bind(text=self._on_text_change)
        self.ids.txt_hour.bind(text=self._on_text_change)
        self.ids.txt_minute.bind(text=self._on_text_change)

    def on_ok(self, *args):
        try:
            self.dt = datetime.strptime("{}-{}-{} {}:{} {}".format(self.year, self.month, self.date, self.hour, self.minute, self.ampm), "%Y-%m-%d %I:%M %p")
        except:
            self.dt = None

        if self.dt is None:
            self.has_error = True
        else:
            self.clear_error()
            self.on_valid()

    def clear_error(self):
        self.has_error = False

    def _on_text_change(self, instance, value):
        self.clear_error()

    def on_valid(self):
        set_system_time(self.dt)
        self.dismiss()


