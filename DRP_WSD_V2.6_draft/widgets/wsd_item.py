from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('widgets/kv/wsd_item.kv')


class WSDItem(BoxLayout):
    label = StringProperty()
    value = NumericProperty()
    unit = StringProperty()
    label_width = NumericProperty(1.5)

    def get_value(self):
        return self.value

    def set_value(self, val):
        self.value = val
