
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

    def streamtubeRendererWindow(self):
        """ Popup window for Streamtube Renderer control and options"""

        popupBtnStreamTubeRenderer = PopupButton(self.window, "Stream tube")
        popupBtnStreamTubeRenderer.setFontSize(16)

        def streamtubeOptionsUpdate():
            self.gl_canvas.setStreamtubeRadius(sliderStreamtubeRadius.value())
            self.gl_canvas.setStreamtubeResolution(intBoxStreamtubeLoD.value())
            self.gl_canvas.setStreamtubeSmoothing(intBoxStreamtubeSmoothing.value())
            self.gl_canvas.setStreamtubeStep(intBoxStreamtubeStep.value())

        popupStreamTubeRenderer = popupBtnStreamTubeRenderer.popup()
        popupStreamTubeRenderer.setLayout(GroupLayout())
        Label(popupStreamTubeRenderer, "Stream Tube Renderer Options", "sans-bold")
        def cb(state):
            self.gl_canvas.setStreamTubeBaseStyle(comboStreamTubeBaseStyle.selectedIndex()) 
            self.gl_canvas.switchStreamtubeRenderer()
            streamtubeOptionsUpdate()
        cb = CheckBox(popupStreamTubeRenderer, "Stream Tube", cb)
        
        Label(popupStreamTubeRenderer, "Stream base style :") 
        comboStreamTubeBaseStyle = ComboBox(popupStreamTubeRenderer, 
            self.gl_canvas.getStreamTubeBaseStyles())
        def cb(state):
            self.gl_canvas.setStreamTubeBaseStyle(comboStreamTubeBaseStyle.selectedIndex()) 
            streamtubeOptionsUpdate()
        comboStreamTubeBaseStyle.setCallback( cb ) 
        comboStreamTubeBaseStyle.setFontSize(16)
        comboStreamTubeBaseStyle.setFixedSize((100, 20))
        
        Label(popupStreamTubeRenderer, "Streamtube radius :") 
        def cb(state):
            self.gl_canvas.setStreamtubeRadius(sliderStreamtubeRadius.value())
        sliderStreamtubeRadius = Slider(popupStreamTubeRenderer)
        sliderStreamtubeRadius.setRange((0, 0.25))
        sliderStreamtubeRadius.setValue(0.125)
        sliderStreamtubeRadius.setFixedWidth(120)
        sliderStreamtubeRadius.setCallback(cb)
        
        Label(popupStreamTubeRenderer, "Streamtube level of detail :") 
        intBoxStreamtubeLoD = IntBox(popupStreamTubeRenderer)
        intBoxStreamtubeLoD.setEditable(True)
        intBoxStreamtubeLoD.setFixedSize((150, 20))
        intBoxStreamtubeLoD.setUnits("absolute")
        intBoxStreamtubeLoD.setValue(20)
        intBoxStreamtubeLoD.setDefaultValue("1")
        intBoxStreamtubeLoD.setFontSize(16)
        intBoxStreamtubeLoD.setFormat("[3-9]|1[0-9]|20")
        intBoxStreamtubeLoD.setSpinnable(True)
        intBoxStreamtubeLoD.setMinValue(3)
        intBoxStreamtubeLoD.setMaxValue(20)
        intBoxStreamtubeLoD.setValueIncrement(1)
        def update_cb(state):
            self.gl_canvas.setStreamtubeResolution(intBoxStreamtubeLoD.value())
        intBoxStreamtubeLoD.setCallback(update_cb)
        
        Label(popupStreamTubeRenderer, "Streamtube smoothing :") 
        intBoxStreamtubeSmoothing = IntBox(popupStreamTubeRenderer)
        intBoxStreamtubeSmoothing.setEditable(True)
        intBoxStreamtubeSmoothing.setFixedSize((150, 20))
        intBoxStreamtubeSmoothing.setUnits("steps")
        intBoxStreamtubeSmoothing.setValue(3)
        intBoxStreamtubeSmoothing.setDefaultValue("1")
        intBoxStreamtubeSmoothing.setFontSize(16)
        intBoxStreamtubeSmoothing.setFormat("[0-9]")
        intBoxStreamtubeSmoothing.setSpinnable(True)
        intBoxStreamtubeSmoothing.setMinValue(0)
        intBoxStreamtubeSmoothing.setMaxValue(9)
        intBoxStreamtubeSmoothing.setValueIncrement(1)
        def update_cb(state):
            self.gl_canvas.setStreamtubeSmoothing(intBoxStreamtubeSmoothing.value())
        intBoxStreamtubeSmoothing.setCallback(update_cb)
        
        Label(popupStreamTubeRenderer, "Streamtube step :") 
        intBoxStreamtubeStep = IntBox(popupStreamTubeRenderer)
        intBoxStreamtubeStep.setEditable(True)
        intBoxStreamtubeStep.setFixedSize((150, 20))
        intBoxStreamtubeStep.setValue(1)
        intBoxStreamtubeStep.setDefaultValue("1")
        intBoxStreamtubeStep.setFontSize(16)
        intBoxStreamtubeStep.setFormat("[1-9]|1[0-9]|[20]")
        intBoxStreamtubeStep.setSpinnable(True)
        intBoxStreamtubeStep.setMinValue(1)
        intBoxStreamtubeStep.setMaxValue(20)
        intBoxStreamtubeStep.setValueIncrement(1)
        def update_cb(state):
            self.gl_canvas.setStreamtubeStep(intBoxStreamtubeStep.value())
        intBoxStreamtubeStep.setCallback(update_cb)

    def dotsRenderWindow(self):
        """ Popup window for Dots Renderer control and options"""
        
        popupBtnDotRenderer = PopupButton(self.window, "Dots")
        popupBtnDotRenderer.setFontSize(16)
        
        popupDotRenderer = popupBtnDotRenderer.popup()
        popupDotRenderer.setLayout(GroupLayout())
        Label(popupDotRenderer, "Dot Renderer Options", "sans-bold")
        def cb(state):
            self.gl_canvas.switchDotRenderer(comboDotStyle.selectedIndex())
            self.gl_canvas.setDotRadius(sliderDotRadius.value())
        chb = CheckBox(popupDotRenderer, "Dot", cb)
        def cb(state):
            self.gl_canvas.setDotRadius(sliderDotRadius.value())
        sliderDotRadius = Slider(popupDotRenderer)
        sliderDotRadius.setRange([0,1000])
        sliderDotRadius.setValue(500)
        sliderDotRadius.setFixedWidth(120)
        sliderDotRadius.setCallback(cb)
        Label(popupDotRenderer, "Dot style") 
        comboDotStyle = ComboBox(popupDotRenderer, 
            self.gl_canvas.getDotStyles())
        def cb(state):
            self.gl_canvas.setDotStyle( comboDotStyle.selectedIndex()) 
        comboDotStyle.setCallback( cb ) 
        comboDotStyle.setFontSize(16)
        comboDotStyle.setFixedSize((100, 20))

    def neighborsRendererWindow(self):
        """ Popup window for Neighbors Renderer control and options"""
        
        popupBtnNeighborsRenderer = PopupButton(self.window, "Neighbors")
        popupBtnNeighborsRenderer.setFontSize(16)
        
        popupNeighborsRenderer = popupBtnNeighborsRenderer.popup()
        popupNeighborsRenderer.setLayout(GroupLayout())
        Label(popupNeighborsRenderer, "Neighbors Renderer Options", "sans-bold")
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


    def cubesRendererWindow(self):
        """ Popup window for Cubes Renderer control and options"""

        popupBtnCubesRenderer = PopupButton(self.window, "Cubes")
        popupBtnCubesRenderer.setFontSize(16) 
        
        popupCubesRenderer = popupBtnCubesRenderer.popup()
        popupCubesRenderer.setLayout(GroupLayout())
        Label(popupCubesRenderer, "Cubes Renderer Options", "sans-bold")
        def cb(state):
            self.gl_canvas.switchCubesRenderer()
            self.gl_canvas.setCubesSize(sliderCubeSize.value())
        chb = CheckBox(popupCubesRenderer, "Cubes", cb)
        def cb(state):
            self.gl_canvas.setCubesSize(sliderCubeSize.value())
        sliderCubeSize = Slider(popupCubesRenderer)
        sliderCubeSize.setValue(0.25)
        sliderCubeSize.setRange((0, 0.5))
        sliderCubeSize.setFixedWidth(120)
        sliderCubeSize.setCallback(cb)

    def arrowsRendererWindow(self):
        """ Popup window for Arrows Renderer control and options"""
        
        popupBtnArrowsRenderer = PopupButton(self.window, "Arrows")
        popupBtnArrowsRenderer.setFontSize(16)

        popupArrowsRenderer = popupBtnArrowsRenderer.popup()
        popupArrowsRenderer.setLayout(GroupLayout())
        Label(popupArrowsRenderer, "Arrows Renderer Options", "sans-bold")
        def cb(state):
            self.gl_canvas.switchArrowsRenderer()
        chb = CheckBox(popupArrowsRenderer, "Arrows", cb)
        chb.setChecked(self.gl_canvas.show_arrows)

    def miscaleneousRenderersWindow(self):

        popupBtnMiscRenderers = PopupButton(self.window, "Misc")
        popupBtnMiscRenderers.setFontSize(16)

        popupMiscRenderers = popupBtnMiscRenderers.popup()
        popupMiscRenderers.setLayout(GroupLayout())
        Label(popupMiscRenderers, "Miscaleneous Renderers", "sans-bold")
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

    def windowRenderers(self):
        height = 240
        height_min = 30
        width = 200
        self.window = Window(self, "Renderers")
        self.window.setFixedSize(
            (width*self.pixelRatio(), height*self.pixelRatio()))
        self.window.setPosition((5, 235))
        self.window.setLayout(GroupLayout())

        self.arrowsRendererWindow();
        self.cubesRendererWindow();
        self.dotsRenderWindow();
        self.streamtubeRendererWindow();
        self.neighborsRendererWindow();
        self.miscaleneousRenderersWindow();
        
        buttons = self.window.buttonPanel()

        # Minimize/Maximize
        b_minmax = Button(buttons, "", icon=entypo.ICON_CHEVRON_DOWN)

        def cb():
            if self.window.height() == height_min:
                self.window.setHeight(height)
            else:
                self.window.setHeight(height_min)
            b_minmax.setPushed(not b_minmax.pushed())
        b_minmax.setCallback(cb)

        # Close
        b_close = Button(buttons, "", icon=entypo.ICON_CIRCLE_WITH_CROSS)

        def cb():
            self.window.dispose()
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

