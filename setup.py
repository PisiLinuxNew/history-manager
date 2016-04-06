#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import glob
import shutil
import sys

from code.historymanager import about

from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install

PROJECT = about.appName

def makeDirs(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

def remove(path):
    if os.path.exists(path):
        print ' removing: ', path
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

class Build(build):
    def run(self):
        # Clear all
        os.system("rm -rf build")

        # Copy codes
        print "Copying PYs..."
        os.system("cp -R code/ build/")

        # Copy icons
        print "Copying Images..."
        os.system("cp -R resources/ build/")

        print "Generating RCs..."
        for filename in glob.glob1("resources", "*.qrc"):
            os.system("pyrcc5 resources/%s -o build/%s_rc.py" % (filename, filename.split(".")[0]))


        for language in glob.glob1("languages", "*.ts"):
            print language
            os.system("lrelease-qt5 languages/%s"%language)

            # Copy languages
        print "Copying Languages File..."
        os.system("cp -R languages/ build/")

class Install(install):
    def run(self):
        install.run(self)


        root_dir = "/usr/share"
        bin_dir = "/usr/bin"
            
        pixmap_dir = os.path.join(root_dir, "pixmap")

        apps_dir = os.path.join(root_dir, "applications")
        project_dir = os.path.join(root_dir, PROJECT)

        # Make directories
        print "Making directories..."
        makeDirs(bin_dir)
        makeDirs(apps_dir)
        makeDirs(pixmap_dir)
        makeDirs(project_dir)
            
         # Install desktop files
        print "Installing desktop files..."

        shutil.copy("resources/%s.desktop" % PROJECT, apps_dir)

        shutil.copy("resources/icons/%s.png" % PROJECT, pixmap_dir)

        shutil.rmtree('build/resources')
        
        # Install codes
        print "Installing codes..."
        os.system("cp -R build/* %s/" % project_dir)

        os.chmod("script/history-manager", 0755)
        shutil.copy("script/history-manager", "/usr/bin")


setup(
        name = PROJECT,
        version = about.version,
        description = unicode(about.PACKAGE),
        scripts = ["script/history-manager"],
        license = unicode('GPL V2'),
        author = "Pisi Linux Developers",
        author_email = about.bugEmail,
        url = about.homePage,
        cmdclass          = {
                            'build': Build,
                            'install': Install,
                          }
)
