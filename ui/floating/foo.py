from nanogui import Label, Button, Color, entypo
from . import base

class FooWindow(base.FloatingWindow):
    
    def __init__(self, parent_window):
        position = (5, 35)
        super(FooWindow, self).__init__(parent_window, position)
        # Buttons
        Label(self.window, "Push buttons", "sans-bold")
        b = Button(self.window, "Plain button")
        def cb():
            print("pushed!")
        b.setCallback(cb)
        b = Button(self.window, "Styled", entypo.ICON_ROCKET)
        b.setBackgroundColor(Color(0, 0, 1.0, 0.1))
        b.setCallback(cb)
