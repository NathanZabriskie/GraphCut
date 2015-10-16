import sys
import cv2
import numpy as np
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
from graph_cut import GraphMaker

class NewCutUI:

    def __init__(self):
        self.graph_maker = GraphMaker.GraphMaker()
        self.a = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("GraphCut")
        self.seed_num = self.graph_maker.foreground

        # Setup file menu
        mainMenu = self.window.menuBar()
        fileMenu = mainMenu.addMenu('&File')

        openButton = QAction(QIcon('exit24.png'), 'Open Image', self.window)
        openButton.setShortcut('Ctrl+O')
        openButton.setStatusTip('Open a file for segmenting.')
        openButton.triggered.connect(self.on_open)
        fileMenu.addAction(openButton)

        saveButton = QAction(QIcon('exit24.png'), 'Save Image', self.window)
        saveButton.setShortcut('Ctrl+S')
        saveButton.setStatusTip('Save file to disk.')
        saveButton.triggered.connect(self.on_save)
        fileMenu.addAction(saveButton)

        closeButton = QAction(QIcon('exit24.png'), 'Exit', self.window)
        closeButton.setShortcut('Ctrl+Q')
        closeButton.setStatusTip('Exit application')
        closeButton.triggered.connect(self.on_close)
        fileMenu.addAction(closeButton)

        # Setup main widget #
        mainWidget = QWidget()
        mainBox = QVBoxLayout()

        # Setup Mode Buttons ##
        buttonLayout = QHBoxLayout()
        foregroundButton = QPushButton('Add Foreground Seeds')
        foregroundButton.clicked.connect(self.on_foreground)

        backGroundButton = QPushButton('Add Background Seeds')
        backGroundButton.clicked.connect(self.on_background)

        clearButton = QPushButton('Clear All Seeds')
        clearButton.clicked.connect(self.on_clear)

        segmentButton = QPushButton('See Current Segmentation')
        segmentButton.clicked.connect(self.on_segment)

        buttonLayout.addWidget(foregroundButton)
        buttonLayout.addWidget(backGroundButton)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(segmentButton)
        buttonLayout.addStretch()
        ##

        mainBox.addLayout(buttonLayout)

        # Setup Image Area ##
        imageLayout = QHBoxLayout()
        parms = self.get_qimage_parms(self.graph_maker.get_image_with_overlay(self.graph_maker.seeds))

        self.seedLabel = QLabel()
        self.seedLabel.setPixmap(QPixmap.fromImage(QImage(parms[0], parms[1], parms[2], parms[3])))

        parms = self.get_qimage_parms(self.graph_maker.get_image_with_overlay(self.graph_maker.segmented))
        self.overlayLabel = QLabel()
        self.overlayLabel.setPixmap(QPixmap.fromImage(QImage(parms[0], parms[1], parms[2], parms[3])))

        imageLayout.addWidget(self.seedLabel)
        imageLayout.addWidget(self.overlayLabel)
        imageLayout.addStretch()
        mainBox.addLayout(imageLayout)
        ##
        mainBox.addStretch()
        mainWidget.setLayout(mainBox)
        #
        self.window.setCentralWidget(mainWidget)

    def run(self):
        self.window.show()
        sys.exit(self.a.exec_())

    @staticmethod
    def get_qimage_parms(cvimage):
        height, width, bytes_per_pix = cvimage.shape
        bytes_per_line = width * bytes_per_pix;
        cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB, cvimage)
        return cvimage.data, width, height, QImage.Format_RGB888

    @pyqtSlot()
    def on_foreground(self):
        self.seed_num = self.graph_maker.foreground

    @pyqtSlot()
    def on_background(self):
        self.seed_num = self.graph_maker.background

    @pyqtSlot()
    def on_clear(self):
        self.graph_maker.clear_seeds()

    @pyqtSlot()
    def on_segment(self):
        print 'Segmenting'

    @pyqtSlot()
    def on_open(self):
        filename = QFileDialog.getOpenFileName()
        print filename + "f"

    @pyqtSlot()
    def on_save(self):
        print 'Saving'

    @pyqtSlot()
    def on_close(self):
        print 'Closing'
        self.window.close()

if __name__ == "__main__":
    newUI = NewCutUI()
    newUI.run()
