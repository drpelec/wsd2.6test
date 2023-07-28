# -*- coding: utf-8 -*-
"""
Snackbar
========

`Material Design spec page <https://material.io/guidelines/components/snackbars-toasts.html>`_

API
---
"""

from collections import deque
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout


Builder.load_string('''
#:import Window kivy.core.window.Window
#:import get_color_from_hex kivy.utils.get_color_from_hex
<_SnackbarWidget>
    canvas:
        Color:
            rgb: root.background_color
        Rectangle:
            size: self.size
    size_hint_y: None
    size_hint_x: None
    height: dp(48) if _label.texture_size[1] < dp(30) else dp(80)
    width: dp(24) + _label.width + _spacer.width + root.padding_right
    top: 0
    x: Window.width/2 - self.width/2
    BoxLayout:
        width: _label.texture_size[0] if (dp(568) - root.padding_right - \
            _spacer.width - _label.texture_size[0] - dp(24)) >= 0 else (dp(568) - root.padding_right - \
            _spacer.width - dp(24))
        size_hint_x: None
        x: dp(24)
        Label:
            id: _label
            text: root.text
            color: get_color_from_hex('ffffff')
            size: self.texture_size
            font_size: 13
    BoxLayout:
        id: _spacer
        size_hint_x: None
        x: _label.right
        width: 0
''')


class SnackbarManager:

    playing = False
    queue = deque()
    background_color = ListProperty([.3, .3, .3, 1])

    def __init__(self):
        pass

    def _play_next(self, dying_widget=None):
        if (dying_widget or not self.playing) and len(self.queue) > 0:
            self.playing = True
            self.queue.popleft().begin()
        elif len(self.queue) == 0:
            self.playing = False

    def make(self, text, duration=3, background_color=(.3, .3, .3, 1)):
        self.queue.append(_SnackbarWidget(text=text, duration=duration, background_color=background_color))
        self._play_next()


class Snackbar(EventDispatcher):
    text = StringProperty("")
    '''The text that will appear in the Snackbar.

    :attr:`text` is a :class:`~kivy.properties.StringProperty` and defaults to ''.
    '''
    duration = NumericProperty(2)
    '''The amount of time that the Snackbar will stay on screen for.

    :attr:`duration` is a :class:`~kivy.properties.NumericProperty` and defaults to 2.
    '''
    background_color = ListProperty([.3, .3, .3, 1])
    '''Background color of Snackbar

    :attr:`background_color` is a :class:`~kivy.properties.ListProperty` and defaults to [.3, .3, .3, 1].
    '''

    def __init__(self, text, duration=None, background_color=[.3, .3, .3, 1], *args, **kwargs):
        super(Snackbar, self).__init__(*args, **kwargs)
        self.text = text
        self.duration = duration or self.duration
        self.background_color = background_color

    def show(self):
        manager.make(text=self.text, duration=self.duration, background_color=self.background_color)


class _SnackbarWidget(RelativeLayout):
    text = StringProperty()
    duration = NumericProperty()
    padding_right = NumericProperty(dp(24))
    background_color = ListProperty([.3, .3, .3, 1])

    def __init__(self, text, duration, **kwargs):
        super(_SnackbarWidget, self).__init__(**kwargs)
        self.text = text
        self.duration = duration
        self.ids['_label'].text_size = (None, None)

    def begin(self):
        Window.add_widget(self)
        anim = Animation(y=0, duration=.3, t='out_quad')
        anim.start(self)
        Clock.schedule_once(lambda dt: self.die(), self.duration)

    def die(self):
        anim = Animation(top=0, duration=.3, t='out_quad')
        anim.bind(on_complete=lambda *args: manager._play_next(self))
        anim.bind(on_complete=lambda *args: Window.remove_widget(self))
        anim.start(self)


manager = SnackbarManager()
