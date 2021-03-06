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
import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path

from openlp.core.api.http import requires_auth
from openlp.core.api.http.endpoint import Endpoint
from openlp.core.common.applocation import AppLocation
from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.lib import create_thumb
from openlp.core.lib.serviceitem import ItemCapabilities


log = logging.getLogger(__name__)

controller_endpoint = Endpoint('controller')
api_controller_endpoint = Endpoint('api')


@api_controller_endpoint.route('controller/live/text')
@controller_endpoint.route('live/text')
def controller_text(request):
    """
    Perform an action on the slide controller.

    :param request: the http request - not used
    """
    log.debug('controller_text')
    live_controller = Registry().get('live_controller')
    current_item = live_controller.service_item
    data = []
    if current_item:
        for index, frame in enumerate(current_item.get_frames()):
            item = {}
            # Handle text (songs, custom, bibles)
            if current_item.is_text():
                if frame['verse']:
                    item['tag'] = str(frame['verse'])
                else:
                    item['tag'] = str(index + 1)
                # TODO: Figure out rendering chords
                item['chords_text'] = str(frame.get('chords_text', ''))
                item['text'] = frame['text']
                item['html'] = current_item.get_rendered_frame(index)
            # Handle images, unless a custom thumbnail is given or if thumbnails is disabled
            elif current_item.is_image() and not frame.get('image', '') and Settings().value('api/thumbnails'):
                item['tag'] = str(index + 1)
                thumbnail_path = os.path.join('images', 'thumbnails', frame['title'])
                full_thumbnail_path = AppLocation.get_data_path() / thumbnail_path
                # Create thumbnail if it doesn't exists
                if not full_thumbnail_path.exists():
                    create_thumb(Path(current_item.get_frame_path(index)), full_thumbnail_path, False)
                Registry().get('image_manager').add_image(str(full_thumbnail_path), frame['title'], None, 88, 88)
                item['img'] = urllib.request.pathname2url(os.path.sep + str(thumbnail_path))
                item['text'] = str(frame['title'])
                item['html'] = str(frame['title'])
            else:
                # Handle presentation etc.
                item['tag'] = str(index + 1)
                if current_item.is_capable(ItemCapabilities.HasDisplayTitle):
                    item['title'] = str(frame['display_title'])
                if current_item.is_capable(ItemCapabilities.HasNotes):
                    item['slide_notes'] = str(frame['notes'])
                if current_item.is_capable(ItemCapabilities.HasThumbnails) and Settings().value('api/thumbnails'):
                    # If the file is under our app directory tree send the portion after the match
                    data_path = str(AppLocation.get_data_path())
                    if frame['image'][0:len(data_path)] == data_path:
                        item['img'] = urllib.request.pathname2url(frame['image'][len(data_path):])
                    Registry().get('image_manager').add_image(frame['image'], frame['title'], None, 88, 88)
                item['text'] = str(frame['title'])
                item['html'] = str(frame['title'])
            item['selected'] = (live_controller.selected_row == index)
            item['title'] = current_item.title
            data.append(item)
    json_data = {'results': {'slides': data}}
    if current_item:
        json_data['results']['item'] = live_controller.service_item.unique_identifier
    return json_data


@api_controller_endpoint.route('controller/live/set')
@controller_endpoint.route('live/set')
@requires_auth
def controller_set(request):
    """
    Perform an action on the slide controller.

    :param request: The action to perform.
    """
    event = getattr(Registry().get('live_controller'), 'slidecontroller_live_set')
    try:
        json_data = request.GET.get('data')
        data = int(json.loads(json_data)['request']['id'])
        event.emit([data])
    except KeyError:
        log.error("Endpoint controller/live/set request id not found")
    return {'results': {'success': True}}


@controller_endpoint.route('{controller}/{action:next|previous}')
@requires_auth
def controller_direction(request, controller, action):
    """
    Handles requests for setting service items in the slide controller
    :param request: The http request object.
    :param controller: the controller slides forward or backward.
    :param action: the controller slides forward or backward.
    """
    event = getattr(Registry().get('live_controller'), 'slidecontroller_{controller}_{action}'.
                    format(controller=controller, action=action))
    event.emit()


@api_controller_endpoint.route('controller/{controller}/{action:next|previous}')
@requires_auth
def controller_direction_api(request, controller, action):
    """
    Handles requests for setting service items in the slide controller

    :param request: The http request object.
    :param controller: the controller slides forward or backward.
    :param action: the controller slides forward or backward.
    """
    controller_direction(request, controller, action)
    return {'results': {'success': True}}
