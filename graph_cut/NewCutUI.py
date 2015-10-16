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
        self.foregroundButton = QPushButton('Add Foreground Seeds')
        self.foregroundButton.clicked.connect(self.on_foreground)
        self.foregroundButton.setStyleSheet("background-color: gray")

        self.backGroundButton = QPushButton('Add Background Seeds')
        self.backGroundButton.clicked.connect(self.on_background)
        self.backGroundButton.setStyleSheet("background-color: white")

        clearButton = QPushButton('Clear All Seeds')
        clearButton.clicked.connect(self.on_clear)

        segmentButton = QPushButton('Segment Image')
        segmentButton.clicked.connect(self.on_segment)

        buttonLayout.addWidget(self.foregroundButton)
        buttonLayout.addWidget(self.backGroundButton)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(segmentButton)
        buttonLayout.addStretch()
        ##

        mainBox.addLayout(buttonLayout)

        # Setup Image Area ##
        imageLayout = QHBoxLayout()

        self.seedLabel = QLabel()
        self.seedLabel.setPixmap(QPixmap.fromImage(
            self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.seeds))))
        self.seedLabel.mousePressEvent = self.mouse_down
        self.seedLabel.mouseMoveEvent = self.mouse_drag

        self.segmentLabel = QLabel()
        self.segmentLabel.setPixmap(QPixmap.fromImage(
            self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.segmented))))

        imageLayout.addWidget(self.seedLabel)
        imageLayout.addWidget(self.segmentLabel)
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
    def get_qimage(cvimage):
        height, width, bytes_per_pix = cvimage.shape
        bytes_per_line = width * bytes_per_pix;
        cv2.cvtColor(cvimage, cv2.COLOR_BGR2RGB, cvimage)
        return QImage(cvimage.data, width, height, QImage.Format_RGB888)

    @pyqtSlot()
    def on_foreground(self):
        self.seed_num = self.graph_maker.foreground
        self.foregroundButton.setStyleSheet("background-color: gray")
        self.backGroundButton.setStyleSheet("background-color: white")

    @pyqtSlot()
    def on_background(self):
        self.seed_num = self.graph_maker.background
        self.foregroundButton.setStyleSheet("background-color: white")
        self.backGroundButton.setStyleSheet("background-color: gray")

    @pyqtSlot()
    def on_clear(self):
        self.graph_maker.clear_seeds()
        self.seedLabel.setPixmap(QPixmap.fromImage(
                self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.seeds))))

    @pyqtSlot()
    def on_segment(self):
        self.graph_maker.create_graph()
        self.segmentLabel.setPixmap(QPixmap.fromImage(
            self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.segmented))))

    @pyqtSlot()
    def on_open(self):
        f = QFileDialog.getOpenFileName()
        if f is not None and f != "":
            self.graph_maker.load_image(str(f))
            self.seedLabel.setPixmap(QPixmap.fromImage(
                self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.seeds))))
            self.segmentLabel.setPixmap(QPixmap.fromImage(
                self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.segmented))))


    @pyqtSlot()
    def on_save(self):
        f = QFileDialog.getSaveFileName()
        print 'Saving'
        if f is not None and f != "":
            self.graph_maker.save_image(f)

    @pyqtSlot()
    def on_close(self):
        print 'Closing'
        self.window.close()

    def mouse_down(self, event):
        self.graph_maker.add_seed(event.x(), event.y(), self.seed_num)
        self.seedLabel.setPixmap(QPixmap.fromImage(
                self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.seeds))))

    def mouse_drag(self, event):
        self.graph_maker.add_seed(event.x(), event.y(), self.seed_num)
        self.seedLabel.setPixmap(QPixmap.fromImage(
                self.get_qimage(self.graph_maker.get_image_with_overlay(self.graph_maker.seeds))))

if __name__ == "__main__":
    newUI = NewCutUI()
    newUI.run()
