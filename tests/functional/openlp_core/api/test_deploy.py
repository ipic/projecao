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
import os
import shutil
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase, skip
from unittest.mock import MagicMock, patch

from openlp.core.api.deploy import deploy_zipfile, download_and_check, download_sha256


CONFIG_FILE = '2c266badff1e3d140664c50fd1460a2b332b24d5ad8c267fa62e506b5eb6d894  deploy/site.zip\n2017_06_27'


class TestRemoteDeploy(TestCase):
    """
    Test the Remote plugin deploy functions
    """

    def setUp(self):
        """
        Setup for tests
        """
        self.app_root_path = Path(mkdtemp())

    def tearDown(self):
        """
        Clean up after tests
        """
        shutil.rmtree(self.app_root_path)

    @patch('openlp.core.api.deploy.ZipFile')
    def test_deploy_zipfile(self, MockZipFile):
        """
        Remote Deploy tests - test the dummy zip file is processed correctly
        """
        # GIVEN: A new downloaded zip file
        mocked_zipfile = MagicMock()
        MockZipFile.return_value = mocked_zipfile
        root_path_str = '{sep}tmp{sep}remotes'.format(sep=os.sep)
        root_path = Path(root_path_str)

        # WHEN: deploy_zipfile() is called
        deploy_zipfile(root_path, 'site.zip')

        # THEN: the zip file should have been extracted to the right location
        MockZipFile.assert_called_once_with(Path('/tmp/remotes/site.zip'))
        mocked_zipfile.extractall.assert_called_once_with(Path('/tmp/remotes'))

    @skip('Broken and being refactored')
    @patch('openlp.core.api.deploy.Registry')
    @patch('openlp.core.api.deploy.get_web_page')
    def test_download_sha256_connection_error(self, mocked_get_web_page, MockRegistry):
        """
        Test that if a ConnectionError occurs while downloading a sha256 False is returned
        """
        # GIVEN: A bunch of mocks
        MockRegistry.return_value.get.return_value.applicationVersion.return_value = '1.0'
        mocked_get_web_page.side_effect = ConnectionError()

        # WHEN: download_sha256() is called
        result = download_sha256()

        # THEN: The result should be False
        assert result is False, 'download_sha256() should return False when encountering ConnectionError'

    @skip('Broken and being refactored')
    @patch('openlp.core.api.deploy.Registry')
    @patch('openlp.core.api.deploy.get_web_page')
    def test_download_sha256_no_config(self, mocked_get_web_page, MockRegistry):
        """
        Test that if there's no config when downloading a sha256 None is returned
        """
        # GIVEN: A bunch of mocks
        MockRegistry.return_value.get.return_value.applicationVersion.return_value = '1.0'
        mocked_get_web_page.return_value = None

        # WHEN: download_sha256() is called
        result = download_sha256()

        # THEN: The result should be Nonw
        assert result is None, 'download_sha256() should return None when there is a problem downloading the page'

    @skip('Broken and being refactored')
    @patch('openlp.core.api.deploy.Registry')
    @patch('openlp.core.api.deploy.get_web_page')
    def test_download_sha256(self, mocked_get_web_page, MockRegistry):
        """
        Test that the sha256 and the version are returned
        """
        # GIVEN: A bunch of mocks
        MockRegistry.return_value.get.return_value.applicationVersion.return_value = '1.0'
        mocked_get_web_page.return_value = CONFIG_FILE

        # WHEN: download_sha256() is called
        result = download_sha256()

        # THEN: The result should be Nonw
        assert result == ('2c266badff1e3d140664c50fd1460a2b332b24d5ad8c267fa62e506b5eb6d894', '2017_06_27'), \
            'download_sha256() should return a tuple of sha256 and version'

    @skip('Broken and being refactored')
    @patch('openlp.core.api.deploy.Registry')
    @patch('openlp.core.api.deploy.download_sha256')
    @patch('openlp.core.api.deploy.get_url_file_size')
    @patch('openlp.core.api.deploy.download_file')
    @patch('openlp.core.api.deploy.AppLocation.get_section_data_path')
    @patch('openlp.core.api.deploy.deploy_zipfile')
    def test_download_and_check(self, mocked_deploy_zipfile, mocked_get_data_path, mocked_download_file,
                                mocked_get_url_file_size, mocked_download_sha256, MockRegistry):
        # GIVEN: A bunch of mocks
        mocked_get_data_path.return_value = Path('/tmp/remotes')
        mocked_download_file.return_value = True
        mocked_get_url_file_size.return_value = 5
        mocked_download_sha256.return_value = ('asdfgh', '0.1')
        MockRegistry.return_value.get.return_value.applicationVersion.return_value = '1.0'
        mocked_callback = MagicMock()

        # WHEN: download_and_check() is called
        download_and_check(mocked_callback)

        # THEN: The correct things should have been done
        mocked_download_sha256.assert_called_once_with()
        mocked_get_url_file_size.assert_called_once_with('https://get.openlp.org/webclient/site.zip')
        mocked_callback.setRange.assert_called_once_with(0, 5)
        mocked_download_file.assert_called_once_with(mocked_callback, 'https://get.openlp.org/webclient/site.zip',
                                                     Path('/tmp/remotes/site.zip'), sha256='asdfgh')
        mocked_deploy_zipfile.assert_called_once_with(Path('/tmp/remotes'), 'site.zip')
