
from nanogui import Color, Screen, Window, GroupLayout, BoxLayout, \
    ToolButton, Label, Button, Widget, \
    PopupButton, CheckBox, MessageDialog, VScrollPanel, \
    ImagePanel, ImageView, ComboBox, ProgressBar, Slider, \
    TextBox, ColorWheel, Graph, GridLayout, \
    Alignment, Orientation, TabWidget, TabHeader, IntBox, \
    GLShader, GLCanvas, glfw, entypo

from ui.gl_canvas import GLWidget
from ui.floating.foo import FooWindow
from ui.floating.renderers import RenderersWindow


class MainWindow(Screen):
    
    def __init__(self, height, width):
        super(MainWindow, self).__init__((height, width), "SpinView 0.0")

        # GL canvas
        self.gl_canvas = GLWidget(self)

        # Header tabs
        header = TabHeader(self, "sans-bold")
        header.setSize((100, 300))
        header.setPosition((-20, 0))

        # TODO: connect the tabs with CombBoxes(?)
        header.addTab("File")
        header.addTab("Edit")
        header.addTab("Geometry")
        header.addTab("Orientation")

        FooWindow(self)
        RenderersWindow(self)

        # # Tab widget
        # tw = TabWidget(self)
        # tw.setPosition((-20,300))
        # twtest = tw.createTab("tab test")
        # tw.addTab("tab 0",twtest)
        # tw.addTab("tab 2",twtest)
        # tw.setFixedSize((200*self.pixelRatio(),300*self.pixelRatio()))

        self.performLayout()

    def draw(self, ctx):
        super(MainWindow, self).draw(ctx)

    def drawContents(self):
        super(MainWindow, self).drawContents()
        self.gl_canvas.view.draw()

    def keyboardEvent(self, key, scancode, action, modifiers):
        if super(MainWindow, self).keyboardEvent(key, scancode,
                                                 action, modifiers):
            return True
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.setVisible(False)
            return True
        if key == glfw.KEY_C and action == glfw.PRESS:
            print( "Canvas Loaded" )
            return True
        return False

    def resizeEvent(self, size):
        super(MainWindow, self).resizeEvent(size)
        # Make sure that the GLcanvas is resized
        self.gl_canvas.setSize(size[:])
        self.gl_canvas.view.setFramebufferSize(
            size[0]*self.pixelRatio(), size[1]*self.pixelRatio())
        return True

