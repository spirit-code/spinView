#!/usr/bin/env python3

# Make sure to find pyVFRendering, nanogui and ovf if manually built
# This is only needed if you did not install the package
#
# import sys
# import os
# pyVFRenderingDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "VFRendering/build/Release"))
# sys.path.insert(0, pyVFRenderingDir)
# nanoguiDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "nanogui/build/Release/python"))
# sys.path.insert(0, nanoguiDir)
# nanoguiDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "ovf/python"))
# sys.path.insert(0, nanoguiDir)

import nanogui
import gc

from ui.main_window import MainWindow

if __name__ == '__main__':
    nanogui.init()
    win = MainWindow(800, 600)
    win.setVisible(True)
    nanogui.mainloop(refresh=1000)
    del win
    gc.collect
    nanogui.shutdown()