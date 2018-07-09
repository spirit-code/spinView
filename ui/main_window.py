
from nanogui import Color, Screen, Window, GroupLayout, BoxLayout, \
    ToolButton, Label, Button, Widget, \
    PopupButton, CheckBox, MessageDialog, VScrollPanel, \
    ImagePanel, ImageView, ComboBox, ProgressBar, Slider, \
    TextBox, ColorWheel, Graph, GridLayout, \
    Alignment, Orientation, TabWidget, TabHeader, IntBox, \
    GLShader, GLCanvas, glfw, entypo

from ui.gl_canvas import GLWidget

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

        self.windowFoo()
        self.windowRenderers()

        # # Tab widget
        # tw = TabWidget(self)
        # tw.setPosition((-20,300))
        # twtest = tw.createTab("tab test")
        # tw.addTab("tab 0",twtest)
        # tw.addTab("tab 2",twtest)
        # tw.setFixedSize((200*self.pixelRatio(),300*self.pixelRatio()))

        self.performLayout()

    def windowFoo(self):
        height = 200
        height_min = 30
        width = 200
        window = Window(self, "alpha")
        window.setFixedSize(
            (width*self.pixelRatio(), height*self.pixelRatio()))
        window.setPosition((5, 30))
        window.setLayout(GroupLayout())

        buttons = window.buttonPanel()

        # Minimize/Maximize
        b_minmax = Button(buttons, "", icon=entypo.ICON_CHEVRON_DOWN)

        def cb():
            if window.height() == height_min:
                window.setHeight(height)
            else:
                window.setHeight(height_min)
            b_minmax.setPushed(not b_minmax.pushed())
        b_minmax.setCallback(cb)

        # Close
        b_close = Button(buttons, "", icon=entypo.ICON_CIRCLE_WITH_CROSS)

        def cb():
            window.dispose()
        b_close.setCallback(cb)

        # Buttons
        Label(window, "Push buttons", "sans-bold")
        b = Button(window, "Plain button")

        def cb():
            print("pushed!")
        b.setCallback(cb)

        b = Button(window, "Styled", entypo.ICON_ROCKET)
        b.setBackgroundColor(Color(0, 0, 1.0, 0.1))
        b.setCallback(cb)

    def windowRenderers(self):
        height = 200
        height_min = 30
        width = 200
        window = Window(self, "Renderers")
        window.setFixedSize(
            (width*self.pixelRatio(), height*self.pixelRatio()))
        window.setPosition((5, 235))
        window.setLayout(GroupLayout())

        def mouseDragEvent(window):
            pass

        popupBtnMiscRenderers = PopupButton(window, "Misc")
        popupBtnMiscRenderers.setFontSize(16)

        popupMiscRenderers = popupBtnMiscRenderers.popup()
        popupMiscRenderers.setLayout(GroupLayout())
        Label(popupMiscRenderers, "Miscaleneous Renderers")
        def cb(state):
            self.gl_canvas.switchArrowsRenderer()
        chb = CheckBox(popupMiscRenderers, "Arrows", cb)
        chb.setChecked(self.gl_canvas.show_arrows)
        def cb(state):
            self.gl_canvas.switchCoordinateSystemRenderer()
        chb = CheckBox(popupMiscRenderers, "Coordinates", cb)
        chb.setChecked(self.gl_canvas.show_coordinate_system)
        def cb(state):
            print("Not implemented!")
        chb = CheckBox(popupMiscRenderers, "ArrowsSphere", cb)
        def cb(state):
            self.gl_canvas.switchBoundingBoxRenderer()
        chb = CheckBox(popupMiscRenderers, "Bounding Box", cb)
        chb.setChecked(self.gl_canvas.show_bounding_box)
        
        popupBtnDotRenderer = PopupButton(window, "Dot")
        popupBtnDotRenderer.setFontSize(16)
        
        popupDotRenderer = popupBtnDotRenderer.popup()
        popupDotRenderer.setLayout(GroupLayout())
        Label(popupDotRenderer, "Dot Renderer Options")
        def cb(state):
            self.gl_canvas.switchDotRenderer(comboDotStyle.selectedIndex())
            self.gl_canvas.setDotRadius(sliderDotRadius.value())
        chb = CheckBox(popupDotRenderer, "Dot", cb)
        def cb(state):
            self.gl_canvas.setDotRadius(sliderDotRadius.value())
        sliderDotRadius = Slider(popupDotRenderer)
        sliderDotRadius.setRange([0,1000])
        sliderDotRadius.setValue(500)
        sliderDotRadius.setFixedWidth(80)
        sliderDotRadius.setCallback(cb)
        Label(popupDotRenderer, "Dot style :", "sans-bold") 
        comboDotStyle = ComboBox(popupDotRenderer, 
            self.gl_canvas.getDotStyles())
        def cb(state):
            self.gl_canvas.setDotStyle( comboDotStyle.selectedIndex()) 
        comboDotStyle.setCallback( cb ) 
        comboDotStyle.setFontSize(16)
        comboDotStyle.setFixedSize((100, 20))
      
        popupBtnNeighborsRenderer = PopupButton(window, "Neighbors")
        popupBtnNeighborsRenderer.setFontSize(16)
        
        popupNeighborsRenderer = popupBtnNeighborsRenderer.popup()
        popupNeighborsRenderer.setLayout(GroupLayout())
        Label(popupNeighborsRenderer, "Neighbors Renderer Options")
        def switch_cb(state):
            self.gl_canvas.switchNeighborRenderer(intBox.value()-1)
        chb = CheckBox(popupNeighborsRenderer, "Neighbors", switch_cb)
        intBox = IntBox(popupNeighborsRenderer)
        intBox.setEditable(True)
        intBox.setFixedSize((150, 20))
        intBox.setUnits("spin index")
        intBox.setValue(1)
        intBox.setDefaultValue("1")
        intBox.setFontSize(16)
        intBox.setFormat("[1-9][0-9]*")
        intBox.setSpinnable(True)
        intBox.setMinValue(1)
        intBox.setValueIncrement(1)
        def update_cb(state):
            self.gl_canvas.drawNeighbors(intBox.value()-1)
        intBox.setCallback(update_cb)
         
        popupBtnCubesRenderer = PopupButton(window, "Cubes")
        popupBtnCubesRenderer.setFontSize(16) 
        
        popupCubesRenderer = popupBtnCubesRenderer.popup()
        popupCubesRenderer.setLayout(GroupLayout())
        Label(popupCubesRenderer, "Cubes Renderer Options")
        def cb(state):
            self.gl_canvas.switchCubesRenderer()
            self.gl_canvas.setCubesSize(sliderCubeSize.value())
        chb = CheckBox(popupCubesRenderer, "Cubes", cb)
        def cb(state):
            self.gl_canvas.setCubesSize(sliderCubeSize.value())
        sliderCubeSize = Slider(popupCubesRenderer)
        sliderCubeSize.setValue(0.5)
        sliderCubeSize.setFixedWidth(80)
        sliderCubeSize.setCallback(cb)

        buttons = window.buttonPanel()

        # Minimize/Maximize
        b_minmax = Button(buttons, "", icon=entypo.ICON_CHEVRON_DOWN)

        def cb():
            if window.height() == height_min:
                window.setHeight(height)
            else:
                window.setHeight(height_min)
            b_minmax.setPushed(not b_minmax.pushed())
        b_minmax.setCallback(cb)

        # Close
        b_close = Button(buttons, "", icon=entypo.ICON_CIRCLE_WITH_CROSS)

        def cb():
            window.dispose()
        b_close.setCallback(cb)

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
        return False

    def resizeEvent(self, size):
        super(MainWindow, self).resizeEvent(size)
        # Make sure that the GLcanvas is resized
        self.gl_canvas.setSize(size[:])
        self.gl_canvas.view.setFramebufferSize(
            size[0]*self.pixelRatio(), size[1]*self.pixelRatio())
        return True

