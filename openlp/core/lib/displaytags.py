# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Andreas Preikschat, Christian      #
# Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon Tibble,    #
# Carsten Tinggaard, Frode Woldsund                                           #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
Provide Html Tag management and Display Tag access class
"""

from openlp.core.lib import base_html_expands

class HtmlTags(object):
    """
    """
    def __init__(self):
        self.html_expands = []
        self.reset_list()

    def reset_list(self):
        """
        """
        self.html_expands = []
        for html in base_html_expands:
            self.html_expands.append(html)

    def add_tag(self, html):
        """
        """
        self.html_expands.append(html)


class DisplayTags(object):
    """
    Static Class to HTML Tags to be access around the code the list is managed
    by the Options Tab.
    """
    html_tags = HtmlTags()

    @staticmethod
    def get_html_tags():
        """
        Provide access to the html_expands list.
        """
        return DisplayTags.html_tags.html_expands

    @staticmethod
    def reset_html_tags():
        """
        Resets the html_expands list.
        """
        return DisplayTags.html_tags.reset_list()

    @staticmethod
    def add_html_tag(tag):
        """
        Add a new tag to the list
        """
        return DisplayTags.html_tags.add_tag(tag)

    @staticmethod
    def remove_html_tag(id):
        """
        Removes amd individual html_expands list.
        """
        return DisplayTags.html_tags.html_expands.pop(id)
