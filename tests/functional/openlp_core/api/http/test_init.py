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
Functional tests to test the Http init.
"""
from unittest import TestCase
from unittest.mock import MagicMock

from openlp.core.api.http import authenticate, check_auth, requires_auth
from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from tests.helpers.testmixin import TestMixin


class TestInit(TestCase, TestMixin):
    """
    A test suite to test the functions on the init
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry().create()
        Registry().register('service_list', MagicMock())
        self.build_settings()
        self.password = 'c3VwZXJmbHk6bGFtYXM='

    def tearDown(self):
        self.destroy_settings()

    def test_auth(self):
        """
        Test the check_auth method with a match
        :return:
        """
        # GIVEN: a known user
        Settings().setValue('api/user id', "superfly")
        Settings().setValue('api/password', "lamas")

        # WHEN : I check the authorisation
        is_valid = check_auth(['aaaaa', self.password])

        # THEN:
        assert is_valid is True

    def test_auth_falure(self):
        """
        Test the check_auth method with a match
        :return:
        """
        # GIVEN: a known user
        Settings().setValue('api/user id', 'superfly')
        Settings().setValue('api/password', 'lamas')

        # WHEN : I check the authorisation
        is_valid = check_auth(['aaaaa', 'monkey123'])

        # THEN:
        assert is_valid is False

    def test_requires_auth_disabled(self):
        """
        Test the requires_auth wrapper with disabled security
        :return:
        """
        # GIVEN: A disabled security
        Settings().setValue('api/authentication enabled', False)

        # WHEN: I call the function
        wrapped_function = requires_auth(func)
        value = wrapped_function()

        # THEN: the result will be as expected
        assert value == 'called'

    def test_requires_auth_enabled(self):
        """
        Test the requires_auth wrapper with enabled security
        :return:
        """
        # GIVEN: A disabled security
        Settings().setValue('api/authentication enabled', True)

        # WHEN: I call the function
        wrapped_function = requires_auth(func)
        req = MagicMock()
        value = wrapped_function(req)

        # THEN: the result will be as expected
        assert str(value) == str(authenticate())

    def test_requires_auth_enabled_auth_error(self):
        """
        Test the requires_auth wrapper with enabled security and authorization taken place and and error
        :return:
        """
        # GIVEN: A enabled security
        Settings().setValue('api/authentication enabled', True)

        # WHEN: I call the function with the wrong password
        wrapped_function = requires_auth(func)
        req = MagicMock()
        req.authorization = ['Basic', 'cccccccc']
        value = wrapped_function(req)

        # THEN: the result will be as expected - try again
        assert str(value) == str(authenticate())

    def test_requires_auth_enabled_auth(self):
        """
        Test the requires_auth wrapper with enabled security and authorization taken place and and error
        :return:
        """
        # GIVEN: An enabled security and a known user
        Settings().setValue('api/authentication enabled', True)
        Settings().setValue('api/user id', 'superfly')
        Settings().setValue('api/password', 'lamas')

        # WHEN: I call the function with the wrong password
        wrapped_function = requires_auth(func)
        req = MagicMock()
        req.authorization = ['Basic', self.password]
        value = wrapped_function(req)

        # THEN: the result will be as expected - try again
        assert str(value) == 'called'

    def test_requires_auth_missing_credentials(self):
        """
        Test the requires_auth wrapper with enabled security and authorization taken place and and error
        :return:
        """
        # GIVEN: An enabled security and a known user
        Settings().setValue('api/authentication enabled', True)
        Settings().setValue('api/user id', 'superfly')
        Settings().setValue('api/password', 'lamas')

        # WHEN: I call the function with no password
        wrapped_function = requires_auth(func)
        value = wrapped_function(0)

        # THEN: the result will be as expected (unauthorized)
        assert str(value) == str(authenticate())


def func(field=None):
    return 'called'
