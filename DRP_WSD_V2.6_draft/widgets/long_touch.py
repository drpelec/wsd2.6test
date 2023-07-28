from kivy.clock import Clock
from kivy.properties import ObjectProperty


class LongTouchBehavior(object):

    _event_long_touch = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(LongTouchBehavior, self).__init__(**kwargs)
        self.register_event_type('on_long_press')

    def on_touch_down(self, touch):
        super(LongTouchBehavior, self).on_touch_down(touch)
        if self.collide_point(*touch.pos) and self._event_long_touch is None:
            self._event_long_touch = Clock.schedule_once(lambda dt: self._on_long_press(), 1)

    def on_touch_move(self, touch):
        super(LongTouchBehavior, self).on_touch_move(touch)
        if not self.collide_point(*touch.pos):
            self._cancel_schedule()

    def on_touch_up(self, touch):
        super(LongTouchBehavior, self).on_touch_up(touch)
        self._cancel_schedule()

    def _cancel_schedule(self):
        if self._event_long_touch:
            self._event_long_touch.cancel()
        self._event_long_touch = None

    def _on_long_press(self):
        self._event_long_touch = None
        self.dispatch('on_long_press')

    def on_long_press(self):
        pass


if __name__ == '__main__':

    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.uix.floatlayout import FloatLayout

    class ButtonWithLongTouch(LongTouchBehavior, Button):
        pass

    class LongTouchApp(App):

        def build(self):
            box = FloatLayout()
            btn = ButtonWithLongTouch(size_hint=(.3, .3))
            btn.bind(on_long_press=self.on_long_touch)
            box.add_widget(btn)
            return box

        @staticmethod
        def on_long_touch(*args):
            print('Long touch!')

    LongTouchApp().run()
