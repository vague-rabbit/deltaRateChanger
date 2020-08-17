# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Programming\Python\taikosomething\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(766, 93)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pathLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.pathLineEdit.setGeometry(QtCore.QRect(10, 10, 691, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pathLineEdit.setFont(font)
        self.pathLineEdit.setObjectName("pathLineEdit")
        self.chooseDirectoryButton = QtWidgets.QPushButton(self.centralwidget)
        self.chooseDirectoryButton.setGeometry(QtCore.QRect(710, 9, 51, 33))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.chooseDirectoryButton.setFont(font)
        self.chooseDirectoryButton.setObjectName("chooseDirectoryButton")
        self.changeRateButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeRateButton.setGeometry(QtCore.QRect(140, 39, 71, 33))
        self.changeRateButton.setCheckable(True)
        self.changeRateButton.setObjectName("changeRateButton")
        self.rateDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.rateDoubleSpinBox.setGeometry(QtCore.QRect(65, 40, 70, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rateDoubleSpinBox.setFont(font)
        self.rateDoubleSpinBox.setMinimum(0.5)
        self.rateDoubleSpinBox.setMaximum(2.0)
        self.rateDoubleSpinBox.setSingleStep(0.01)
        self.rateDoubleSpinBox.setProperty("value", 1.0)
        self.rateDoubleSpinBox.setObjectName("rateDoubleSpinBox")
        self.rateLabel = QtWidgets.QLabel(self.centralwidget)
        self.rateLabel.setGeometry(QtCore.QRect(8, 44, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rateLabel.setFont(font)
        self.rateLabel.setObjectName("rateLabel")
        self.bpmLabel = QtWidgets.QLabel(self.centralwidget)
        self.bpmLabel.setGeometry(QtCore.QRect(220, 44, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bpmLabel.setFont(font)
        self.bpmLabel.setObjectName("bpmLabel")
        self.bpmSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.bpmSpinBox.setGeometry(QtCore.QRect(279, 40, 70, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bpmSpinBox.setFont(font)
        self.bpmSpinBox.setMaximum(1000)
        self.bpmSpinBox.setObjectName("bpmSpinBox")
        self.changeBpmButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeBpmButton.setGeometry(QtCore.QRect(352, 39, 71, 33))
        self.changeBpmButton.setCheckable(True)
        self.changeBpmButton.setObjectName("changeBpmButton")
        self.pitchCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.pitchCheckBox.setGeometry(QtCore.QRect(430, 39, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pitchCheckBox.setFont(font)
        self.pitchCheckBox.setObjectName("pitchCheckBox")
        self.adjustCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.adjustCheckBox.setGeometry(QtCore.QRect(570, 39, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.adjustCheckBox.setFont(font)
        self.adjustCheckBox.setChecked(True)
        self.adjustCheckBox.setObjectName("adjustCheckBox")
        self.changeBpmButton.raise_()
        self.changeRateButton.raise_()
        self.bpmLabel.raise_()
        self.bpmSpinBox.raise_()
        self.rateDoubleSpinBox.raise_()
        self.pathLineEdit.raise_()
        self.chooseDirectoryButton.raise_()
        self.rateLabel.raise_()
        self.adjustCheckBox.raise_()
        self.pitchCheckBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 766, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "★Rate Changer★ Xtreme δ Deluxx Edition v1.77c Final (fix incl.)"))
        self.chooseDirectoryButton.setText(_translate("MainWindow", "..."))
        self.changeRateButton.setText(_translate("MainWindow", "Create"))
        self.rateLabel.setText(_translate("MainWindow", "Rate:"))
        self.bpmLabel.setText(_translate("MainWindow", "BPM:"))
        self.changeBpmButton.setText(_translate("MainWindow", "Create"))
        self.pitchCheckBox.setText(_translate("MainWindow", "Nightcore?"))
        self.adjustCheckBox.setText(_translate("MainWindow", "Adjust AR/OD"))