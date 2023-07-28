# -*- coding: iso8859-15 -*-
from kivy.lang import Builder
from screens.base import BaseScreen


Builder.load_file('screens/error_screen.kv')


class ErrorScreen(BaseScreen):

    def on_enter(self, *args):
        error_msg = self.app.get_exception()
        self.ids.error_msg.text = str(error_msg)
        super(ErrorScreen, self).on_enter(*args)
