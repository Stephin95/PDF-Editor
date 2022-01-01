# import kivy
import os
from kivy.app import App
from pathlib import Path

# from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from pdf_E import PdfEditor
from kivy.clock import Clock
from kivy.utils import platform
# from kivy.lang import Builder

python_script_path = Path(__file__).parents[0]

python_script_path=Path(python_script_path, "pdf.kv")

# Builder.load_file(str(python_script_path))

if platform == "android":
    from android.permissions import request_permissions, Permission

    # request_permissions(
    #     [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE,Permission.MANAGE_EXTERNAL_STORAGE]
    # )
    request_permissions(["android.permission.MANAGE_EXTERNAL_STORAGE"])

else:
	pass


# Builder.load_file("C:\\Users\\steph\\Home\\Python\\Pdf_editor\\pdf.kv")
class Screen_manager(ScreenManager):
    pass


class Main_window(Screen):
    pass


class Secondary_window(Screen):
    headgrid = ObjectProperty()
    innerBOX = ObjectProperty()
    heading_label = ObjectProperty()
    description_label = ObjectProperty()
    selection_label = ObjectProperty()
    # print(heading_label)
    # print(description_label)
    # print(selection_label)

    def show_error(self, errormsg="Error occured"):
        content = ErrorDialog(cancel=self.dismiss_popup)
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

    def load(self, path, filename, auto_close=False):
        if not filename:
            print("please select a valid file")
            self.show_error(errormsg="file not found")
            return 0
        file_path = os.path.join(path, filename[0])
        print(file_path)
        if self.selection_label.text == "No files loaded":
            self.selection_label.text = file_path
        else:
            self.selection_label.text = self.selection_label.text + "\n" + file_path
        if auto_close:
            self.dismiss_popup()

    def save(self, path):
        # path=Path(path)
        print("Folder selected for saving is ", path)
        self.final(path)

    def final(self):
        pass

    def show_completed(self):
        content = CompletedDialog(cancel=self.dismiss_popup)
        self._popup = Popup(title="Completed", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


class CompletedDialog(FloatLayout):
    cancel = ObjectProperty(None)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ErrorDialog(FloatLayout):
    cancel = ObjectProperty(None)


class Imagetopdf_screen(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.initiation)

    def initiation(self, nw):
        self.heading_label.text = "Convert Image to Pdf"
        self.description_label.text = (
            "Please select the images that need to be combined and converted to pdf"
        )

    def final(self, path):
        path_list = self.selection_label.text.split("\n")
        print(path_list)
        path_lib_path = list(map(Path, path_list))
        print("splitted path",)
        p = PdfEditor(path_list=path_lib_path)
        p.imgtopdf(savepath=path)
        self.dismiss_popup()
        self.show_completed()

class Searchable_pdf_screen(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.initiation)

    def initiation(self, nw):
        self.heading_label.text = "Searchable Pdf"
        self.description_label.text = "Please select the files that need to be made searchable"

    def final(self, path):
        path_list = self.selection_label.text.split("\n")
        print(path_list)
        path_lib_path = list(map(Path, path_list))
        print("splitted path",)
        p = PdfEditor(path_list=path_lib_path)
        p.pdf_merge(savepath=path)
        self.dismiss_popup()
        self.show_completed()

class Ext_text(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.initiation)

    def initiation(self, nw):
        self.heading_label.text = "Extract text from Pdfs"
        self.description_label.text = "Please select the file to extract text"

    def final(self, path):
        path_list = self.selection_label.text.split("\n")
        print(path_list)
        path_lib_path = list(map(Path, path_list))
        print("splitted path",)
        p = PdfEditor(path_list=path_lib_path)
        p.extract_text(savepath=path)
        self.dismiss_popup()
        self.show_completed()

class MergePDF_screen(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.initiation)

    def initiation(self, nw):
        self.heading_label.text = "Merge Pdfs"
        self.description_label.text = "Please select the files that need to be merged"

    def final(self, path):
        path_list = self.selection_label.text.split("\n")
        print(path_list)
        path_lib_path = list(map(Path, path_list))
        print("splitted path",)
        p = PdfEditor(path_list=path_lib_path)
        p.pdf_merge(savepath=path)
        self.dismiss_popup()
        self.show_completed()


class Extract_page_screen(Secondary_window):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.input1 = ObjectProperty()
        Clock.schedule_once(self.initiation)
        self.my_list = ""

    def initiation(self, nw):
        self.heading_label.text = "Extract pages from pdf"
        self.description_label.text = "Please select the pdfs"
        self.range_input = False
        label_pg_start = Label(
            text="Enter the page no.s to extract seperated by commas below for range extract enter the first page only"
        )
        label_pg_start.text_size = label_pg_start.size
        self.headgrid.add_widget(label_pg_start)
        label_pg_end = Label(
            text="for a range extract enter the final page no. Leave blank if you are not doing a range extract"
        )
        label_pg_end.text_size = label_pg_end.size
        self.headgrid.add_widget(label_pg_end)
        self.start_page = TextInput(hint_text="start", multiline=False)
        self.start_page.bind(text=self.check_button)
        final_page = TextInput(hint_text="end", multiline=False)
        final_page.bind(text=self.check_button)
        self.headgrid.add_widget(self.start_page)
        self.headgrid.add_widget(final_page)
        self.ids.save_but.disabled = True

    def check_button(self, *args):
        if args[0] == self.start_page:
            self.first_page = args[1]
            self.ids.save_but.disabled = False
        else:
            self.final_page = args[1]

    def final(self, path):
        print("started final class")
        if self.first_page:
            try:
                if self.final_page:
                    self.my_list = [int(self.first_page) - 1, int(self.final_page) - 1]
                    print(self.my_list)
                    print(type(self.my_list[0]))
                    self.range_input = True
            except Exception as e:
                print(e)
                print(
                    "Doing single page extract - if it is an error please check the try and catch statement"
                )
                page_list = self.first_page.split(",")
                print(page_list)
                # self.my_list = list(map(int, page_list))
                self.my_list = [int(el) - 1 for el in page_list]
                print(type(self.my_list))
                self.range_input = False

        else:
            print("Please enter the start page no. to extract")

        print("starting page extraction")
        print(self.my_list)
        print(self.range_input)
        path_list = self.selection_label.text.split("\n")
        print(path_list)
        path_lib_path = list(map(Path, path_list))
        print("splitted path",)
        p = PdfEditor(path_list=path_lib_path)
        p.extract_page(page_nos=self.my_list, range=self.range_input, savepath=path)
        self.dismiss_popup()
        self.show_completed()


class PDFApp(App):
    file_path = StringProperty("")
    if platform == "android":
        from android.storage import primary_external_storage_path

        primary_ext_storage = primary_external_storage_path()
        file_path = primary_ext_storage
    elif platform == "linux":
        file_path = str(Path.home())
        print("File explorer file path=", file_path)
    elif platform == "win":
        # file_path = Path.home().joinpath("temp_pdf_editor")
        # file_path.mkdir(exist_ok=True)
        file_path=Path.home()
        file_path = str(file_path)
        # file_path = str(Path.home())

        print("File explorer file path=", file_path)

    def build(self):
        print(self.file_path, "This is the current path")
        return Screen_manager()

if __name__ == "__main__":
    PDFApp().run()

