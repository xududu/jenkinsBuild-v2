from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox


class UiDialog(QWidget):
    def __init__(self):
        super(UiDialog, self).__init__()
        self.resize(400, 300)
        self.setWindowTitle("UiDialog")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(100, 80, 181, 91))
        self.label.setText("UiDialog")

    def closeEvent(self, QcloseEvent):
        reply = QMessageBox.question(self,
                                     "are you sour?",
                                     "are you sour close?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QcloseEvent.accept()
        else:
            QcloseEvent.ignore()
