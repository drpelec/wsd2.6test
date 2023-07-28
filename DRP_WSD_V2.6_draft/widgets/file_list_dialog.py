from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.modalview import ModalView
from widgets.dialog import DRPModalView
from datetime import datetime
from utils.common import set_system_time
from kivy.uix.button import Button

Builder.load_file('widgets/kv/file_list_dialog.kv')


class FileListDialog(DRPModalView):

    comparison = StringProperty("")

    def __init__(self, file_list, comparison, **kwargs):
        self.register_event_type('on_confirm')
        super(FileListDialog, self).__init__(**kwargs)

        self.comparison = comparison
        self.add_file_buttons(file_list)
        self.title = "Choose a saved file"

    def add_file_buttons(self, file_list):
        self.ids.file_list.height = len(file_list)*62
        for filename in file_list:
            button = Button(text=filename, height=60, padding=[10, 10])
            button.bind(on_press=self._choose_file)
            self.ids.file_list.add_widget(button)

    def _choose_file(self, button):
        self.dismiss()
        self.dispatch('on_confirm', button.text, self.comparison)

    def on_confirm(self, filename, comparison):
        pass


class WorksheetListDialog(FileListDialog):

    temp_file = StringProperty("")
    comparison = StringProperty("")

    def __init__(self, temp_file, comparison, worksheet_list, **kwargs):
        super(WorksheetListDialog, self).__init__(worksheet_list, comparison, **kwargs)
        self.temp_file = temp_file
        self.comparison = comparison
        self.title = "Choose a data set from the file"

    def _choose_file(self, button):
        self.dismiss()
        self.dispatch('on_confirm', self.temp_file, button.text, self.comparison)

    def on_confirm(self, filename, worksheet, comparison):
        pass

