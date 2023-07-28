# -*- coding: iso8859-15 -*-
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from widgets.icons import ICONS


Builder.load_file('widgets/kv/label.kv')


class ColoredLabel(Label):
    pass


class H1(ColoredLabel):
    pass


class H2(ColoredLabel):
    pass


class H3(ColoredLabel):
    pass


class H4(ColoredLabel):
    pass


class H5(ColoredLabel):
    pass


class H6(ColoredLabel):
    pass


class H1Sub(ColoredLabel):
    pass


class H2Sub(ColoredLabel):
    pass


class H3Sub(ColoredLabel):
    pass


class P(ColoredLabel):
    pass


class B(ColoredLabel):
    pass


class DRPIconLabel(ColoredLabel):
    icon = StringProperty("")
    font_name = StringProperty("Icon")
    font_size = NumericProperty(40)

    def on_icon(self, *args):
        self.text = ICONS.get(self.icon, "")


class ScrollableLabel(ScrollView):
    text = StringProperty('')
    color = ListProperty([1, 1, 1, 1])
