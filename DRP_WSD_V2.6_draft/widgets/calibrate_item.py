from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from widgets.card import Card
from widgets.icons import ICONS


Builder.load_file('widgets/kv/calibrate_item.kv')


arrows = {
    'LF': 'arrow-top-left',
    'RF': 'arrow-top-right',
    'LR': 'arrow-bottom-left',
    'RR': 'arrow-bottom-right'
}

titles = {
    'LF': 'LEFT FRONT',
    'RF': 'RIGHT FRONT',
    'LR': 'LEFT REAR',
    'RR': 'RIGHT REAR'
}


class WSDCalibrateItem(Card):
    direction = StringProperty('LR')

    def __init__(self, **kwargs):
        super(WSDCalibrateItem, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.__init())
        self.register_event_type('on_calibrate')
        self.register_event_type('on_zero')

    def __init(self):
        self.ids.icon.icon = ICONS[arrows[self.direction]]
        self.ids.title.text = titles[self.direction]

    def on_btn_zero(self, _type):
        self.dispatch('on_zero', _type)

    def on_btn_calibrate(self, _type):
        self.dispatch('on_calibrate', _type)

    def on_calibrate(self, *args):
        pass

    def on_zero(self, *args):
        pass
