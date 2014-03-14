# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2014 Raoul Snyman                                        #
# Portions copyright (c) 2008-2014 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
Package to test the openlp.core.ui package.
"""
from unittest import TestCase

from PyQt4 import QtCore, QtGui, QtTest

from openlp.core.common import Registry
from openlp.core.ui import servicenoteform
from tests.interfaces import patch


class TestStartNoteDialog(TestCase):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        old_app_instance = QtCore.QCoreApplication.instance()
        if old_app_instance is None:
            self.app = QtGui.QApplication([])
        else:
            self.app = old_app_instance
        self.main_window = QtGui.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = servicenoteform.ServiceNoteForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def basic_display_test(self):
        """
        Test Service Note form functionality
        """
        # GIVEN: A dialog with an empty text box
        self.form.text_edit.setPlainText('')

        # WHEN displaying the UI and pressing enter
        with patch('PyQt4.QtGui.QDialog.exec_'):
            self.form.exec_()
        ok_widget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following input text is returned
        self.assertEqual(self.form.text_edit.toPlainText(), '', 'The returned text should be empty')

        # WHEN displaying the UI, having set the text and pressing enter
        text = 'OpenLP is the best worship software'
        self.form.text_edit.setPlainText(text)
        with patch('PyQt4.QtGui.QDialog.exec_'):
            self.form.exec_()
        ok_widget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following text is returned
        self.assertEqual(self.form.text_edit.toPlainText(), text, 'The text originally entered should still be there')

        # WHEN displaying the UI, having set the text and pressing enter
        self.form.text_edit.setPlainText('')
        with patch('PyQt4.QtGui.QDialog.exec_'):
            self.form.exec_()
            self.form.text_edit.setPlainText(text)
        okWidget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(okWidget, QtCore.Qt.LeftButton)

        # THEN the following text is returned
        self.assertEqual(self.form.text_edit.toPlainText(), text, 'The new text should be returned')

