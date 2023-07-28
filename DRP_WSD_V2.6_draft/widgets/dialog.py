from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.modalview import ModalView
from hashlib import sha256


Builder.load_file('widgets/kv/dialog.kv')


class DRPModalView(ModalView):
    pass


class PasswordDialog(DRPModalView):
    pwd = StringProperty('')
    is_error = BooleanProperty(False)

    def __init__(self, **kwargs):
        self.register_event_type('on_success')
        super(PasswordDialog, self).__init__(**kwargs)

    def on_open(self):
        self.clear_error()
        self.ids.txt_pwd.text = ''
        self.ids.txt_pwd.focus = True
        self.ids.txt_pwd.bind(text=self._on_text_change)

    def on_success(self, *args):
        pass

    def on_ok(self):
        if sha256(self.ids.txt_pwd.text).hexdigest() == self.pwd:
            self.dismiss()
            self.dispatch('on_success')
        elif self.ids.txt_pwd.text == self.pwd:
            self.dismiss()
            self.dispatch('on_success')
        else:
            self.is_error = True

    def _on_text_change(self, instance, value):
        self.clear_error()

    def clear_error(self):
        self.is_error = False


class LoadingDialog(DRPModalView):
    pass


class YesNoDialog(DRPModalView):

    message = StringProperty('')

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super(YesNoDialog, self).__init__(**kwargs)

    def on_yes(self):
        self.dispatch('on_confirm')

    def on_confirm(self):
        pass


class InputDialog(DRPModalView):

    text = StringProperty('')
    hint_text = StringProperty('')
    input_filter = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.register_event_type('on_confirm')
        super(InputDialog, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.enable_focus(), .3)

    def on_yes(self):
        new_val = self.ids.input.text
        self.dismiss()
        self.dispatch('on_confirm', new_val)

    def on_confirm(self, *args):
        pass

    def enable_focus(self):
        self.ids.input.focus = True
        self.ids.input.bind(text=self.on_text_input)

    def on_text_input(self, *args):
        self.ids.btn.disabled = False if args[1] else True
