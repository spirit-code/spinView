from nanogui import Label, Button, PopupButton, GroupLayout, Slider, ComboBox, IntBox, CheckBox
from . import base

class RenderersWindow(base.FloatingWindow):
    
    def __init__(self, parent_window):
        position = (5, 235)
        super(RenderersWindow, self).__init__(parent_window, position)
        # Renderers 
        self.arrowsRendererWindow();
        self.cubesRendererWindow();
        self.dotsRenderWindow();
        self.streamtubeRendererWindow();
        self.neighborsRendererWindow();
        self.miscaleneousRenderersWindow();
    
    def streamtubeOptionsUpdate():
        self.pw.gl_canvas.setStreamtubeRadius(sliderStreamtubeRadius.value())
        self.pw.gl_canvas.setStreamtubeResolution(intBoxStreamtubeLoD.value())
        self.pw.gl_canvas.setStreamtubeSmoothing(intBoxStreamtubeSmoothing.value())
        self.pw.gl_canvas.setStreamtubeStep(intBoxStreamtubeStep.value())
    
    def streamtubeRendererWindow(self):
        """ Popup window for Streamtube Renderer control and options"""

        popupBtnStreamTubeRenderer = PopupButton(self.window, "Stream tube")
        popupBtnStreamTubeRenderer.setFontSize(16)

        popupStreamTubeRenderer = popupBtnStreamTubeRenderer.popup()
        popupStreamTubeRenderer.setLayout(GroupLayout())
        Label(popupStreamTubeRenderer, "Stream Tube Renderer Options", "sans-bold")
        def cb(state):
            if cb_circular.checked():
                self.pw.gl_canvas.setStreamTubeBaseStyle(0) 
            elif cb_grid.checked():
                self.pw.gl_canvas.setStreamTubeBaseStyle(1)
            self.pw.gl_canvas.switchStreamtubeRenderer()
            self.streamtubeOptionsUpdate()
        cb = CheckBox(popupStreamTubeRenderer, "Stream Tube", cb)
        
        Label(popupStreamTubeRenderer, "Stream base style :") 
        # Circular Base Switch and Options
        def cb_circular(state):
            # In case of recheck we do not want redrawing
            if cb_circular.checked():
                cb_grid.setChecked(False)
                self.pw.gl_canvas.setStreamTubeBaseStyle(0) 
                self.streamtubeOptionsUpdate()
            cb_circular.setChecked(True) 
        cb_circular = CheckBox(popupStreamTubeRenderer, "Circular", cb_circular)
        cb_circular.setChecked(True) 
        popupBtnCircular = PopupButton(popupStreamTubeRenderer, "Circular Base Options") 
        popupBtnCircular.setFontSize(14)
        popupCircular = popupBtnCircular.popup()
        popupCircular.setLayout(GroupLayout()) 
        # Grid Base Switch and Options
        def cb_grid(state):
            # In case of recheck we do not want redrawing
            if cb_grid.checked():
                cb_circular.setChecked(False)
                self.pw.gl_canvas.setStreamTubeBaseStyle(1)
                self.streamtubeOptionsUpdate()
            cb_grid.setChecked(True)
        cb_grid = CheckBox(popupStreamTubeRenderer, "Grid", cb_grid)
        cb_grid.setChecked(False)
        popupBtnGrid = PopupButton(popupStreamTubeRenderer, "Grid Base Options") 
        popupBtnGrid.setFontSize(14)
        popupGrid = popupBtnGrid.popup()
        popupGrid.setLayout(GroupLayout()) 
        
        
        Label(popupStreamTubeRenderer, "Stream Tube Options :") 
        popupBtnGeneral = PopupButton(popupStreamTubeRenderer, "General Options") 
        popupBtnGeneral.setFontSize(14)
        popupGeneral = popupBtnGeneral.popup()
        popupGeneral.setLayout(GroupLayout()) 

        Label(popupGeneral, "Streamtube radius :") 
        def cb(state):
            self.pw.gl_canvas.setStreamtubeRadius(sliderStreamtubeRadius.value())
        sliderStreamtubeRadius = Slider(popupGeneral)
        sliderStreamtubeRadius.setRange((0, 0.25))
        sliderStreamtubeRadius.setValue(0.125)
        sliderStreamtubeRadius.setFixedWidth(120)
        sliderStreamtubeRadius.setCallback(cb)
        
        Label(popupGeneral, "Streamtube level of detail :") 
        intBoxStreamtubeLoD = IntBox(popupGeneral)
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
            self.pw.gl_canvas.setStreamtubeResolution(intBoxStreamtubeLoD.value())
        intBoxStreamtubeLoD.setCallback(update_cb)
        
        Label(popupGeneral, "Streamtube smoothing :") 
        intBoxStreamtubeSmoothing = IntBox(popupGeneral)
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
            self.pw.gl_canvas.setStreamtubeSmoothing(intBoxStreamtubeSmoothing.value())
        intBoxStreamtubeSmoothing.setCallback(update_cb)
        
        Label(popupGeneral, "Streamtube step :") 
        intBoxStreamtubeStep = IntBox(popupGeneral)
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
            self.pw.gl_canvas.setStreamtubeStep(intBoxStreamtubeStep.value())
        intBoxStreamtubeStep.setCallback(update_cb)

    def dotsRenderWindow(self):
        """ Popup window for Dots Renderer control and options"""
        
        popupBtnDotRenderer = PopupButton(self.window, "Dots")
        popupBtnDotRenderer.setFontSize(16)
        
        popupDotRenderer = popupBtnDotRenderer.popup()
        popupDotRenderer.setLayout(GroupLayout())
        Label(popupDotRenderer, "Dot Renderer Options", "sans-bold")
        def cb(state):
            self.pw.gl_canvas.switchDotRenderer(comboDotStyle.selectedIndex())
            self.pw.gl_canvas.setDotRadius(sliderDotRadius.value())
        chb = CheckBox(popupDotRenderer, "Dot", cb)
        def cb(state):
            self.pw.gl_canvas.setDotRadius(sliderDotRadius.value())
        sliderDotRadius = Slider(popupDotRenderer)
        sliderDotRadius.setRange([0,1000])
        sliderDotRadius.setValue(500)
        sliderDotRadius.setFixedWidth(120)
        sliderDotRadius.setCallback(cb)
        Label(popupDotRenderer, "Dot style") 
        comboDotStyle = ComboBox(popupDotRenderer, 
            self.pw.gl_canvas.getDotStyles())
        def cb(state):
            self.pw.gl_canvas.setDotStyle( comboDotStyle.selectedIndex()) 
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
            self.pw.gl_canvas.switchNeighborRenderer(intBox.value()-1)
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
            self.pw.gl_canvas.drawNeighbors(intBox.value()-1)
        intBox.setCallback(update_cb)

    def cubesRendererWindow(self):
        """ Popup window for Cubes Renderer control and options"""

        popupBtnCubesRenderer = PopupButton(self.window, "Cubes")
        popupBtnCubesRenderer.setFontSize(16) 
        
        popupCubesRenderer = popupBtnCubesRenderer.popup()
        popupCubesRenderer.setLayout(GroupLayout())
        Label(popupCubesRenderer, "Cubes Renderer Options", "sans-bold")
        def cb(state):
            self.pw.gl_canvas.switchCubesRenderer()
            self.pw.gl_canvas.setCubesSize(sliderCubeSize.value())
        chb = CheckBox(popupCubesRenderer, "Cubes", cb)
        def cb(state):
            self.pw.gl_canvas.setCubesSize(sliderCubeSize.value())
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
            self.pw.gl_canvas.switchArrowsRenderer()
        chb = CheckBox(popupArrowsRenderer, "Arrows", cb)
        chb.setChecked(self.pw.gl_canvas.show_arrows)

    def miscaleneousRenderersWindow(self):

        popupBtnMiscRenderers = PopupButton(self.window, "Misc")
        popupBtnMiscRenderers.setFontSize(16)

        popupMiscRenderers = popupBtnMiscRenderers.popup()
        popupMiscRenderers.setLayout(GroupLayout())
        Label(popupMiscRenderers, "Miscaleneous Renderers", "sans-bold")
        def cb(state):
            self.pw.gl_canvas.switchCoordinateSystemRenderer()
        chb = CheckBox(popupMiscRenderers, "Coordinates", cb)
        chb.setChecked(self.pw.gl_canvas.show_coordinate_system)
        def cb(state):
            print("Not implemented!")
        chb = CheckBox(popupMiscRenderers, "ArrowsSphere", cb)
        def cb(state):
            self.pw.gl_canvas.switchBoundingBoxRenderer()
        chb = CheckBox(popupMiscRenderers, "Bounding Box", cb)
        chb.setChecked(self.pw.gl_canvas.show_bounding_box)
