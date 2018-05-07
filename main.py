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

        # Create the VFR.geometry
        n_cells = [20, 20, 20]
        self.geometry = vfr.Geometry.rectilinearGeometry(
            range(n_cells[0]), range(n_cells[1]), range(n_cells[2]))

        # Initialize directions
        directions = []
        for iz in range(n_cells[2]):
            for iy in range(n_cells[1]):
                for ix in range(n_cells[0]):
                    directions.append([0, 0, 1])
        directions = np.array(directions)

        # Create the VFR.view
        self.view = vfr.View()
        self.view.setFramebufferSize( 
            parent.size()[0]*parent.pixelRatio(), 
            parent.size()[1]*parent.pixelRatio())

        # Create/Init VFR.vf
        self.vf = vfr.VectorField(self.geometry, directions)

        # Create arrow renderer with VFR.view and VFR.vf
        self.renderer_arrows = vfr.ArrowRenderer(self.view, self.vf)
        
        # Added the renderer_arrows to view renderers
        self.renderers = [(self.renderer_arrows, [0.0, 0.0, 1.0, 1.0])]
        self.view.renderers(self.renderers, False)

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
        self.previous_mouse_position = [0,0]
        
    def drawGL(self):
        gl.Enable(gl.DEPTH_TEST)
        self.view.draw() 
        gl.Disable(gl.DEPTH_TEST)

    def scrollEvent(self,p,rel):
        scale = 3
        self.view.mouseScroll(rel[1] * scale )
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

    def setNeighborVisualization(self):
        self.renderer_neighbors = vfr.SphereRenderer(self.view, self.vf)
        self.renderers.append((self.renderer_neighbors,[0.0, 0.0, 1.0, 1.0]))
        self.view.renderers(self.renderers, False)

    def mouseButtonEvent(self,p,button,down,modifiers):
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

        # Window Alpha
        window_a = Window(self, "alpha")
        window_a.setFixedSize((200*self.pixelRatio(), 200*self.pixelRatio()))
        window_a.setPosition((5, 30))
        window_a.setLayout(GroupLayout())

        buttons = window_a.buttonPanel()

        # Minimize/Maximize
        b_a_minmax = Button(buttons, "", icon=entypo.ICON_CHEVRON_DOWN)

        def cb():
            height = window_a.height()
            if height == 30:
                window_a.setHeight(300)
            else:
                window_a.setHeight(30)
            b_a_minmax.setPushed(not b_a_minmax.pushed())
        b_a_minmax.setCallback(cb)

        # Close
        b_a_close = Button(buttons, "", icon=entypo.ICON_CIRCLE_WITH_CROSS)

        def cb():
            window_a.dispose()
        b_a_close.setCallback(cb)

        # Buttons
        Label(window_a, "Push buttons", "sans-bold")
        b = Button(window_a, "Plain button")

        def cb():
            print("pushed!")
        b.setCallback(cb)

        b = Button(window_a, "Styled", entypo.ICON_ROCKET)
        b.setBackgroundColor(Color(0, 0, 1.0, 0.1))
        b.setCallback(cb)

        # Window Renderers
        window_renderers = Window(self, "Renderers")
        window_renderers.setFixedSize((200*self.pixelRatio(), 150*self.pixelRatio()))
        window_renderers.setPosition((5, 235))
        window_renderers.setLayout(GroupLayout())
       
        def mouseDragEvent(window_renderers):
            pass

        def cb(state):
            print("Not implemented!")
        chb = CheckBox(window_renderers,"Arrows",cb) 
        
        def cb(state):
            print("Not implemented!")
        chb = CheckBox(window_renderers,"Coordinates",cb) 
       
        def cb(state):
            print("Not implemented!")
        chb = CheckBox(window_renderers,"ArrowsSphere",cb) 
        
        def cb(state):
            print("Not implemented!")
        chb = CheckBox(window_renderers,"Neighbors",cb) 
        
        buttons = window_renderers.buttonPanel()

        # Minimize/Maximize
        b_b_minmax = Button(buttons, "", icon=entypo.ICON_CHEVRON_DOWN)

        def cb():
            height = window_renderers.height()
            if height == 30:
                window_renderers.setHeight(300)
            else:
                window_renderers.setHeight(30)
            b_b_minmax.setPushed(not b_b_minmax.pushed())
        b_b_minmax.setCallback(cb)

        # Close
        b_b_close = Button(buttons, "", icon=entypo.ICON_CIRCLE_WITH_CROSS)

        def cb():
            window_renderers.dispose()
        b_b_close.setCallback(cb)

        # # Tab widget
        # tw = TabWidget(self)
        # tw.setPosition((-20,300))
        # twtest = tw.createTab("tab test")
        # tw.addTab("tab 0",twtest)
        # tw.addTab("tab 2",twtest)
        # tw.setFixedSize((200*self.pixelRatio(),300*self.pixelRatio()))

        self.performLayout()

    def draw(self, ctx):
        super(MainWindow, self).draw(ctx)

    def drawContents(self):
        self.gl_canvas.view.draw()
        super(MainWindow, self).drawContents()

    def keyboardEvent(self, key, scancode, action, modifiers):
        if super(MainWindow, self).keyboardEvent(key, scancode,
                                                 action, modifiers):
            return True
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.setVisible(False)
            return True
        if key == glfw.KEY_S:
            self.gl_canvas.setNeighborVisualization()
            return True
        return False
    
    def resizeEvent(self,size):
        super(MainWindow,self).resizeEvent(size)
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

