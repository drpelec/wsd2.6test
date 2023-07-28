from assets.styles import defaultstyle
from assets.styles.defaultstyle import COLOR_1, BUTTONN_PRESSED_COLOR
from kivy.properties import OptionProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from widgets.label import DRPIconLabel
from widgets.long_touch import LongTouchBehavior


class DRPButton(LongTouchBehavior, Button):
    button_type = OptionProperty('blue', options=['blue', 'white'])
    font_size = NumericProperty(17)

    def __init__(self, **kwargs):
        super(DRPButton, self).__init__(**kwargs)
        self.set_default_color()

    def set_white_color(self):
        self.color = defaultstyle.COLOR_1
        self.background_normal = 'assets/images/buttons/white_button.png'
        self.background_down = 'assets/images/buttons/white_button_pressed.png'

    def set_default_color(self):
        self.color = (1, 1, 1, 1)
        self.background_normal = 'assets/images/buttons/blue_button.png'
        self.background_down = 'assets/images/buttons/blue_button_pressed.png'

    def on_button_type(self, obj, val):
        if val == 'blue':
            obj.set_default_color()
        else:
            self.set_white_color()


class ImageButton(LongTouchBehavior, ButtonBehavior, Image):
    pass


class IconButton(ButtonBehavior, DRPIconLabel):

    def _do_press(self):
        self.color = BUTTONN_PRESSED_COLOR
        super(IconButton, self)._do_press()

    def _do_release(self, *args):
        self.color = COLOR_1
        super(IconButton, self)._do_release()
