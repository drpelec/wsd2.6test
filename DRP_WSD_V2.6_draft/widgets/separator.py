from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp


Builder.load_file('widgets/kv/separator.kv')


class Separator(BoxLayout):

    def __init__(self, **kwargs):
        super(Separator, self).__init__(**kwargs)
        self.on_orientation()

    def on_orientation(self, *args):
        self.size_hint = (1, None) if self.orientation == 'horizontal' else (None, 1)
        if self.orientation == 'horizontal':
            self.height = dp(1)
        else:
            self.width = dp(1)
