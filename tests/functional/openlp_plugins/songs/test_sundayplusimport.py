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
This module contains tests for the SundayPlus song importer.
"""
from unittest.mock import patch

from tests.helpers.songfileimport import SongImportTestHelper
from tests.utils.constants import RESOURCE_PATH


TEST_PATH = RESOURCE_PATH / 'songs' / 'sundayplus'


class TestSundayPlusFileImport(SongImportTestHelper):

    def __init__(self, *args, **kwargs):
        self.importer_class_name = 'SundayPlusImport'
        self.importer_module_name = 'sundayplus'
        super(TestSundayPlusFileImport, self).__init__(*args, **kwargs)

    def test_song_import(self):
        """
        Test that loading an SundayPlus file works correctly on various files
        """
        with patch('openlp.plugins.songs.lib.importers.sundayplus.retrieve_windows_encoding') as \
                mocked_retrieve_windows_encoding:
            mocked_retrieve_windows_encoding.return_value = 'cp1252'
            self.file_import([TEST_PATH / 'Amazing Grace.ptf'],
                             self.load_external_result_data(TEST_PATH / 'Amazing Grace.json'))
