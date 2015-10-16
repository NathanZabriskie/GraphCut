import sys
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *


class NewCutUI:

    def __init__(self):
        self.a = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.resize(1000, 1000)
        self.window.setWindowTitle("GraphCut")
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

        self.window.show()

        sys.exit(self.a.exec_())

    @pyqtSlot()
    def on_open(self):
        print 'Opening'

    @pyqtSlot()
    def on_save(self):
        print 'Saving'

    @pyqtSlot()
    def on_close(self):
        print 'Closing'
        self.window.close()

if __name__ == "__main__":
    newUI = NewCutUI()