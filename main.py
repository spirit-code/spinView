#!/usr/bin/env python3

import sys

# Make sure to find pyVFRendering
# This is only needed if you did not install the package
#
# import os
# pyVFRenderingDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../vfrendering_iff/build"))
# sys.path.insert(0, pyVFRenderingDir)

import nanogui
import random
import math
import time
import gc

import pyVFRendering as vfr
import numpy as np

from nanogui import Color, Screen, Window, GroupLayout, BoxLayout, \
    ToolButton, Label, Button, Widget, \
    PopupButton, CheckBox, MessageDialog, VScrollPanel, \
    ImagePanel, ImageView, ComboBox, ProgressBar, Slider, \
    TextBox, ColorWheel, Graph, GridLayout, \
    Alignment, Orientation, TabWidget, TabHeader, IntBox, GLShader, GLCanvas

from nanogui import gl, glfw, entypo


class glWidget(GLCanvas):

    def __init__(self, parent):
        super(glWidget, self).__init__(parent)

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
                    directions.append([0, 0, 0.6])
        self.directions = np.array(directions)

        # Create the VFR.view
        self.view = vfr.View()
        self.view.setFramebufferSize(
            parent.size()[0]*parent.pixelRatio(),
            parent.size()[1]*parent.pixelRatio())

        # Create/Init VFR.vf
        self.vf = vfr.VectorField(self.geometry, directions)

        # Renderers
        self.show_arrows = False
        self.show_neighbors = False
        self.show_coordinate_system = False

        # Switch On initial renderers
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
        j = ((index-i)//self.nx) % self.ny
        k = (((index-i)//self.nx) - j) // self.ny

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

    def switchArrowsRenderer(self):
        # Create arrow renderer with VFR.view and VFR.vf
        self.renderer_arrows = vfr.ArrowRenderer(self.view, self.vf)
        self.show_arrows = not self.show_arrows
        self._setupRenderers()

    def _setupRenderers(self):
        self.renderers_list = []
        if self.show_arrows:
            self.renderers_list.append(self.renderer_arrows)
        if self.show_neighbors:
            self.renderers_list.append(self.renderer_neighbors)
        # combine renderers
        renderers_system = vfr.CombinedRenderer(
            self.view, self.renderers_list)
        renderers = [(renderers_system, [0.0, 0.0, 1.0, 1.0])]
        # add the coordinate system
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


class MainWindow(Screen):
    def __init__(self, height, width):
        super(MainWindow, self).__init__((height, width), "NanoGUI Test")

        # GL canvas
        self.gl_canvas = glWidget(self)

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

        def cb(state):
            self.gl_canvas.switchArrowsRenderer()
        chb = CheckBox(window, "Arrows", cb)
        chb.setChecked(True)

        def cb(state):
            self.gl_canvas.switchCoordinateSystemRenderer()
        chb = CheckBox(window, "Coordinates", cb)
        chb.setChecked(True)

        def cb(state):
            print("Not implemented!")
        chb = CheckBox(window, "ArrowsSphere", cb)

        def update_cb(state):
            self.gl_canvas.drawNeighbors(intBox.value()-1)

        def switch_cb(state):
            self.gl_canvas.switchNeighborRenderer(intBox.value()-1)
        chb = CheckBox(window, "Neighbors", switch_cb)
        intBox = IntBox(window)
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
        intBox.setCallback(update_cb)

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


if __name__ == '__main__':
    nanogui.init()
    win = MainWindow(800, 600)
    # win.drawAll()
    win.setVisible(True)
    nanogui.mainloop(refresh=1000)
    del win
    gc.collect
    nanogui.shutdown()
