# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2020 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Package to test the openlp.core.ui package.
"""
from unittest import TestCase
from unittest.mock import patch

from PyQt5 import QtCore, QtTest, QtWidgets

from openlp.core.common.registry import Registry
from openlp.core.ui import servicenoteform
from tests.helpers.testmixin import TestMixin


class TestStartNoteDialog(TestCase, TestMixin):

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = servicenoteform.ServiceNoteForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def test_basic_display(self):
        """
        Test Service Note form functionality
        """
        # GIVEN: A dialog with an empty text box
        self.form.text_edit.setPlainText('')

        # WHEN displaying the UI and pressing enter
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
        ok_widget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following input text is returned
        assert self.form.text_edit.toPlainText() == '', 'The returned text should be empty'

        # WHEN displaying the UI, having set the text and pressing enter
        text = 'OpenLP is the best worship software'
        self.form.text_edit.setPlainText(text)
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
        ok_widget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following text is returned
        assert self.form.text_edit.toPlainText() == text, 'The text originally entered should still be there'

        # WHEN displaying the UI, having set the text and pressing enter
        self.form.text_edit.setPlainText('')
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
            self.form.text_edit.setPlainText(text)
        ok_widget = self.form.button_box.button(self.form.button_box.Save)
        QtTest.QTest.mouseClick(ok_widget, QtCore.Qt.LeftButton)

        # THEN the following text is returned
        assert self.form.text_edit.toPlainText() == text, 'The new text should be returned'
