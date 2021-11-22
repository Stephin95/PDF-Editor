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
from pathlib import Path
# from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

# from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from pdf_E import PdfEditor
from kivy.clock import Clock

class Screen_manager(ScreenManager):
    pass


class Main_window(Screen):
    pass


class Secondary_window(Screen):
    # loadfile = ObjectProperty(None)
    # savefile = ObjectProperty(None)
    # text_input = ObjectProperty(None)
    heading_label = ObjectProperty()
    description_label = ObjectProperty()
    selection_label = ObjectProperty()
    print(heading_label)
    print(description_label)
    print(selection_label)

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

    def load(self, path, filename,auto_close=False):
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
        if auto_close:
            self.dismiss_popup()

        
        # with open(os.path.join(path, filename[0])) as stream:
        #     self.text_input.text = stream.read()

        

    def save(self, path):
        
        # path=Path(path)
        print(path)
        self.final(path)
    def final(self):
        pass

        

    def show_completed(self):
        content= CompletedDialog(cancel=self.dismiss_popup)
        self._popup = Popup(title="Completed", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

class CompletedDialog(FloatLayout):
    cancel = ObjectProperty(None)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    # text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ErrorDialog(FloatLayout):
    cancel = ObjectProperty(None)

class Imagetopdf_screen(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.initiation)
        
    def initiation(self,nw):
        self.heading_label.text='Convert Image to Pdf'
        self.description_label.text='Please select the images that need to be combined and converted to pdf'

    def final(self,path):
        path_list=self.selection_label.text.split('\n')
        print(path_list)
        path_lib_path= list(map(Path,path_list))
        print('splitted path', )
        p= PdfEditor(path_list=path_lib_path)
        p.imgtopdf(savepath=path)
        self.dismiss_popup()
        self.show_completed()

class MergePDF_screen(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.initiation)
        
    def initiation(self,nw):
        self.heading_label.text='Merge Pdfs'
        self.description_label.text='Please select the files that need to be merged'

    def final(self,path):
        path_list=self.selection_label.text.split('\n')
        print(path_list)
        path_lib_path= list(map(Path,path_list))
        print('splitted path', )
        p= PdfEditor(path_list=path_lib_path)
        p.pdf_merge(savepath=path)
        self.dismiss_popup()
        self.show_completed()

    

   


class PDFApp(App):
    def build(self):
        return Screen_manager()


if __name__ == "__main__":
    PDFApp().run()
