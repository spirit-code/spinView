from nanogui import Window, Button, GroupLayout, entypo

class FloatingWindow():
    
    def __init__(self, parent_window, position):
        # The parent window is the main window for floating windows 
        self.pw = parent_window

        # Default properties 
        default_height = 250
        default_height_min = 30
        default_width = 200
        
        # Initialize the floating window 
        self.window = Window(self.pw, "alpha")
        self.window.setFixedSize(
            (default_width * self.pw.pixelRatio(),
             default_height * self.pw.pixelRatio()))
        self.window.setPosition(position)
        self.window.setLayout(GroupLayout())

        # Add window control buttons (min/max, close, etc)
        buttons = self.window.buttonPanel()

        # Minimize/Maximize
        b_minmax = Button(buttons, "", icon=entypo.ICON_CHEVRON_DOWN)
        def cb():
            if self.window.height() == default_height_min:
                self.window.setHeight(default_height)
            else:
                self.window.setHeight(default_height_min)
            b_minmax.setPushed(not b_minmax.pushed())
        b_minmax.setCallback(cb)

        # Close
        b_close = Button(buttons, "", icon=entypo.ICON_CIRCLE_WITH_CROSS)
        def cb():
            self.window.dispose()
        b_close.setCallback(cb)

