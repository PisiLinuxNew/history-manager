#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


import sys
import dbus
from os.path import join

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QLocale, QTranslator
from PyQt5.QtWidgets import QApplication

def main():
    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.pyqt5 import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)


    # Application Stuff
    from libhistorymanager.window import MainManager

    app = QApplication(sys.argv)
    app.setOrganizationName("history-manager")
    app.setApplicationName("history-manager")
    app.setApplicationVersion("0.2.8.0")

    locale = QLocale.system().name()
    translator = QTranslator(app)
    translator.load(join("/usr/share/history-manager", "languages/{}.qm".format(locale)))
    app.installTranslator(translator)

    # Create Main Widget and make some settings
    mainWindow = MainManager(None, app= app)
    mainWindow.show()
    mainWindow.resize(640, 480)
    mainWindow.setWindowIcon(QIcon.fromTheme("view-history"))

    # Create connection for lastWindowClosed signal to quit app
    app.lastWindowClosed.connect(app.quit)

    # Run the applications
    app.exec_()


if __name__ == '__main__':
    main()