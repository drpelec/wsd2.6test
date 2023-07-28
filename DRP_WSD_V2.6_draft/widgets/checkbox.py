from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('widgets/kv/checkbox.kv')


class LabeledOption(BoxLayout):

    text = StringProperty()
    font_size = NumericProperty(14)
    active = BooleanProperty(False)
    group = StringProperty()
    allow_no_selection = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(LabeledOption, self).__init__(**kwargs)
        self.register_event_type('on_pressed')
        Clock.schedule_once(lambda dt: self._bind_active())

    def _bind_active(self):
        self.ids.checkbox.bind(active=self._on_chk_active)

    def on_touch_down(self, touch):
        if self.ids.label.collide_point(*touch.pos):
            self.ids.checkbox._do_press()
        self.active = self.ids.checkbox.active
        super(LabeledOption, self).on_touch_down(touch)

    def _on_chk_active(self, *args):
        self.active = self.ids.checkbox.active
        self.dispatch('on_pressed')

    def on_pressed(self):
        pass
