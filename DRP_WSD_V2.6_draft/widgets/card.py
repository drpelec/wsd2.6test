from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty, AliasProperty, VariableListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex


Builder.load_file('widgets/kv/card.kv')


class BorderLessCard(BoxLayout):
    border_radius = NumericProperty(0)
    background_color = ListProperty([0.93, 0.94, 0.95, 1])
    orientation = StringProperty('vertical')

    def __init__(self, **kwargs):
        self.register_event_type('on_press')
        super(BorderLessCard, self).__init__(**kwargs)

    def _get_diameter(self):
        return self.border_radius * 2

    _diameter = AliasProperty(_get_diameter, None, bind=('border_radius',))

    def on_touch_down(self, touch):
        super(BorderLessCard, self).on_touch_down(touch)
        if self.collide_point(*touch.pos):
            self.dispatch('on_press')

    def on_press(self):
        pass


class BorderedCard(ButtonBehavior, BoxLayout):
    border_radius = NumericProperty(0)
    background_color = ListProperty(get_color_from_hex('#F2F2F2'))
    outline_color = ListProperty(get_color_from_hex('#C5C9CC'))
    orientation = StringProperty('vertical')

    def _get_diameter(self):
        return self.border_radius * 2

    _diameter = AliasProperty(_get_diameter, None, bind=('border_radius',))


class Card(BoxLayout):
    padding = VariableListProperty([5, 5, 5, 5])
