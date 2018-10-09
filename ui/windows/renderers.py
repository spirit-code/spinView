from nanogui import Label, Button, PopupButton, GroupLayout, Slider, ComboBox, IntBox, CheckBox
from . import base

class RenderersWindow(base.FloatingWindow):
    
    def __init__(self, parent_window):
        # TODO: move that to the init arguments of the Object 
        position =(5, 235)
        super(RenderersWindow, self).__init__(parent_window, position)
        # Renderers 
        self.arrowsRendererWindow();
        self.cubesRendererWindow();
        self.dotsRenderWindow();
        self.streamtubesRendererWindow();
        self.neighborsRendererWindow();
        self.miscaleneousRenderersWindow();
    
    def streamtubesOptionsUpdate(self):
        self.pw.gl_canvas.streamtubes.setRadius(self.sliderStreamtubeRadius.value())
        self.pw.gl_canvas.streamtubes.setResolution(self.intBoxStreamtubeLoD.value())
        self.pw.gl_canvas.streamtubes.setSmoothing(self.intBoxStreamtubeSmoothing.value())
        self.pw.gl_canvas.streamtubes.setStep(self.intBoxStreamtubeStep.value())

    def streamtubesRedraw(self):
        # If the renderer is activated swich off and on for redraw
        if self.pw.gl_canvas.streamtubes.show:
            # Switch Off 
            self.pw.gl_canvas.streamtubes.switch()
            self.pw.gl_canvas.updateRenderers()
            # Switch On 
            self.pw.gl_canvas.streamtubes.switch()
            self.pw.gl_canvas.updateRenderers()

    def streamtubesRendererWindow(self):
        """ Popup window for Streamtube Renderer control and options"""

        popupBtnStreamTubeRenderer = PopupButton(self.window, "Stream tube")
        popupBtnStreamTubeRenderer.setFontSize(16)

        popupStreamTubeRenderer = popupBtnStreamTubeRenderer.popup()
        popupStreamTubeRenderer.setLayout(GroupLayout())
        Label(popupStreamTubeRenderer, "Stream Tube Renderer Options", "sans-bold")
        def cb(state):
            
            if cb_circular.checked():
                self.pw.gl_canvas.streamtubes.setStyle(0) 
            elif cb_grid.checked():
                self.pw.gl_canvas.streamtubes.setStyle(1)
            self.streamtubesRedraw() 
                 
            self.pw.gl_canvas.streamtubes.switch()
            self.pw.gl_canvas.updateRenderers() 
            # Update options 
            self.streamtubesOptionsUpdate()
        cb = CheckBox(popupStreamTubeRenderer, "Stream Tube", cb)
        
        Label(popupStreamTubeRenderer, "Stream base style :") 
        
        # Circular Base Switch and Options
        def cb_circular(state):
            # In case of recheck we do not want redrawing
            if cb_circular.checked():
                cb_grid.setChecked(False)
                self.pw.gl_canvas.streamtubes.setStyle(0) 
                self.streamtubesRedraw() 
                self.streamtubesOptionsUpdate()
            cb_circular.setChecked(True) 
        cb_circular = CheckBox(popupStreamTubeRenderer, "Circular", cb_circular)
        cb_circular.setChecked(True) 
        popupBtnCircular = PopupButton(popupStreamTubeRenderer, "Circular Base Options") 
        popupBtnCircular.setFontSize(14)
        popupCircular = popupBtnCircular.popup()
        popupCircular.setLayout(GroupLayout()) 
        Label(popupCircular, "Spins in circumeference :")
        Label(popupCircular, "Radius :")
        Label(popupCircular, "Position :")

        # Grid Base Switch and Options
        def cb_grid(state):
            # In case of recheck we do not want redrawing
            if cb_grid.checked():
                cb_circular.setChecked(False)
                self.pw.gl_canvas.streamtubes.setStyle(1) 
                self.streamtubesRedraw() 
                self.streamtubesOptionsUpdate()
            cb_grid.setChecked(True)
        cb_grid = CheckBox(popupStreamTubeRenderer, "Grid", cb_grid)
        cb_grid.setChecked(False)
        popupBtnGrid = PopupButton(popupStreamTubeRenderer, "Grid Base Options") 
        popupBtnGrid.setFontSize(14)
        popupGrid = popupBtnGrid.popup()
        popupGrid.setLayout(GroupLayout())
        Label(popupGrid, "Spins in circumeference :")
        Label(popupGrid, "Position :")
        
        Label(popupStreamTubeRenderer, "Stream Tube Options :") 
        popupBtnGeneral = PopupButton(popupStreamTubeRenderer, "General Options") 
        popupBtnGeneral.setFontSize(14)
        popupGeneral = popupBtnGeneral.popup()
        popupGeneral.setLayout(GroupLayout()) 

        Label(popupGeneral, "Streamtube radius :") 
        def cb(state):
            self.pw.gl_canvas.streamtubes.setRadius(self.sliderStreamtubeRadius.value())
            self.pw.gl_canvas.updateRenderers()
        self.sliderStreamtubeRadius = Slider(popupGeneral)
        self.sliderStreamtubeRadius.setValue(self.pw.gl_canvas.streamtubes.getOptions()[0])
        self.sliderStreamtubeRadius.setRange((0, 2*self.sliderStreamtubeRadius.value()))
        self.sliderStreamtubeRadius.setFixedWidth(120)
        self.sliderStreamtubeRadius.setCallback(cb)
        
        Label(popupGeneral, "Streamtube level of detail :") 
        self.intBoxStreamtubeLoD = IntBox(popupGeneral)
        self.intBoxStreamtubeLoD.setEditable(True)
        self.intBoxStreamtubeLoD.setFixedSize((150, 20))
        self.intBoxStreamtubeLoD.setUnits("absolute")
        self.intBoxStreamtubeLoD.setValue(int(self.pw.gl_canvas.streamtubes.getOptions()[1]))
        self.intBoxStreamtubeLoD.setFontSize(16)
        self.intBoxStreamtubeLoD.setFormat("[3-9]|1[0-9]|20")
        self.intBoxStreamtubeLoD.setSpinnable(True)
        self.intBoxStreamtubeLoD.setMinValue(3)
        self.intBoxStreamtubeLoD.setMaxValue(20)
        self.intBoxStreamtubeLoD.setValueIncrement(1)
        def update_cb(state):
            self.pw.gl_canvas.streamtubes.setResolution(self.intBoxStreamtubeLoD.value())
            self.pw.gl_canvas.updateRenderers()
        self.intBoxStreamtubeLoD.setCallback(update_cb)
        
        Label(popupGeneral, "Streamtube smoothing :") 
        self.intBoxStreamtubeSmoothing = IntBox(popupGeneral)
        self.intBoxStreamtubeSmoothing.setEditable(True)
        self.intBoxStreamtubeSmoothing.setFixedSize((150, 20))
        self.intBoxStreamtubeSmoothing.setUnits("steps")
        self.intBoxStreamtubeSmoothing.setValue(int(self.pw.gl_canvas.streamtubes.getOptions()[3]))
        self.intBoxStreamtubeSmoothing.setFontSize(16)
        self.intBoxStreamtubeSmoothing.setFormat("[0-9]")
        self.intBoxStreamtubeSmoothing.setSpinnable(True)
        self.intBoxStreamtubeSmoothing.setMinValue(0)
        self.intBoxStreamtubeSmoothing.setMaxValue(9)
        self.intBoxStreamtubeSmoothing.setValueIncrement(1)
        def update_cb(state):
            self.pw.gl_canvas.streamtubes.setSmoothing(self.intBoxStreamtubeSmoothing.value())
            self.pw.gl_canvas.updateRenderers()
        self.intBoxStreamtubeSmoothing.setCallback(update_cb)
        
        Label(popupGeneral, "Streamtube step :") 
        self.intBoxStreamtubeStep = IntBox(popupGeneral)
        self.intBoxStreamtubeStep.setEditable(True)
        self.intBoxStreamtubeStep.setFixedSize((150, 20))
        self.intBoxStreamtubeStep.setValue(int(self.pw.gl_canvas.streamtubes.getOptions()[2]))
        self.intBoxStreamtubeStep.setDefaultValue("1")
        self.intBoxStreamtubeStep.setFontSize(16)
        self.intBoxStreamtubeStep.setFormat("[1-9]|1[0-9]|[20]")
        self.intBoxStreamtubeStep.setSpinnable(True)
        self.intBoxStreamtubeStep.setMinValue(1)
        self.intBoxStreamtubeStep.setMaxValue(20)
        self.intBoxStreamtubeStep.setValueIncrement(1)
        def update_cb(state):
            self.pw.gl_canvas.streamtubes.setStep(self.intBoxStreamtubeStep.value())
            self.pw.gl_canvas.updateRenderers()
        self.intBoxStreamtubeStep.setCallback(update_cb)

    def dotsRenderWindow(self):
        """ Popup window for Dots Renderer control and options"""
        
        popupBtnDotRenderer = PopupButton(self.window, "Dots")
        popupBtnDotRenderer.setFontSize(16)
        
        popupDotRenderer = popupBtnDotRenderer.popup()
        popupDotRenderer.setLayout(GroupLayout())
        Label(popupDotRenderer, "Dot Renderer Options", "sans-bold")
        def cb(state):
            self.pw.gl_canvas.dots.switch(comboDotStyle.selectedIndex())
            self.pw.gl_canvas.dots.setSize(sliderDotRadius.value())
            self.pw.gl_canvas.updateRenderers() 
        chb = CheckBox(popupDotRenderer, "Dot", cb)
        def cb(state):
            self.pw.gl_canvas.dots.setSize(sliderDotRadius.value())
            self.pw.gl_canvas.updateRenderers() 
        sliderDotRadius = Slider(popupDotRenderer)
        sliderDotRadius.setRange([0,1000])
        sliderDotRadius.setValue(500)
        sliderDotRadius.setFixedWidth(120)
        sliderDotRadius.setCallback(cb)
        Label(popupDotRenderer, "Dot style") 
        comboDotStyle = ComboBox(popupDotRenderer, 
            self.pw.gl_canvas.dots.getStyles())
        def cb(state):
            self.pw.gl_canvas.dots.setStyle( comboDotStyle.selectedIndex()) 
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
            self.pw.gl_canvas.neighbors.switch(intBox.value()-1)
            self.pw.gl_canvas.updateRenderers()
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
            self.pw.gl_canvas.neighbors.setIndex(intBox.value()-1)
            self.pw.gl_canvas.updateRenderers()
        intBox.setCallback(update_cb)

    def cubesRendererWindow(self):
        """ Popup window for Cubes Renderer control and options"""

        popupBtnCubesRenderer = PopupButton(self.window, "Cubes")
        popupBtnCubesRenderer.setFontSize(16) 
        
        popupCubesRenderer = popupBtnCubesRenderer.popup()
        popupCubesRenderer.setLayout(GroupLayout())
        Label(popupCubesRenderer, "Cubes Renderer Options", "sans-bold")
        def cb(state):
            # self.pw.gl_canvas.switchCubesRenderer()
            self.pw.gl_canvas.cubes.switch() 
            # self.pw.gl_canvas.setCubesSize(sliderCubeSize.value())
            self.pw.gl_canvas.cubes.setSize(sliderCubeSize.value()) 
            self.pw.gl_canvas.updateRenderers()
        chb = CheckBox(popupCubesRenderer, "Cubes", cb)
        def cb(state):
            # self.pw.gl_canvas.setCubesSize(sliderCubeSize.value())
            self.pw.gl_canvas.cubes.setSize(sliderCubeSize.value()) 
            self.pw.gl_canvas.updateRenderers()
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
            self.pw.gl_canvas.arrows.switch()
            self.pw.gl_canvas.updateRenderers()
        chb = CheckBox(popupArrowsRenderer, "Arrows", cb)
        chb.setChecked(self.pw.gl_canvas.arrows.show)

    def miscaleneousRenderersWindow(self):
        """ Popup window for other Renderers and general options"""

        popupBtnMiscRenderers = PopupButton(self.window, "Misc")
        popupBtnMiscRenderers.setFontSize(16)

        popupMiscRenderers = popupBtnMiscRenderers.popup()
        popupMiscRenderers.setLayout(GroupLayout())
        Label(popupMiscRenderers, "Miscaleneous Renderers", "sans-bold")
        def cb(state):
            self.pw.gl_canvas.coordinate.switch()
            self.pw.gl_canvas.updateRenderers()
        chb = CheckBox(popupMiscRenderers, "Coordinates", cb)
        chb.setChecked(self.pw.gl_canvas.coordinate.show)
        def cb(state):
            print("Not implemented!")
        chb = CheckBox(popupMiscRenderers, "ArrowsSphere", cb)
        def cb(state):
            self.pw.gl_canvas.bounding_box.switch()
            self.pw.gl_canvas.updateRenderers()
        chb = CheckBox(popupMiscRenderers, "Bounding Box", cb)
        chb.setChecked(self.pw.gl_canvas.bounding_box.show)
