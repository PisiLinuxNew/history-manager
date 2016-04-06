#!/usr/bin/python
# -*- coding: utf-8 -*-


from PyQt5 import QtCore
from PyQt5 import QtWidgets

# Application Stuff
from ui_uiitem import Ui_HistoryItemWidget
from ui_configure import Ui_Configure
from ui_mainwindow import Ui_MainManager

from interface import *

SHOW, HIDE     = 0, 1
TARGET_HEIGHT  = 0
ANIMATION_TIME = 200
DEFAULT_HEIGHT = 16777215


class MainManager(QtWidgets.QWidget):
    def __init__(self, parent, standAlone=True, app=None):
        super(MainManager, self).__init__(parent)

        self.ui = Ui_MainManager()
        self.app = app

        if standAlone:
            self.ui.setupUi(self)
            self.parent = self
        else:
            self.ui.setupUi(parent)
            self.parent = parent

        self.settings = QtCore.QSettings()

        self.animator = QTimeLine(ANIMATION_TIME, self)
        self.lastAnimation = SHOW

        self.tweakUi()

        self.last_item = None
        self.checkMsgClicks = False

        self.cface = ComarIface()
        self.pface = PisiIface(self)
        self.config = ConfigWindow(self)
        self.loaded = 0

        self.connectSignals()

        self.ui.textEdit.installEventFilter(self)
        self.ui.lw.installEventFilter(self)
        self.ui.opTypeLabel.installEventFilter(self)

        self.cface.listen(self.handler)
        self.pface.start()

    def connectSignals(self):
        self.pface.loadFetched.connect(self.loadHistory)

        self.animator.frameChanged.connect(self.animate)
        self.animator.finished.connect(self.animateFinished)
        self.ui.newSnapshotPB.clicked.connect(self.takeSnapshot)
        self.ui.buttonCancelMini.clicked.connect(self.hideEditBox)
        self.ui.aliasLE.textEdited.connect(self.setAlias)
        self.ui.configurePB.clicked.connect(self.showConfig)

    def showConfig(self):
        self.config.show()

    def loadHistory(self, num):
        map(self.addNewOperation, self.pface.ops.values()[self.loaded:num])

        self.loaded = num
        self.status(self.tr("%s Operations Loaded")%self.loaded)
        self.checkMsgClicks = True

    def setAlias(self, txt):
        if self.last_item:
            self.last_item.setAlias(txt)

    def tweakUi(self):
        self.ui.lw.clear()
        self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
        self.ui.progressBar.hide()

    def animate(self, height):
        self.ui.editBox.setMaximumHeight(height)
        self.ui.lw.setMaximumHeight(self.parent.height()-height)
        self.update()

    def animateFinished(self):
        if self.lastAnimation == SHOW:
            self.ui.editBox.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.lw.setMaximumHeight(TARGET_HEIGHT)
            self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        elif self.lastAnimation == HIDE:
            self.ui.lw.setFocus()
            self.ui.lw.setMaximumHeight(DEFAULT_HEIGHT)
            self.ui.editBox.setMaximumHeight(TARGET_HEIGHT)
            self.ui.lw.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def hideEditBox(self):
        if self.lastAnimation == SHOW:
            self.lastAnimation = HIDE
            self.hideScrollBars()
            self.animator.setFrameRange(self.ui.editBox.height(), TARGET_HEIGHT)
            self.animator.start()
            self.ui.textEdit.clear()
            self.ui.editGroup.setTitle("")

    def hideScrollBars(self):
        self.ui.editBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.lw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def loadDetails(self):
        self.status(self.tr("Loading operation details.."))

        self.ui.textEdit.clear()
        item = self.sender().parent()
        self.last_item = item

        self.ui.editGroup.setTitle(self.tr("Details for operation on %s at %s")%(item.op_date, item.op_time))

        self.ui.aliasLE.setText(unicode(item.ui.labelLabel.text()))

        message = ""
        if item.op_type == "snapshot":
            message += self.tr("There are %s packages in this snapshot.")%item.op_pack_len
        elif item.op_type == "repoupdate":
            for val in item.op_repo:
                message += "- %s\n" % val
        else:
            for val in item.op_pack:
                message += "- %s\n" % val

        self.ui.textEdit.setText(message)

        self.lastAnimation = SHOW
        self.hideScrollBars()

        self.animator.setFrameRange(TARGET_HEIGHT, self.parent.height() - TARGET_HEIGHT)
        self.animator.start()

        self.status(self.tr("Ready .."))

    def addNewOperation(self, op):
        item = HistoryItem(self.ui.lw, op[0])
        item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
        item.setSizeHint(QSize(38,48))
        self.ui.lw.setItemWidget(item, NewOperation(op, self))
        self.ui.lw.sortItems(Qt.DescendingOrder)

    def loadPlan(self):
        self.status(self.tr("Loading Operation Plan"))

        self.ui.textEdit.clear()
        self.lastAnimation = SHOW
        self.hideScrollBars()

        item = self.sender().parent()
        self.last_item = item

        self.app.processEvents()

        willbeinstalled, willberemoved = self.pface.historyPlan(item.op_no)

        information = ""
        if item.op_type == "snapshot":
            configs = self.pface.historyConfigs(item.op_no)
            if configs and len(configs) != 0:
                information += self.tr("Configuration files in snapshot:")
                for i in configs.keys():
                    information += "<br><br><b> %s </b><br>" % i
                    for j in configs.get(i):
                        information += "%s \n" % ("/".join(j.split(str(item.op_no),1)[1].split(i,1)[1:]))
        message = ""

        if willbeinstalled and len(willbeinstalled) != 0:
            message += self.tr("<br> These package(s) will be <b>installed</b> :<br>")
            for i in range(len(willbeinstalled)):
                message += "%s <br>" % willbeinstalled[i]

        if willberemoved and len(willberemoved) != 0:
            message += self.tr("<br> These package(s) will be <b>removed</b> :<br>")
            for i in range(len(willberemoved)):
                message += "%s <br>" % willberemoved[i]

        message += "<br>"

        self.ui.editGroup.setTitle(self.tr("Takeback plan for Operation on %s at %s")%(item.op_date, item.op_time))
        self.ui.textEdit.setText(message+information)

        self.animator.setFrameRange(TARGET_HEIGHT, self.parent.height() - TARGET_HEIGHT)
        self.animator.start()

        self.status(self.tr("Ready .."))

    def status(self, txt):
        if self.ui.progressBar.isVisible():
            self.ui.progressBar.setFormat(txt)
            self.ui.opTypeLabel.hide()
        else:
            self.ui.opTypeLabel.setText(txt)
            self.ui.opTypeLabel.show()

        self.checkMsgClicks = False

    def takeLastOperation(self):
        self.pface.deinit()
        return self.pface.getLastOperation()

    def takeBack(self):
        willbeinstalled, willberemoved = None, None

        item = self.sender().parent()

        try:
            willbeinstalled, willberemoved = self.pface.historyPlan(item.op_no)
        except ValueError:
            return

        reply = QtWidgets.QMessageBox.warning(self, self.tr("Takeback operation verification"),
            self.tr("<center>This will restore your system back to : <b>%s</b> - <b>%s</b><br>")%(item.op_date, item.op_time) + \
            self.tr("If you're unsure, click Cancel and see TakeBack Plan.</center>"),
             QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

        if reply == QtWidgets.QMessageBox.Ok:
            self.status(self.tr("Taking back to : %s"%item.op_date))
            self.enableButtons(False)

            self.app.processEvents()
            self.cface.takeBack(item.op_no)

    def takeSnapshot(self):
        reply = QtWidgets.QMessageBox.question(self, self.tr("Start new snapshot"),
            self.tr("<center>This will take a snapshot of your system.<br>Click Ok when you're ready.</center>"),
                                QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

        if reply == QtWidgets.QMessageBox.Cancel:
            return

        self.status(self.tr("Taking New Snapshot"))
        self.enableButtons(False)

        try:
            self.app.processEvents()
            self.cface.takeSnap()
        except:
            self.status(self.tr("Authentication Failed"))
            self.enableButtons(True)

    def handler(self, package, signal, args):
        if signal == "status":
            self.status(" ".join(args))
        elif signal == "finished":
            self.status(self.tr("Finished succesfully"))
            self.addNewOperation( self.takeLastOperation() )
            self.enableButtons(True)
        elif signal == "progress":
            self.status(self.tr("Taking Snapshot : <b>%s</b>/100")%args[1])
            self.enableButtons(False)

    def closeEvent(self, event=None):
        self.saveConfig()
        if self.pface.isRunning():
            self.pface.quit()
            # self.pface.wait()

        if event != None:
            event.accept()

    def saveConfig(self):
        self.settings.setValue("pos", QtCore.QVariant(self.mapToGlobal(self.parent.pos())))
        self.settings.setValue("size", QtCore.QVariant(self.parent.size()))
        self.settings.sync()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Hide:
            self.closeEvent()
            return True

        return QtCore.QObject.eventFilter(self, obj, event)

    def enableButtons(self, true):
        self.ui.newSnapshotPB.setEnabled(true)

class ConfigWindow(QtWidgets.QDialog):
    def __init__(self, parent):
        super(ConfigWindow, self).__init__(parent)

        self.ui = Ui_Configure()
        self.ui.setupUi(self)
        self.settings = QtCore.QSettings()
        self.resetConfig()

        self.accepted.connect(self.saveConfig)
        self.rejected.connect(self.resetConfig)

    def saveConfig(self):
        self.settings.setValue("maxhistory", self.ui.maxHistorySB.value())

    def resetConfig(self):
        self.ui.maxHistorySB.setValue(int(self.settings.value("maxhistory", 100)))
