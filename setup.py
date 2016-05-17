# -*- coding: utf-8 -*-
#
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# Please read the docs/COPYING file.
#

from setuptools import setup, find_packages
from os import listdir, system


langs = []
for l in listdir('languages'):
    if l.endswith('ts'):
        system('lrelease-qt5 languages/%s' % l)
        langs.append(('languages/%s' % l).replace('.ts', '.qm'))

#system("pyrcc5 resources/data.qrc -o historymanager/data_rc.py")

datas = [('/usr/share/applications', ['history-manager.desktop']),
         ('/usr/share/history-manager/languages', langs)]

setup(
    name = "history-manager",
    version = "0.2.8.0",
    description = u"Pisi Geçmiş Yöneticisi",
    scripts = ["script/history-manager"],
    license = 'GPL V2',
    author = "Pisi Linux Developers",
    author_email = "admin@pisilinux.org",
    url = "https://www.github.com/PisiLinuxNew/history-manager",
    packages=find_packages(),
    data_files=datas,

)
