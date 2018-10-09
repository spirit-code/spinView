import pyVFRendering as vfr
import numpy as np
from ovf import ovf
from nanogui import gl, glfw, GLCanvas

from renderers.general import CoordinateSystemRenderer, BoundingBoxRenderer, \
     NeighborsRenderer
from renderers.vectorfield import ArrowsRenderer, CubesRenderer, DotsRenderer, \
    StreamTubeRenderer


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
        self.arrows = ArrowsRenderer(self.view, self.vf) 
        self.dots = DotsRenderer(self.view, self.vf) 
       
        # TODO: FIX
        # self.show_neighbors = False
        self.neighbors = NeighborsRenderer(self.view, self.geometry, self.system_dimensions) 
        
        self.coordinate = CoordinateSystemRenderer(self.view)
        self.cubes = CubesRenderer(self.view, self.vf) 
        self.bounding_box = BoundingBoxRenderer(self.view, self.geometry, self.system_dimensions) 
        self.streamtubes = StreamTubeRenderer(self.view, self.vf, self.system_dimensions)

        # Switch on initial renderers
        self.arrows.switch() 
        self.coordinate.switch() 
        self.bounding_box.switch()

        self.updateRenderers()

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

    def updateRenderers(self):
        self.renderers_list = []
        if self.arrows.show:
            self.renderers_list.append(self.arrows.renderer)
        if self.dots.show:
            self.renderers_list.append(self.dots.renderer)
        if self.neighbors.show:
            self.renderers_list.append(self.neighbors.renderer)
        if self.bounding_box.show:
            self.renderers_list.append(self.bounding_box.renderer)
        if self.cubes.show:
            self.renderers_list.append(self.cubes.renderer)
        if self.streamtubes.show:
            self.renderers_list.append(self.streamtubes.renderer)
        # combine renderers
        renderers_system = vfr.CombinedRenderer(
            self.view, self.renderers_list)
        renderers = [(renderers_system, [0.0, 0.0, 1.0, 1.0])]
        # last add the coordinate system renderer
        if self.coordinate.show:
            renderers.append((self.coordinate.renderer, self.coordinate.position))
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

