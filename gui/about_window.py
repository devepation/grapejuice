import variables
from gui.window_base import WindowBase


class AboutWindow(WindowBase):
    def __init__(self):
        super().__init__(variables.grapejuice_main_glade())

    def window(self):
        return self.builder.get_object("grapejuice_about")

    def run(self):
        w = self.window()
        w.run()
        w.hide()
