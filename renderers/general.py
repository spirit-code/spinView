import pyVFRendering as vfr
import numpy as np


class Renderer():
    
    def __init__(self, view):
        self.view = view 
        self.show = False

    def switch(self):
        self.show = not self.show
        self.update()

    def update(self):
        pass 

    def getOptions(self):
        pass

    def getDetails(self):
        pass


class CoordinateSystemRenderer(Renderer):
    
    def switch(self):
        super().switch()
        self.position = [0.9, 0, 0.1, 0.1]
        self.renderer = vfr.CoordinateSystemRenderer(self.view)
        self.renderer.setAxisLength([1, 1, 1])
        self.renderer.setNormalize(True)


class BoundingBoxRenderer(Renderer):

    def __init__(self, view, geometry, system_dimensions):
        super().__init__(view)
        self.geometry = geometry
        self.sys_dim = system_dimensions

    def switch(self):
        super().switch()
        self.renderer = vfr.BoundingBoxRenderer.forCuboid(self.view, 
                (self.geometry.min() + self.geometry.max()) * 0.5, 
                [self.sys_dim[0], self.sys_dim[1], self.sys_dim[2]],
                [0, 0, 0], 1)


class NeighborsRenderer(Renderer):

    def __init__(self, view, geometry, system_dimensions):
        self.geometry = geometry
        self.sys_dimen = system_dimensions
        self.nos = self.sys_dimen[0] * self.sys_dimen[1] * self.sys_dimen[2]
        super().__init__(view)
    
    def switch(self, index):
        self.index = index
        super().switch() 

    def setIndex(self, index):
        self.index = index 
        if self.show:
            self.update()

    def update(self):
        scale = 0.8
        cyan_sph = np.array([-1, -1, 0.7]) / np.linalg.norm([-1, -1, 0.7])
        pink_sph = np.array([0, 1, 0.7]) / np.linalg.norm([0, 1, 0.7])

        # Check index
        if self.index >= self.nos:
            print("Error: Invalid indeces in Neighbors Renderer")
            return

        # Turn single index into 3D indeces i,j,k
        i = self.index % self.sys_dimen[0]
        j = ((self.index - i) // self.sys_dimen[0]) % self.sys_dimen[1]
        k = (((self.index - i) // self.sys_dimen[0]) - j) // self.sys_dimen[1]
       
        # Create a new direction array that represents the neighbor spheres
        directions = [[0, 0, 0] for x in range(self.nos)]

        # Set the sphere for the spin tha we are looking at
        self.index = k * self.sys_dimen[0] * self.sys_dimen[1] + j * self.sys_dimen[0] + i
        directions[self.index] = cyan_sph

        # Set the neighbors
        x_plus = self.index + 1
        if x_plus < self.nos and x_plus >= 0 and not i == (self.sys_dimen[0] - 1):
            directions[x_plus] = pink_sph

        x_minus = self.index - 1
        if x_minus < self.nos and x_minus >= 0 and not i == 0:
            directions[x_minus] = pink_sph

        y_plus = self.index + self.sys_dimen[0]
        if y_plus < self.nos and y_plus >= 0 and not j == (self.sys_dimen[1] - 1):
            directions[y_plus] = pink_sph

        y_minus = self.index - self.sys_dimen[0]
        if y_minus < self.nos and y_minus >= 0 and not j == 0:
            directions[y_minus] = pink_sph

        z_plus = self.index + self.sys_dimen[0] * self.sys_dimen[1]
        if z_plus < self.nos and z_plus >= 0 and not k == (self.sys_dimen[2] - 1):
            directions[z_plus] = pink_sph

        z_minus = self.index - self.sys_dimen[0] * self.sys_dimen[1]
        if z_minus < self.nos and z_minus >= 0 and not k == 0:
            directions[z_minus] = pink_sph

        # Scale and add the sphere renderer
        # NOTE: the neighbors_vf variable MUST be member variable otherwise the
        # VFRendering will crash randomly when we are out of scope
        directions = np.array(directions) * scale
        self.neighbors_vf = vfr.VectorField(self.geometry, directions)
        self.renderer = vfr.SphereRenderer(self.view, self.neighbors_vf)
        
