"""
    Package to test the openlp.core.lib package.
"""
import os
import cPickle
from unittest import TestCase
from mock import MagicMock, patch

from openlp.core.lib import ItemCapabilities, ServiceItem, Registry


VERSE = u'The Lord said to {r}Noah{/r}: \n'\
        'There\'s gonna be a {su}floody{/su}, {sb}floody{/sb}\n'\
        'The Lord said to {g}Noah{/g}:\n'\
        'There\'s gonna be a {st}floody{/st}, {it}floody{/it}\n'\
        'Get those children out of the muddy, muddy \n'\
        '{r}C{/r}{b}h{/b}{bl}i{/bl}{y}l{/y}{g}d{/g}{pk}'\
        'r{/pk}{o}e{/o}{pp}n{/pp} of the Lord\n'
FOOTER = [u'Arky Arky (Unknown)', u'Public Domain', u'CCLI 123456']

TEST_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), u'..', u'..', u'resources'))


class TestServiceItem(TestCase):

    def setUp(self):
        """
        Set up the Registry
        """
        Registry.create()
        mocked_renderer = MagicMock()
        mocked_renderer.format_slide.return_value = [VERSE]
        Registry().register(u'renderer', mocked_renderer)
        Registry().register(u'image_manager', MagicMock())

    def serviceitem_basic_test(self):
        """
        Test the Service Item - basic test
        """
        # GIVEN: A new service item

        # WHEN:A service item is created (without a plugin)
        service_item = ServiceItem(None)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.missing_frames() is True, u'There should not be any frames in the service item'

    def serviceitem_add_text_test(self):
        """
        Test the Service Item - add text test
        """
        # GIVEN: A new service item
        service_item = ServiceItem(None)

        # WHEN: adding text to a service item
        service_item.add_from_text(VERSE)
        service_item.raw_footer = FOOTER

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.missing_frames() is False, u'check frames loaded '

        # WHEN: Render called
        assert len(service_item._display_frames) == 0, u'A blank Service Item with no display frames'
        service_item.render(True)

        # THEN: We should have a page of output.
        assert len(service_item._display_frames) == 1, u'A valid rendered Service Item has 1 display frame'
        assert service_item.get_rendered_frame(0) == VERSE.split(u'\n')[0], u'A output has rendered correctly.'

    def serviceitem_add_image_test(self):
        """
        Test the Service Item - add image test
        """
        # GIVEN: A new service item and a mocked renderer
        service_item = ServiceItem(None)
        service_item.name = u'test'

        # WHEN: adding image to a service item
        test_image = os.path.join(TEST_PATH, u'church.jpg')
        service_item.add_from_image(test_image, u'Image Title')

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert len(service_item._display_frames) == 0, u'The service item has no display frames'

        # THEN: We should have a page of output.
        assert len(service_item._raw_frames) == 1, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == test_image

        # WHEN: adding a second image to a service item
        service_item.add_from_image(test_image, u'Image1 Title')

        # THEN: We should have an increased page of output.
        assert len(service_item._raw_frames) == 2, u'A valid rendered Service Item has display frames'
        assert service_item.get_rendered_frame(0) == test_image
        assert service_item.get_rendered_frame(0) == service_item.get_rendered_frame(1)

        # WHEN requesting a saved service item
        service = service_item.get_service_repr(True)

        # THEN: We should have two parts of the service.
        assert len(service) == 2, u'A saved service has two parts'
        assert service[u'header'][u'name'] == u'test', u'A test plugin was returned'
        assert service[u'data'][0][u'title'] == u'Image Title', u'The first title name matches the request'
        assert service[u'data'][0][u'path'] == test_image, u'The first image name matches'
        assert service[u'data'][0][u'title'] != service[u'data'][1][u'title'], \
            u'The individual titles should not match'
        assert service[u'data'][0][u'path'] == service[u'data'][1][u'path'], u'The file paths should match'

        # WHEN validating a service item
        service_item.validate_item([u'jpg'])

        # THEN the service item should be valid
        assert service_item.is_valid is True, u'The new service item should be valid'

        # WHEN: adding a second image to a service item
        service_item.add_from_image(u'resources/church1.jpg', u'Image1 Title')

        # WHEN validating a service item
        service_item.validate_item([u'jpg'])

        # THEN the service item should be valid
        assert service_item.is_valid is False, u'The service item is not valid due to validation changes'

    def serviceitem_add_command_test(self):
        """
        Test the Service Item - add command test
        """
        # GIVEN: A new service item and a mocked renderer
        service_item = ServiceItem(None)
        service_item.name = u'test'

        # WHEN: adding image to a service item
        test_file = os.path.join(TEST_PATH, u'church.jpg')
        service_item.add_from_command(TEST_PATH, u'church.jpg', test_file)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert len(service_item._display_frames) == 0, u'The service item has no display frames '

        # THEN: We should have a page of output.
        assert len(service_item._raw_frames) == 1, u'A valid rendered Service Item has one raw frame'
        assert service_item.get_rendered_frame(0) == test_file, u'The image matches the input'

        # WHEN requesting a saved service item
        service = service_item.get_service_repr(True)

        # THEN: We should have two parts of the service.
        assert len(service) == 2, u'A saved service has two parts'
        assert service[u'header'][u'name'] == u'test', u'A test plugin'
        assert service[u'data'][0][u'title'] == u'church.jpg', u'The first title name '
        assert service[u'data'][0][u'path'] == TEST_PATH, u'The first image name'
        assert service[u'data'][0][u'image'] == test_file, u'The first image name'

        # WHEN validating a service item
        service_item.validate_item([u'jpg'])

        # THEN the service item should be valid
        assert service_item.is_valid is True, u'The service item should be valid'

        # WHEN validating a service item with a different suffix
        service_item.validate_item([u'png'])

        # THEN the service item should not be valid
        assert service_item.is_valid is False, u'The service item is not valid'

    def serviceitem_load_custom_from_service_test(self):
        """
        Test the Service Item - adding a custom slide from a saved service
        """
        # GIVEN: A new service item and a mocked add icon function
        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding a custom from a saved Service
        line = self.convert_file_service_item(u'serviceitem_custom_1.osd')
        service_item.set_from_service(line)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert len(service_item._display_frames) == 0, u'The service item has no display frames'
        assert len(service_item.capabilities) == 5, u'There are 5 default custom item capabilities'
        service_item.render(True)
        assert service_item.get_display_title() == u'Test Custom', u'The custom title should be correct'
        assert service_item.get_frames()[0][u'text'] == VERSE[:-1], \
            u'The original text has been returned except the last line feed'
        assert service_item.get_rendered_frame(1) == VERSE.split(u'\n', 1)[0], u'The first line has been returned'
        assert service_item.get_frame_title(0) == u'Slide 1', u'The title of the first slide is returned'
        assert service_item.get_frame_title(1) == u'Slide 2', u'The title of the second slide is returned'
        assert service_item.get_frame_title(2) == u'', u'The title of the first slide is returned'

    def serviceitem_load_image_from_service_test(self):
        """
        Test the Service Item - adding an image from a saved service
        """
        # GIVEN: A new service item and a mocked add icon function
        image_name = u'image_1.jpg'
        test_file = os.path.join(TEST_PATH, image_name)
        frame_array = {u'path': test_file, u'title': image_name}

        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding an image from a saved Service and mocked exists
        line = self.convert_file_service_item(u'serviceitem_image_1.osd')
        with patch('os.path.exists'):
            service_item.set_from_service(line, TEST_PATH)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        print service_item.get_rendered_frame(0)
        assert service_item.get_rendered_frame(0) == test_file, u'The first frame is the path to the image'
        assert service_item.get_frames()[0] == frame_array, u'The first frame array is as expected'
        assert service_item.get_frame_path(0) == test_file, u'The frame path is the full path to the image'
        assert service_item.get_frame_title(0) == image_name, u'The frame title is the image name'
        assert service_item.get_display_title() == image_name, u'The display title is the first image name'
        assert service_item.is_image() is True, u'This is an image service item'
        assert service_item.is_capable(ItemCapabilities.CanMaintain) is True, u'Images can be Maintained'
        assert service_item.is_capable(ItemCapabilities.CanPreview) is True, u'Images can be Previewed'
        assert service_item.is_capable(ItemCapabilities.CanLoop) is True, u'Images can be made to Loop'
        assert service_item.is_capable(ItemCapabilities.CanAppend) is True, u'Images can have new items added'

    def serviceitem_load_image_from_local_service_test(self):
        """
        Test the Service Item - adding an image from a saved local service
        """
        # GIVEN: A new service item and a mocked add icon function
        image_name1 = u'image_1.jpg'
        image_name2 = u'image_2.jpg'
        test_file1 = os.path.join(u'/home/openlp', image_name1)
        test_file2 = os.path.join(u'/home/openlp', image_name2)
        frame_array1 = {u'path': test_file1, u'title': image_name1}
        frame_array2 = {u'path': test_file2, u'title': image_name2}

        service_item = ServiceItem(None)
        service_item.add_icon = MagicMock()

        # WHEN: adding an image from a saved Service and mocked exists
        line = self.convert_file_service_item(u'serviceitem_image_2.osd')
        with patch('os.path.exists'):
            service_item.set_from_service(line)

        # THEN: We should get back a valid service item
        assert service_item.is_valid is True, u'The new service item should be valid'
        assert service_item.get_rendered_frame(0) == test_file1, u'The first frame is the path to the image'
        assert service_item.get_rendered_frame(1) == test_file2, u'The Second frame is the path to the image'
        assert service_item.get_frames()[0] == frame_array1, u'The first frame array is as expected'
        assert service_item.get_frames()[1] == frame_array2, u'The first frame array is as expected'
        assert service_item.get_frame_path(0) == test_file1, u'The frame path is the full path to the image'
        assert service_item.get_frame_path(1) == test_file2, u'The frame path is the full path to the image'
        assert service_item.get_frame_title(0) == image_name1, u'The 1st frame title is the image name'
        assert service_item.get_frame_title(1) == image_name2, u'The 2nd frame title is the image name'

        assert service_item.get_display_title().lower() == service_item.name, \
            u'The display title as there are > 1 Images'
        assert service_item.is_image() is True, u'This is an image service item'
        assert service_item.is_capable(ItemCapabilities.CanMaintain) is True, u'Images can be Maintained'
        assert service_item.is_capable(ItemCapabilities.CanPreview) is True, u'Images can be Previewed'
        assert service_item.is_capable(ItemCapabilities.CanLoop) is True, u'Images can be made to Loop'
        assert service_item.is_capable(ItemCapabilities.CanAppend) is True, u'Images can have new items added'


    def convert_file_service_item(self, name):
        service_file = os.path.join(TEST_PATH, name)
        try:
            open_file = open(service_file, u'r')
            items = cPickle.load(open_file)
            first_line = items[0]
        except IOError:
            first_line = u''
        return first_line