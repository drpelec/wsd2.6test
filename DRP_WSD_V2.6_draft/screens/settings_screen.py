from kivy.lang import Builder
from screens.base import BaseScreen
from utils.common import get_config, update_config_file


Builder.load_file('screens/settings_screen.kv')


class SettingsScreen(BaseScreen):

    def on_enter(self, *args):
        """
        Don't update values as we don't need here!
        :param args:
        :return:
        """
        super(BaseScreen, self).on_enter(*args)
        self.ids.chk_wireless.active = get_config()['mode'] == 'wifi'
        self.ids.chk_wired.active = get_config()['mode'] != 'wifi'
        self.ids.chk_chart.active = get_config().get('chart', True)

    def on_checkbox_pressed(self, chk_widget):
        if chk_widget.active:
            conn = 'wifi' if chk_widget.text == 'Wireless' else 'wired'
            self.app.set_connection_type(conn)

    def on_chk_chart(self):
        conf = get_config()
        conf['chart'] = self.ids.chk_chart.active
        update_config_file(conf)

    def on_btn_back(self):
        #clear screen cache (to re-create chart button if it was deleted previously)
        self.manager.clear_widgets()
        self.switch_screen('calibration_screen')
