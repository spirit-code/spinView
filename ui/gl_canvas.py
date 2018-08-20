import pyVFRendering as vfr
import numpy as np
from ovf import ovf

from nanogui import gl, glfw, GLCanvas

class GLWidget(GLCanvas):

    def __init__(self, parent):
        super(GLWidget, self).__init__(parent)

        # Set the size to be equal to Screen
        self.setSize(parent.size())

        # self.system_dimensions = np.array([3, 5, 4])
        # self.nx = self.system_dimensions[0]
        # self.ny = self.system_dimensions[1]
        # self.nz = self.system_dimensions[2]

        # # Create the VFR.geometry
        # n_cells = self.system_dimensions
        # self.geometry = vfr.Geometry.rectilinearGeometry(
            # range(n_cells[0]), range(n_cells[1]), range(n_cells[2]))

        # # Initialize directions
        # directions = []
        # for iz in range(n_cells[2]):
            # for iy in range(n_cells[1]):
                # for ix in range(n_cells[0]):
                    # directions.append([0, 0, 0.5])
        # self.directions = np.array(directions)
        
        testfile = "img_out.ovf"
        
        with ovf.ovf_file(testfile) as ovf_file:
            print("found:      ", ovf_file.found)
            print("is_ovf:     ", ovf_file.is_ovf)
            print("n_segments: ", ovf_file.n_segments)
            segment = ovf.ovf_segment()
            success = ovf_file.read_segment_header(0, segment)
            
            self.system_dimensions = (segment.n_cells[0], segment.n_cells[1], 
                segment.n_cells[2], 3)
            
            self.nx = segment.n_cells[0]
            self.ny = segment.n_cells[1]
            self.nz = segment.n_cells[2]
            self.nos = self.nx * self.ny * self.nz
            # Create the VFR.geometry
            n_cells = self.system_dimensions
            self.geometry = vfr.Geometry.rectilinearGeometry(
                range(n_cells[0]), range(n_cells[1]), range(n_cells[2]))
            
            print("data shape: ", self.system_dimensions)
            self.directions = np.zeros(self.system_dimensions, dtype='f')
            success = ovf_file.read_segment_data(0, segment, self.directions)
        print("----- ovf test reading done")
       
        # Create the VFR.view
        self.view = vfr.View()
        self.view.setFramebufferSize(
            parent.size()[0]*parent.pixelRatio(),
            parent.size()[1]*parent.pixelRatio())

        # Create/Init VFR.vf
        self.vf = vfr.VectorField(self.geometry, 
            self.directions.reshape((self.nos, 3)))

        # Renderers
        self.show_arrows = False
        self.show_dots = False
        self.show_neighbors = False
        self.show_coordinate_system = False
        self.show_cubes = False 
        self.show_bounding_box = False
        self.show_stream_tube = False 

        # Switch on initial renderers
        self.switchArrowsRenderer()
        self.switchCoordinateSystemRenderer()
        self.switchBoundingBoxRenderer()

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
        if index >= self.nos:
            print("Error: Invalid indeces in Neighbor Renderer")
            return

        # turn single index into 3D indeces i,j,k
        i = index % self.nx
        j = ((index - i) // self.nx) % self.ny
        k = (((index - i) // self.nx) - j) // self.ny

        # create a new direction array that represents the neighbor spheres
        directions = [[0, 0, 0] for x in range(self.nos)]

        # set the sphere for the spin tha we are looking at
        index = k*self.nx*self.ny + j*self.nx + i
        directions[index] = cyan_sph

        # set the neighbors
        x_plus = index + 1
        if x_plus < self.nos and x_plus >= 0 and not i == (self.nx-1):
            directions[x_plus] = pink_sph

        x_minus = index - 1
        if x_minus < self.nos and x_minus >= 0 and not i == 0:
            directions[x_minus] = pink_sph

        y_plus = index + self.nx
        if y_plus < self.nos and y_plus >= 0 and not j == (self.ny-1):
            directions[y_plus] = pink_sph

        y_minus = index - self.nx
        if y_minus < self.nos and y_minus >= 0 and not j == 0:
            directions[y_minus] = pink_sph

        z_plus = index + self.nx * self.ny
        if z_plus < self.nos and z_plus >= 0 and not k == (self.nz-1):
            directions[z_plus] = pink_sph

        z_minus = index - self.nx * self.ny
        if z_minus < self.nos and z_minus >= 0 and not k == 0:
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

    def switchStreamtubeRenderer(self):
        if not self.show_stream_tube:
            self.renderer_stream_tube = vfr.StreamTubeRenderer(self.view, 
                                            self.vf)
            positions = self.streamtubeBase()
            self.renderer_stream_tube.seedPositions(positions)
        else:
            self.renderer_stream_tube.seedPositions([])
        self.show_stream_tube = not self.show_stream_tube
        self._setupRenderers()

    def streamtubeCircularSeeds(self):
        midx = (self.system_dimensions[0] - 1) / 2
        midy = (self.system_dimensions[1] - 1) / 2
        num_positions = 16                              # set
        radius = 2                                      # set
        positions = np.zeros(0)
        for i in range(num_positions):
            angle = ( 2 * np.pi * i / num_positions )
            positions = np.append(positions, np.array([midx + radius * np.sin(angle),
                                                       midy + radius * np.cos(angle), 
                                                       self.system_dimensions[2] / 2]))
        return positions.reshape(num_positions,3)

    def streamtubeGridSeeds(self):
        midx = (self.system_dimensions[0] - 1) / 2
        midy = (self.system_dimensions[1] - 1) / 2
        z = self.system_dimensions[2] / 2
        xside, yside = (4, 4)                            # set
        xstep, ystep = (1, 1) # increase by 2 for even side points or by 1 for odd
        nos = xside * yside
        gxx, gyy = np.mgrid[ midx - xstep * (xside - 1) / 2 : 
                             midx + xstep * (xside - 1) / 2 : xside * 1j,
                             midy - ystep * (yside - 1) / 2 : 
                             midy + ystep * (yside - 1) / 2 : yside * 1j ]
        gxx = gxx.reshape(1, nos)
        gyy = gyy.reshape(1, nos)
        gzz = np.full((1, nos), z)
        return np.dstack((gxx, gyy, gzz))[0]

    def setDotRadius(self,size):
        if self.show_dots:
            self.renderer_dots.setDotRadius(size)
            self._setupRenderers()
    
    def getDotStyles(self):
        return [e for e in vfr.DotRendererStyle.__members__]

    def setDotStyle(self, index):
        if self.show_dots: 
            self.renderer_dots.setDotStyle(index) 

    def getStreamTubeBaseStyles(self):
        return ["Circular", "Grid"]

    def setStreamTubeBaseStyle(self, style):
        if style == 0:
            self.streamtubeBase = self.streamtubeCircularSeeds
        elif style == 1:
            self.streamtubeBase = self.streamtubeGridSeeds 
        # if show_stream_tube is True switch off and on the renderer to redraw
        if self.show_stream_tube:
            self.switchStreamtubeRenderer()
            self.switchStreamtubeRenderer()

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
        # self.renderer_cubes.setParallelepipedRotation(False)
        self.show_cubes = not self.show_cubes
        self._setupRenderers()

    def setCubesSize(self,scale):
        if self.show_cubes:
            self.renderer_cubes.setParallelepipedLengthA(scale)
            self.renderer_cubes.setParallelepipedLengthB(scale)
            self.renderer_cubes.setParallelepipedLengthC(scale)
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
        if self.show_stream_tube:
            self.renderers_list.append(self.renderer_stream_tube)
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

