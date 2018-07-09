import pyVFRendering as vfr
import numpy as np

from nanogui import gl, glfw, GLCanvas

class GLWidget(GLCanvas):

    def __init__(self, parent):
        super(GLWidget, self).__init__(parent)

        # Set the size to be equal to Screen
        self.setSize(parent.size())

        self.system_dimensions = np.array([3, 5, 4])
        self.nx = self.system_dimensions[0]
        self.ny = self.system_dimensions[1]
        self.nz = self.system_dimensions[2]

        # Create the VFR.geometry
        n_cells = self.system_dimensions
        self.geometry = vfr.Geometry.rectilinearGeometry(
            range(n_cells[0]), range(n_cells[1]), range(n_cells[2]))

        # Initialize directions
        directions = []
        for iz in range(n_cells[2]):
            for iy in range(n_cells[1]):
                for ix in range(n_cells[0]):
                    directions.append([0, 0, 0.5])
        self.directions = np.array(directions)
        
        directions[0] = np.array([0,-0.5,0]) 

        # Create the VFR.view
        self.view = vfr.View()
        self.view.setFramebufferSize(
            parent.size()[0]*parent.pixelRatio(),
            parent.size()[1]*parent.pixelRatio())

        # Create/Init VFR.vf
        self.vf = vfr.VectorField(self.geometry, directions)

        # Renderers
        self.show_arrows = False
        self.show_dots = False
        self.show_neighbors = False
        self.show_coordinate_system = False
        self.show_cubes = False 
        self.show_bounding_box = False
        
        # Switch on initial renderers
        self.switchArrowsRenderer()
        self.switchCoordinateSystemRenderer()

        self._setupRenderers()

        # Options
        self.options = vfr.Options()
        self.options.setBackgroundColor([0.5, 0.5, 0.5])
        self.options.setColormapImplementation(
            vfr.getColormapImplementation(vfr.Colormap.hsv))
        self.options.setSystemCenter(
            (self.geometry.min() + self.geometry.max())*0.5)
        self.options.setCameraPosition([-30, 0, 0])
        self.options.setCenterPosition(self.options.getSystemCenter())
        self.options.setUpVector([0, 0, 1])
        self.view.updateOptions(self.options)

        # For mouse movement events
        self.previous_mouse_position = [0, 0]


    def switchNeighborRenderer(self, index):
        self.drawNeighbors(index)
        self.show_neighbors = not self.show_neighbors
        self._setupRenderers()

    def drawNeighbors(self, index):
        scale = 0.8
        cyan_sph = np.array([-1, -1, 0.7])/np.linalg.norm([-1, -1, 0.7])
        pink_sph = np.array([0, 1, 0.7])/np.linalg.norm([0, 1, 0.7])

        # check index
        nos = self.nx*self.ny*self.nz
        if index >= nos:
            print("Error: Invalid indeces in Neighbor Renderer")
            return

        # turn single index into 3D indeces i,j,k
        i = index % self.nx
        j = ((index - i) // self.nx) % self.ny
        k = (((index - i) // self.nx) - j) // self.ny

        # create a new direction array that represents the neighbor spheres
        directions = [[0, 0, 0] for x in range(nos)]

        # set the sphere for the spin tha we are looking at
        index = k*self.nx*self.ny + j*self.nx + i
        directions[index] = cyan_sph

        # set the neighbors
        x_plus = index + 1
        if x_plus < nos and x_plus >= 0 and not i == (self.nx-1):
            directions[x_plus] = pink_sph

        x_minus = index - 1
        if x_minus < nos and x_minus >= 0 and not i == 0:
            directions[x_minus] = pink_sph

        y_plus = index + self.nx
        if y_plus < nos and y_plus >= 0 and not j == (self.ny-1):
            directions[y_plus] = pink_sph

        y_minus = index - self.nx
        if y_minus < nos and y_minus >= 0 and not j == 0:
            directions[y_minus] = pink_sph

        z_plus = index + self.nx * self.ny
        if z_plus < nos and z_plus >= 0 and not k == (self.nz-1):
            directions[z_plus] = pink_sph

        z_minus = index - self.nx * self.ny
        if z_minus < nos and z_minus >= 0 and not k == 0:
            directions[z_minus] = pink_sph

        # scale and add the sphere renderer
        directions = np.array(directions)*scale
        self.neighbors_vf = vfr.VectorField(self.geometry, directions)
        self.renderer_neighbors = vfr.SphereRenderer(
            self.view, self.neighbors_vf)

        self._setupRenderers()

    def switchCoordinateSystemRenderer(self):
        self.position_coordinate_system = [
            0.9, 0, 0.1, 0.1]  # turn it into dynamic
        self.renderer_cs = vfr.CoordinateSystemRenderer(self.view)
        self.renderer_cs.setAxisLength([1, 1, 1])
        self.renderer_cs.setNormalize(True)

        self.show_coordinate_system = not self.show_coordinate_system
        self._setupRenderers()

    def switchDotRenderer(self, index):
        self.renderer_dots = vfr.DotRenderer(self.view, self.vf)
        self.show_dots = not self.show_dots
        self.renderer_dots.setDotStyle(index) 
        self._setupRenderers()

    def setDotRadius(self,size):
        if self.show_dots:
            self.renderer_dots.setDotRadius(size)
            self._setupRenderers()
    
    def getDotStyles(self):
        return [e for e in vfr.DotRendererStyle.__members__]

    def setDotStyle(self, index):
        if self.show_dots: 
            self.renderer_dots.setDotStyle(index) 

    def switchArrowsRenderer(self):
        self.renderer_arrows = vfr.ArrowRenderer(self.view, self.vf)
        self.show_arrows = not self.show_arrows
        self._setupRenderers()

    def switchBoundingBoxRenderer(self):
        self.renderer_bounding_box = vfr.BoundingBoxRenderer.forCuboid(self.view, 
                (self.geometry.min() + self.geometry.max())*0.5, 
                [self.nx, self.ny, self.nz], [0, 0, 0], 1)
        self.show_bounding_box = not self.show_bounding_box
        self._setupRenderers()
    
    def switchCubesRenderer(self):
        self.renderer_cubes = vfr.ParallelepipedRenderer(self.view, self.vf)
        self.show_cubes = not self.show_cubes
        self._setupRenderers()

    def setCubesSize(self,scale):
        if self.show_cubes:
            self.renderer_cubes.setParallelepipedLengthX(scale)
            self.renderer_cubes.setParallelepipedLengthY(scale)
            self.renderer_cubes.setParallelepipedLengthZ(scale)
            self._setupRenderers()

    def _setupRenderers(self):
        self.renderers_list = []
        if self.show_arrows:
            self.renderers_list.append(self.renderer_arrows)
        if self.show_dots:
            self.renderers_list.append(self.renderer_dots)
        if self.show_neighbors:
            self.renderers_list.append(self.renderer_neighbors)
        if self.show_bounding_box:
            self.renderers_list.append(self.renderer_bounding_box)
        if self.show_cubes:
            self.renderers_list.append(self.renderer_cubes)
        # combine renderers
        renderers_system = vfr.CombinedRenderer(
            self.view, self.renderers_list)
        renderers = [(renderers_system, [0.0, 0.0, 1.0, 1.0])]
        # last add the coordinate system renderer
        if self.show_coordinate_system:
            renderers.append(
                (self.renderer_cs, self.position_coordinate_system))
        # show renderers
        self.view.renderers(renderers, False)

    def drawGL(self):
        gl.Enable(gl.DEPTH_TEST)
        self.view.draw()
        gl.Disable(gl.DEPTH_TEST)

    def scrollEvent(self, p, rel):
        scale = 3
        self.view.mouseScroll(rel[1] * scale)
        return True

    def mouseDragEvent(self, p, rel, button, modifiers):
        scale = 1
        if button == glfw.MOUSE_BUTTON_2:
            # Right button
            camera_mode = vfr.CameraMovementModes.translate
            current_mouse_position = p
            self.view.mouseMove(self.previous_mouse_position, p, camera_mode)
            self.previous_mouse_position = current_mouse_position
            return True
        elif button == glfw.MOUSE_BUTTON_3:
            # Left button
            camera_mode = vfr.CameraMovementModes.rotate_bounded
            current_mouse_position = p
            self.view.mouseMove(self.previous_mouse_position, p, camera_mode)
            self.previous_mouse_position = current_mouse_position
            return True
        return False

    def mouseButtonEvent(self, p, button, down, modifiers):
        self.previous_mouse_position = p
        return True

