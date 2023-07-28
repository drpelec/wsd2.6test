from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import Screen


Builder.load_file('screens/base.kv')


class BaseScreen(Screen):
    app = ObjectProperty()
    show_back_button = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self.app = App.get_running_app()

    def on_enter(self, *args):
        super(BaseScreen, self).on_enter(*args)
        self.update_screen()

    def switch_screen(self, screen_name):
        self.app.switch_screen(screen_name=screen_name)

    def on_btn_back(self):
        if self.show_back_button:
            self.switch_screen('home_screen')

    def update_screen(self):
        state = self.app.state
        for dev in state.keys():
            for _type in state[dev].keys():
                _key = '{}_{}'.format(dev, _type)
                if _key in self.ids:
                    self.ids[_key].set_value(state[dev][_type])

    def on_logo_long_pressed(self):
        pass
