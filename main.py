'''
Application built from a  .kv file
==================================

This shows how to implicitly use a .kv file for your application. You
should see a full screen button labelled "Hello from test.kv".

After Kivy instantiates a subclass of App, it implicitly searches for a .kv
file. The file test.kv is selected because the name of the subclass of App is
TestApp, which implies that kivy should try to load "test.kv". That file
contains a root Widget.
'''

import kivy

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager,Screen


class Screen_manager(ScreenManager):
    pass
class Main_window(Screen):
    pass
class Secondary_window(Screen):
    pass


class PDFApp(App):
    def build(self):
        return Screen_manager()


if __name__ == '__main__':
    PDFApp().run()