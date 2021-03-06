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
Test the media plugin
"""
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from PyQt5 import QtCore

from openlp.core.common.settings import Settings
from openlp.plugins.media.lib.mediaitem import MediaMediaItem
from tests.helpers.testmixin import TestMixin


__default_settings__ = {
    'media/media auto start': QtCore.Qt.Unchecked,
    'media/media files': []
}


class MediaItemTest(TestCase, TestMixin):
    """
    Test the media item for Media
    """

    def setUp(self):
        """
        Set up the components need for all tests.
        """
        with patch('openlp.plugins.media.lib.mediaitem.MediaManagerItem.__init__'),\
                patch('openlp.plugins.media.lib.mediaitem.MediaMediaItem.setup'):
            self.media_item = MediaMediaItem(None, MagicMock())
            self.media_item.settings_section = 'media'
        self.setup_application()
        self.build_settings()
        Settings().extend_default_settings(__default_settings__)

    def tearDown(self):
        """
        Clean up after the tests
        """
        self.destroy_settings()

    def test_search_found(self):
        """
        Media Remote Search Successful find
        """
        # GIVEN: The Mediaitem set up a list of media
        Settings().setValue(self.media_item.settings_section + '/media files', [Path('test.mp3'), Path('test.mp4')])
        # WHEN: Retrieving the test file
        result = self.media_item.search('test.mp4', False)
        # THEN: a file should be found
        assert result == [['test.mp4', 'test.mp4']], 'The result file contain the file name'

    def test_search_not_found(self):
        """
        Media Remote Search not find
        """
        # GIVEN: The Mediaitem set up a list of media
        Settings().setValue(self.media_item.settings_section + '/media files', [Path('test.mp3'), Path('test.mp4')])
        # WHEN: Retrieving the test file
        result = self.media_item.search('test.mpx', False)
        # THEN: a file should be found
        assert result == [], 'The result file should be empty'
