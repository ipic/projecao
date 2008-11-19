"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import random
import unittest

import os, os.path
import sys
mypath=os.path.split(os.path.abspath(__file__))[0]
sys.path.insert(0,(os.path.join(mypath, '..', '..','..','..')))

from openlp.plugins.biblemanager.BibleManager import BibleManager
from openlp.utils import ConfigHelper

import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename='plugins.log',
                filemode='w')

console=logging.StreamHandler()
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
log=logging.getLogger('')

logging.info("\nLogging started")

class TestBibleManager:
    log=logging.getLogger("testBibleMgr")
    def setup_class(self):
        log.debug("\n.......Register BM")
        self.bm = BibleManager()

    def testRegisterCSVBibleFiles(self):
        # Register a bible from files
        log.debug("\n.......testRegisterBibleFiles")
        self.bm.registerCSVFileBible("TheMessage",'biblebooks_msg_short.csv','bibleverses_msg_short.csv')
        self.bm.registerCSVFileBible("NIV",'biblebooks_niv_short.csv','bibleverses_niv_short.csv')        
        b = self.bm.getBibles()
        for b1 in b:
            log.debug( b1)
            assert(b1 in b)    
