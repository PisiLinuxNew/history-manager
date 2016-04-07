#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui_uiitem import Ui_HistoryItemWidget


class HistoryItem(QListWidgetItem):
    def __init__(self, parent, no):
        QListWidgetItem.__init__(self, parent)

        self.no = no

    def __lt__(self, other):
        return int(self.no) < int(other.no)

class NewOperation(QWidget):
    def __init__(self, operation, parent=None):
        super(NewOperation, self).__init__(parent)

        opttrans = {"upgrade":self.tr("Upgrade"), "remove":self.tr("Removal"), "emerge":self.tr("Emerge"), \
                    "install":self.tr("Installation"), "snapshot":self.tr("Snapshot"), "takeback":self.tr("Takeback"), \
                    "repoupdate":self.tr("Repository Update")}

        self.parent = parent
        self.ui = Ui_HistoryItemWidget()
        self.ui.setupUi(self)
        self.settings = QSettings()

        self.toggled = False
        self.toggleButtons()

        self.op_no = operation[0]
        self.op_type = operation[1]
        self.op_date = operation[2]
        self.op_time = operation[3]
        self.op_pack = operation[4]
        self.op_repo = operation[5]

        self.alias = " - ".join([self.op_date, self.op_time])
        self.op_pack_len = len(self.op_pack)

        self.icon = ":/pics/%s.png" % self.op_type

        if self.settings.contains("%d/label" % self.op_no):
            self.alias = str(self.settings.value("%d/label" % self.op_no))

        self.ui.labelLabel.setText(self.alias)

        self.ui.typeLabel.setText(self.tr("No: %s   Type: %s")%(self.op_no, self.tr(opttrans[self.op_type])))
        self.ui.iconLabel.setPixmap(QPixmap(self.icon))

        self.ui.restorePB.clicked.connect(self.parent.takeBack)
        self.ui.detailsPB.clicked.connect(self.parent.loadDetails)
        self.ui.planPB.clicked.connect(self.parent.loadPlan)

    def setAlias(self, txt):
        self.alias = txt
        self.settings.setValue("%d/label" % self.op_no, QVariant(self.alias))
        self.ui.labelLabel.setText(self.alias)

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.ui.planPB.setVisible(toggle)
        self.ui.restorePB.setVisible(toggle)
        self.ui.detailsPB.setVisible(toggle)

