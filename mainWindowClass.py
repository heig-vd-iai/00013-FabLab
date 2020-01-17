from ImageClass import Image
from GeometricClass import Point, Line
from FileClass import File
from mainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import pyqtgraph as pg
import numpy as np

class MainWindow(QMainWindow):
    real_length = np.array([429, 349]) # mm
    pxl_length = np.array([2200, 1800]) # px
    scale = real_length / pxl_length

    def __init__(self,title):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(title)

        self.ref = None
        self.img = None
        self.tform = None
        self.fname = None
        self.list = None

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground(None)
        self.graphWidget.hideAxis('left')
        self.graphWidget.setAspectLocked(True, 1)
        self.ui.chartFrame.layout().addWidget(self.graphWidget)

        self.ui.cali_load.clicked.connect(self.getCalibrationImage)
        self.ui.analysis_load.clicked.connect(self.getAnalysisImage)
        self.ui.get_tform.clicked.connect(self.getTForm)
        self.ui.analyse.clicked.connect(self.analyseImage)
        self.ui.export_button.clicked.connect(self.exportToDXF)

    def getCalibrationImage(self):
        try:
            QImg, self.ref = self.getQPixmap()
        except:
            pass
        else:
            self.ui.calibrationDisplay.setPixmap(QPixmap(QImg))

            self.ui.cali_s_label.setText('Image({self.height},{self.width})'.format(self=self.ref))
            self.ui.cali_tform_success.setText('tform: Not run yet')
            self.ui.cali_tform_success.setStyleSheet('color: red')

            self.resetQPixamp(self.ui.rawImageDisplay)
            self.resetQPixamp(self.ui.resultImageDisplay)

    def getAnalysisImage(self):
        try:
            QImg, self.img = self.getQPixmap()
        except:
            pass
        else:
            self.ui.rawImageDisplay.setPixmap(QPixmap(QImg))

            self.ui.analysis_s_label.setText('Image({self.height},{self.width})'.format(self=self.img))
            self.ui.analysis_result.setText('#px: ')

            self.resetQPixamp(self.ui.resultImageDisplay)
            self.graphWidget.plot([0],[0],clear=True)

    def getQPixmap(self, fromBrowser = True):
        if fromBrowser:
            fname, _ = QFileDialog.getOpenFileName(self, 'Open file', \
                'path/to/file',"Image files (*.png)")
        else:
            fname = '../imagePlaceholder.png'

        img = Image(file = fname)

        w, h = img.width, img.height
        QImg = QImage(img.data.data, w, h, w, QImage.Format_Indexed8)

        return QImg, img

    def getTForm(self):
        assert(isinstance(self.ref,Image))

        try:
            self.tform, self.corners = self.ref.image2tform(Point(2200,1800))
        except:
            self.ui.cali_tform_success.setText('tform: error occured')
            self.ui.cali_tform_success.setStyleSheet('color: red')
        else:
            self.ui.cali_tform_success.setText('tform: computed')
            self.ui.cali_tform_success.setStyleSheet('color: green')

    def analyseImage(self):
        self.list, img = self.img.image2list(self.tform, self.corners, MainWindow.scale)

        w, h = img.width, img.height
        QImg = QImage(img.data.data, w, h, w, QImage.Format_Indexed8)

        pen = pg.mkPen(color=(0,0,0), width=4)
        pen.setCapStyle(Qt.RoundCap)
        self.graphWidget.plot(self.list[:,0], self.list[:,1],pen=pen,clear=True)

        self.ui.resultImageDisplay.setPixmap(QPixmap(QImg))
        self.ui.analysis_result.setText('#px: {}'.format(len(self.list)))
        self.ui.export_button.setEnabled(True)

    def exportToDXF(self):
        f_dxf = self.img.file.toDXF()
        f_dxf.fillDXF(self.list)

    def resetQPixamp(self, label):
        QImg, _ = self.getQPixmap(False)
        label.setPixmap(QPixmap(QImg))
