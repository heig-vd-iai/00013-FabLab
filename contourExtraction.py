#!/usr/bin/env python
#
# ------------------------------------------------------------------------------
# Project: Fablab
#
# ------------------------------------------------------------------------------
#
# contourExtraction.py
#
# 2020-01-09 / Jean DEMEUSY
#
# ------------------------------------------------------------------------------
# *** to enter the environment ***
#
# > cd 'D:\Bureau\MakerSpace\_Python\'
# > ..\pyFablab\Scripts\activate
#
# ------------------------------------------------------------------------------
# *** to compile the .ui file
#
# > pyuic mainWindow.ui -o mainWindow.py
# ------------------------------------------------------------------------------
# *** to run the program ***
#
# > py contourExtraction.py
#
# ------------------------------------------------------------------------------
#
# This software implements ............. with the following methods :
# - ..........
# - ..........
#
# ## Import external libraries
# This application uses the following libraries :
# - ... for ...,
# - ... for ...
#
# ------------------------------------------------------------------------------
# installed libraries
#
# > pip(3) install numpy
# > pip(3) install ezdxf
# > pip(3) install opencv-python
# > pip(3) install matplotlib
# > pip(3) install scipy
# > pip(3) install PyQt5
# > pip(3) install pyqtgraph
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

from PyQt5.QtWidgets import QApplication
from mainWindowClass import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = MainWindow('MakerSpace Tools Extraction')
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
