# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configure.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Configure(object):
    def setupUi(self, Configure):
        Configure.setObjectName("Configure")
        Configure.resize(227, 63)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/history-manager.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Configure.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Configure)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.maxHistoryLabel = QtWidgets.QLabel(Configure)
        self.maxHistoryLabel.setObjectName("maxHistoryLabel")
        self.horizontalLayout.addWidget(self.maxHistoryLabel)
        self.maxHistorySB = QtWidgets.QSpinBox(Configure)
        self.maxHistorySB.setMaximum(15000)
        self.maxHistorySB.setSingleStep(25)
        self.maxHistorySB.setProperty("value", 200)
        self.maxHistorySB.setObjectName("maxHistorySB")
        self.horizontalLayout.addWidget(self.maxHistorySB)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Configure)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Configure)
        self.buttonBox.accepted.connect(Configure.accept)
        self.buttonBox.rejected.connect(Configure.reject)
        QtCore.QMetaObject.connectSlotsByName(Configure)

    def retranslateUi(self, Configure):
        _translate = QtCore.QCoreApplication.translate
        Configure.setWindowTitle(_translate("Configure", "Options"))
        self.maxHistoryLabel.setText(_translate("Configure", "Startup Load :"))
        self.maxHistorySB.setSuffix(_translate("Configure", " Operations"))
