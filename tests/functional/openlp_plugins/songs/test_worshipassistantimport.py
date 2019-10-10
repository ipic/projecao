# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2019 OpenLP Developers                              #
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
The :mod:`worshipassistantimport` module provides the functionality for importing
WorshipAssistant song files into the current installation database.
"""
from tests.helpers.songfileimport import SongImportTestHelper
from tests.utils.constants import RESOURCE_PATH


TEST_PATH = RESOURCE_PATH / 'songs' / 'worshipassistant'


class TestWorshipAssistantFileImport(SongImportTestHelper):

    def __init__(self, *args, **kwargs):
        self.importer_class_name = 'WorshipAssistantImport'
        self.importer_module_name = 'worshipassistant'
        super(TestWorshipAssistantFileImport, self).__init__(*args, **kwargs)

    def test_song_import(self):
        """
        Test that loading an Worship Assistant file works correctly
        """
        self.file_import(TEST_PATH / 'du_herr.csv', self.load_external_result_data(TEST_PATH / 'du_herr.json'))
        self.file_import(TEST_PATH / 'would_you_be_free.csv',
                         self.load_external_result_data(TEST_PATH / 'would_you_be_free.json'))
        self.file_import(TEST_PATH / 'would_you_be_free2.csv',
                         self.load_external_result_data(TEST_PATH / 'would_you_be_free.json'))
