# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sun Aug  1 15:46:03 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_KFZcheck(object):
    def setupUi(self, KFZcheck):
        KFZcheck.setObjectName("KFZcheck")
        KFZcheck.resize(800, 454)
        KFZcheck.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.mainwidget = QtGui.QWidget(KFZcheck)
        self.mainwidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.mainwidget.setObjectName("mainwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.mainwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listfield = QtGui.QListWidget(self.mainwidget)
        self.listfield.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.listfield.setObjectName("listfield")
        self.verticalLayout.addWidget(self.listfield)
        self.searchfield = QtGui.QLineEdit(self.mainwidget)
        self.searchfield.setToolTip("")
        self.searchfield.setStatusTip("")
        self.searchfield.setWhatsThis("")
        self.searchfield.setAccessibleName("")
        self.searchfield.setAutoFillBackground(False)
        self.searchfield.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.searchfield.setInputMask("")
        self.searchfield.setText("")
        self.searchfield.setObjectName("searchfield")
        self.verticalLayout.addWidget(self.searchfield)
        KFZcheck.setCentralWidget(self.mainwidget)
        self.menubar = QtGui.QMenuBar(KFZcheck)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuKFZcheck = QtGui.QMenu(self.menubar)
        self.menuKFZcheck.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.menuKFZcheck.setTitle("KFZcheck")
        self.menuKFZcheck.setObjectName("menuKFZcheck")
        KFZcheck.setMenuBar(self.menubar)
        self.actionMiddle = QtGui.QAction(KFZcheck)
        self.actionMiddle.setCheckable(True)
        self.actionMiddle.setObjectName("actionMiddle")
        self.actionTop = QtGui.QAction(KFZcheck)
        self.actionTop.setCheckable(True)
        self.actionTop.setObjectName("actionTop")
        self.actionBottom = QtGui.QAction(KFZcheck)
        self.actionBottom.setCheckable(True)
        self.actionBottom.setObjectName("actionBottom")
        self.actionCountry = QtGui.QAction(KFZcheck)
        self.actionCountry.setObjectName("actionCountry")
        self.actionAbout = QtGui.QAction(KFZcheck)
        self.actionAbout.setObjectName("actionAbout")
        self.menuKFZcheck.addAction(self.actionTop)
        self.menuKFZcheck.addAction(self.actionMiddle)
        self.menuKFZcheck.addAction(self.actionBottom)
        self.menuKFZcheck.addAction(self.actionCountry)
        self.menuKFZcheck.addAction(self.actionAbout)
        self.menubar.addAction(self.menuKFZcheck.menuAction())

        self.retranslateUi(KFZcheck)
        QtCore.QMetaObject.connectSlotsByName(KFZcheck)

    def retranslateUi(self, KFZcheck):
        KFZcheck.setWindowTitle(QtGui.QApplication.translate("KFZcheck", "KFZcheck", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMiddle.setText(QtGui.QApplication.translate("KFZcheck", "Middle", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTop.setText(QtGui.QApplication.translate("KFZcheck", "Top", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBottom.setText(QtGui.QApplication.translate("KFZcheck", "Bottom", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCountry.setText(QtGui.QApplication.translate("KFZcheck", "Country", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("KFZcheck", "About", None, QtGui.QApplication.UnicodeUTF8))

