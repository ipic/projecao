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
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from openlp.core.common.registry import Registry
from openlp.core.server import Server
from tests.helpers.testmixin import TestMixin


class TestServer(TestCase, TestMixin):
    """
    Test the Server Class used to check if OpenLP is running.
    """
    def setUp(self):
        Registry.create()
        with patch('PyQt5.QtNetwork.QLocalSocket'):
            self.server = Server()

    def tearDown(self):
        self.server.close_server()

    def test_is_another_instance_running(self):
        """
        Run a test as if this was the first time and no instance is running
        """
        # GIVEN: A running Server

        # WHEN: I ask for it to start
        value = self.server.is_another_instance_running()

        # THEN the following is called
        self.server.out_socket.waitForConnected.assert_called_once_with()
        self.server.out_socket.connectToServer.assert_called_once_with(self.server.id)
        assert isinstance(value, MagicMock)

    def test_is_another_instance_running_true(self):
        """
        Run a test as if there is another instance running
        """
        # GIVEN: A running Server
        self.server.out_socket.waitForConnected.return_value = True

        # WHEN: I ask for it to start
        value = self.server.is_another_instance_running()

        # THEN the following is called
        self.server.out_socket.waitForConnected.assert_called_once_with()
        self.server.out_socket.connectToServer.assert_called_once_with(self.server.id)
        assert value is True

    def test_on_read_ready(self):
        """
        Test the on_read_ready method calls the service_manager
        """
        # GIVEN: A server with a service manager
        self.server.in_stream = MagicMock()
        service_manager = MagicMock()
        Registry().register('service_manager', service_manager)

        # WHEN: a file is added to the socket and the method called
        file_name = '\\home\\superfly\\'
        self.server.in_stream.readLine.return_value = file_name
        self.server._on_ready_read()

        # THEN: the service will be loaded
        assert service_manager.load_service.call_count == 1
        service_manager.load_service.assert_called_once_with(Path(file_name))

    @patch("PyQt5.QtCore.QTextStream")
    def test_post_to_server(self, mocked_stream):
        """
        A Basic test with a post to the service
        :return:
        """
        # GIVEN: A server
        # WHEN: I post to a server
        self.server.post_to_server(['l', 'a', 'm', 'a', 's'])

        # THEN: the file should be passed out to the socket
        self.server.out_socket.write.assert_called_once_with(b'lamas')

    @patch("PyQt5.QtCore.QTextStream")
    def test_post_to_server_openlp(self, mocked_stream):
        """
        A Basic test with a post to the service with OpenLP
        :return:
        """
        # GIVEN: A server
        # WHEN: I post to a server
        self.server.post_to_server(['l', 'a', 'm', 'a', 's', 'OpenLP'])

        # THEN: the file should be passed out to the socket
        self.server.out_socket.write.assert_called_once_with(b'lamas')
