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
Package to test the openlp.core.lib package.
"""
from unittest import TestCase
from unittest.mock import MagicMock

from openlp.core.common.registry import Registry, RegistryBase


class TestRegistry(TestCase):

    def test_registry_service(self):
        """
        Test the registry creation and its usage
        """
        # GIVEN: A new registry
        Registry.create()

        # WHEN: I add a component it should save it
        mock_1 = MagicMock()
        Registry().register('test1', mock_1)

        # THEN: we should be able retrieve the saved component
        assert Registry().get('test1') == mock_1, 'The saved service can be retrieved and matches'

        # WHEN: I add a component for the second time I am mad.
        # THEN  and I will get an exception
        with self.assertRaises(KeyError) as context:
            Registry().register('test1', mock_1)
        assert context.exception.args[0] == 'Duplicate service exception test1', \
            'KeyError exception should have been thrown for duplicate service'

        # WHEN I try to get back a non existent component
        # THEN I will get an exception
        temp = Registry().get('test2')
        assert temp is None, 'None should have been returned for missing service'

        # WHEN I try to replace a component I should be allowed
        Registry().remove('test1')
        # THEN I will get an exception
        temp = Registry().get('test1')
        assert temp is None, 'None should have been returned for deleted service'

    def test_registry_function(self):
        """
        Test the registry function creation and their usages
        """
        # GIVEN: An existing registry register a function
        Registry.create()
        Registry().register_function('test1', self.dummy_function_1)

        # WHEN: I execute the function
        return_value = Registry().execute('test1')

        # THEN: I expect then function to have been called and a return given
        assert return_value[0] == 'function_1', 'A return value is provided and matches'

        # WHEN: I execute the a function with the same reference and execute the function
        Registry().register_function('test1', self.dummy_function_1)
        return_value = Registry().execute('test1')

        # THEN: I expect then function to have been called and a return given
        assert return_value == ['function_1', 'function_1'], 'A return value list is provided and matches'

        # WHEN: I execute the a 2nd function with the different reference and execute the function
        Registry().register_function('test2', self.dummy_function_2)
        return_value = Registry().execute('test2')

        # THEN: I expect then function to have been called and a return given
        assert return_value[0] == 'function_2', 'A return value is provided and matches'

    def test_registry_working_flags(self):
        """
        Test the registry working flags creation and its usage
        """
        # GIVEN: A new registry
        Registry.create()

        # WHEN: I add a working flag it should save it
        my_data = 'Lamas'
        my_data2 = 'More Lamas'
        Registry().set_flag('test1', my_data)

        # THEN: we should be able retrieve the saved component
        temp = Registry().get_flag('test1')
        assert temp == my_data, 'The value should have been saved'

        # WHEN: I add a component for the second time I am not mad.
        # THEN  and I will not get an exception
        Registry().set_flag('test1', my_data2)
        temp = Registry().get_flag('test1')
        assert temp == my_data2, 'The value should have been updated'

        # WHEN I try to get back a non existent Working Flag
        # THEN I will get an exception
        with self.assertRaises(KeyError) as context1:
            temp = Registry().get_flag('test2')
        assert context1.exception.args[0] == 'Working Flag test2 not found in list', \
            'KeyError exception should have been thrown for missing working flag'

        # WHEN I try to replace a working flag I should be allowed
        Registry().remove_flag('test1')
        # THEN I will get an exception
        with self.assertRaises(KeyError) as context:
            temp = Registry().get_flag('test1')
        assert context.exception.args[0] == 'Working Flag test1 not found in list', \
            'KeyError exception should have been thrown for duplicate working flag'

    def test_remove_function(self):
        """
        Test the remove_function() method
        """
        # GIVEN: An existing registry register a function
        Registry.create()
        Registry().register_function('test1', self.dummy_function_1)

        # WHEN: Remove the function.
        Registry().remove_function('test1', self.dummy_function_1)

        # THEN: The method should not be available.
        assert Registry().functions_list['test1'] == [], 'The function should not be in the dict anymore.'

    def dummy_function_1(self):
        return "function_1"

    def dummy_function_2(self):
        return "function_2"


class PlainStub(object):
    def __init__(self):
        pass


class RegistryStub(RegistryBase):
    def __init__(self):
        super().__init__()


class TestRegistryBase(TestCase):

    def test_registry_mixin_missing(self):
        """
        Test the registry creation and its usage
        """
        # GIVEN: A new registry
        Registry.create()

        # WHEN: I create an instance of a class that doesn't inherit from RegistryMixin
        PlainStub()

        # THEN: Nothing is registered with the registry
        assert len(Registry().functions_list) == 0, 'The function should not be in the dict anymore.'

    def test_registry_mixin_present(self):
        """
        Test the registry creation and its usage
        """
        # GIVEN: A new registry
        Registry.create()

        # WHEN: I create an instance of a class that inherits from RegistryMixin
        RegistryStub()

        # THEN: The bootstrap methods should be registered
        assert len(Registry().functions_list) == 3, 'The bootstrap functions should be in the dict.'
