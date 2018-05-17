#!/usr/bin/env python3

import sys

# Make sure to find pyVFRendering
# This is only needed if you did not install the package
#
# import os
# pyVFRenderingDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../vfrendering_iff/build"))
# sys.path.insert(0, pyVFRenderingDir)

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
