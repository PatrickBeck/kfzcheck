from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QDialog):
    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)

        self.setMinimumHeight(400)
        self.setMinimumWidth(400)

        self.layout = QVBoxLayout()

        self.listWidget = QListWidget()

        for x in range(5):

            widget = QWidget()

            layoutWidget = QGridLayout()
            progress = QProgressBar();

            layoutWidget.addWidget(QLabel("Nummer %s" % x), 0, 0)
            layoutWidget.addWidget(QLabel("Randomtext"), 1, 0)

            layoutWidget.addWidget(QPushButton('Mehr'), 0, 2, 2, 1, Qt.AlignRight)

            layoutWidget.setSizeConstraint(QLayout.SetMaximumSize)
            widget.setLayout(layoutWidget)

            self.item = QListWidgetItem()

            self.item.setSizeHint(widget.sizeHint())
            self.listWidget.addItem(self.item)
            self.listWidget.setItemWidget(self.item, widget)

            self.layout.addWidget(self.listWidget)
            self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication([])
    myapp = MainWindow()
    myapp.show()
    app.exec_()

