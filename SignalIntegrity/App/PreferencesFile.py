"""
PreferencesFile.py
"""

# Copyright (c) 2018 Teledyne LeCroy, Inc.
# All rights reserved worldwide.
#
# This file is part of SignalIntegrity.
#
# SignalIntegrity is free software: You can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation, either
# version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>
from ProjectFileBase import XMLConfiguration,XMLPropertyDefaultString,XMLPropertyDefaultInt,XMLPropertyDefaultBool
from ProjectFileBase import ProjectFileBase,XMLProperty

import os

class Color(XMLConfiguration):
    def __init__(self,name):
        XMLConfiguration.__init__(self,name)
        self.Add(XMLPropertyDefaultString('Background'))
        self.Add(XMLPropertyDefaultString('Foreground'))
        self.Add(XMLPropertyDefaultString('ActiveBackground'))
        self.Add(XMLPropertyDefaultString('ActiveForeground'))
        self.Add(XMLPropertyDefaultString('DisabledForeground'))
        self.Add(XMLPropertyDefaultString('Plot'))

class Appearance(XMLConfiguration):
    def __init__(self,name):
        XMLConfiguration.__init__(self,name)
        self.Add(XMLPropertyDefaultInt('FontSize',12))
        self.SubDir(Color('Color'))

class Cache(XMLConfiguration):
    def __init__(self,name):
        XMLConfiguration.__init__(self,name)
        self.Add(XMLPropertyDefaultBool('CacheResults',False))

class LastFiles(XMLConfiguration):
    def __init__(self,name):
        XMLConfiguration.__init__(self,name)
        self.Add(XMLPropertyDefaultString('Name'))
        self.Add(XMLPropertyDefaultString('Directory'))

class ProjectFiles(XMLConfiguration):
    def __init__(self,name):
        XMLConfiguration.__init__(self,name)
        self.Add(XMLPropertyDefaultBool('OpenLastFile',True))
        self.Add(XMLPropertyDefaultBool('RetainLastFilesOpened',True))
        self.Add(XMLProperty('LastFile',[LastFiles('LastFiles') for _ in range(4)],'array',LastFiles('LastFiles')))
        self.Add(XMLPropertyDefaultBool('AskToSaveCurrentFile',True))

class OnlineHelp(XMLConfiguration):
    def __init__(self,name):
        XMLConfiguration.__init__(self,name)
        self.Add(XMLPropertyDefaultBool('UseOnlineHelp',True))
        self.Add(XMLPropertyDefaultString('URL','http://teledynelecroy.github.io/SignalIntegrity/SignalIntegrity/App'))
        self.Add(XMLPropertyDefaultBool('RebuildHelpKeys',False))

class PreferencesFile(ProjectFileBase):
    def __init__(self):
        ProjectFileBase.__init__(self)
        self.SubDir(ProjectFiles('ProjectFiles'))
        self.SubDir(Appearance('Appearance'))
        self.SubDir(Cache('Cache'))
        self.SubDir(OnlineHelp('OnlineHelp'))
