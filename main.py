"""
Application built from a  .kv file
==================================

This shows how to implicitly use a .kv file for your application. You
should see a full screen button labelled "Hello from test.kv".

After Kivy instantiates a subclass of App, it implicitly searches for a .kv
file. The file test.kv is selected because the name of the subclass of App is
TestApp, which implies that kivy should try to load "test.kv". That file
contains a root Widget.
"""

# import kivy
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

# from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


class Screen_manager(ScreenManager):
    pass


class Main_window(Screen):
    pass


class Secondary_window(Screen):
    # loadfile = ObjectProperty(None)
    # savefile = ObjectProperty(None)
    # text_input = ObjectProperty(None)
    description_label = ObjectProperty()
    selection_label = ObjectProperty()
    def show_error(self,errormsg="Error occured"):
        content= ErrorDialog(cancel=self.dismiss_popup)
        self._popup = Popup(title="Error", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        if not filename:
            print('please select a valid file')
            self.show_error(errormsg='file not found')
            return 0
        file_path = os.path.join(path, filename[0])
        print(file_path)
        if self.selection_label.text == 'No files loaded':
            self.selection_label.text=file_path
        else:
            self.selection_label.text=self.selection_label.text+'\n'+file_path

        
        # with open(os.path.join(path, filename[0])) as stream:
        #     self.text_input.text = stream.read()

        self.dismiss_popup()

    def save(self, path):
        print(path)
        # print(os.path.join(path, filename))
        # with open(os.path.join(path, filename), "w") as stream:
            # stream.write(
            #     self.text_input.text
            # )  # considering output file as text for now.

        self.dismiss_popup()

    pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    # text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ErrorDialog(FloatLayout):
    cancel = ObjectProperty(None)


class PDFApp(App):
    def build(self):
        return Screen_manager()


if __name__ == "__main__":
    PDFApp().run()
