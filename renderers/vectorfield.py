import pyVFRendering as vfr
import numpy as np
from .general import Renderer

class VectorfieldRenderer(Renderer):
    
    def __init__(self, view, vf, vfr_renderer):
        super().__init__(view)
        self.vfr_renderer = vfr_renderer
        self.vf = vf
        self.update()

    def update(self):
        self.renderer = self.vfr_renderer(self.view, self.vf)
    

class ArrowsRenderer(VectorfieldRenderer):
    
    def __init__(self, view, vf):
        super().__init__(view, vf, vfr.ArrowRenderer)


class DotsRenderer(VectorfieldRenderer):

    def __init__(self, view, vf):
        super().__init__(view, vf, vfr.DotRenderer)

    def switch(self, index):
        super().switch()
        self.setStyle(index)

    def setSize(self, size):
        if self.show:
            self.renderer.setDotRadius(size)

    def getStyles(self):
        return [style for style in vfr.DotRendererStyle.__members__]

    def setStyle(self, index):
        if self.show: 
            self.renderer.setDotStyle(index) 


class CubesRenderer(VectorfieldRenderer):
    
    def __init__(self, view, vf):
        super().__init__(view, vf, vfr.ParallelepipedRenderer)
    
    def setSize(self, size):
        if self.show:
            self.renderer = vfr.ParallelepipedRenderer(self.view, self.vf)
            self.renderer.setParallelepipedLengthA(size)
            self.renderer.setParallelepipedLengthB(size)
            self.renderer.setParallelepipedLengthC(size)

class StreamTubeRenderer(VectorfieldRenderer):

    def __init__(self, view, vf, system_dimensions):
        self.positions = [] # NOTE: must be called before parent method 
        self.sys_dim = system_dimensions
        super().__init__(view, vf, vfr.StreamTubeRenderer)

    def getOptions(self):
        temp = vfr.StreamTubeRenderer(self.view, self.vf)
        return temp.getRadius(), temp.getLevelOfDetail(),\
               temp.getStep(), temp.getSmoothingSteps() 
    
    def switch(self):
        # Set the positions before calling the parent method 
        if not self.show:
            self.positions = self.streamtubeBase()
        else:
            self.positions = []
        super().switch() 

    def update(self):
        super().update() 
        self.renderer.seedPositions(self.positions)

    def setStyle(self, style):
        if style == 0:
            self.streamtubeBase = self.circularSeeds
        elif style == 1:
            self.streamtubeBase = self.gridSeeds 

    def setRadius(self, radius):
        if self.show:
            self.renderer.setRadius(radius)

    def setResolution(self, resolution):
        if self.show:
            self.renderer.setLevelOfDetail(resolution)

    def setSmoothing(self, smoothing_steps):
        if self.show:
            self.renderer.setSmoothingSteps(smoothing_steps)

    def setStep(self, interpolation_step):
        if self.show:
            self.renderer.setStep(interpolation_step)

    def circularSeeds(self):
        midx = (self.sys_dim[0] - 1) / 2
        midy = (self.sys_dim[1] - 1) / 2
        num_positions = 8                               # TODO: setter
        radius = 2                                      # TODO: setter
        positions = np.zeros(0)
        for i in range(num_positions):
            angle = ( 2 * np.pi * i / num_positions )
            positions = np.append(positions, np.array([midx + radius * np.sin(angle),
                                                       midy + radius * np.cos(angle), 
                                                       self.sys_dim[2] / 2]))
        return positions.reshape(num_positions,3)

    def gridSeeds(self):
        midx = (self.sys_dim[0] - 1) / 2
        midy = (self.sys_dim[1] - 1) / 2
        z = self.sys_dim[2] / 2
        xside, yside = (4, 4)                            # TODO: setter
        xstep, ystep = (1, 1) # Increase by 2 for even side points or by 1 for odd
        nos = xside * yside
        gxx, gyy = np.mgrid[ midx - xstep * (xside - 1) / 2 : 
                             midx + xstep * (xside - 1) / 2 : xside * 1j,
                             midy - ystep * (yside - 1) / 2 : 
                             midy + ystep * (yside - 1) / 2 : yside * 1j ]
        gxx = gxx.reshape(1, nos)
        gyy = gyy.reshape(1, nos)
        gzz = np.full((1, nos), z)
        return np.dstack((gxx, gyy, gzz))[0]

