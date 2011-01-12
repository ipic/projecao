# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
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
The :mod:`openlyricsimport` module provides the functionality for importing
songs which are saved as OpenLyrics files.
"""

import logging
import os

from lxml import etree

from openlp.core.lib import translate
from openlp.plugins.songs.lib.songimport import SongImport
from openlp.plugins.songs.lib import OpenLyrics

log = logging.getLogger(__name__)

class OpenLyricsImport(SongImport):
    """
    This provides the Openlyrics import.
    """
    def __init__(self, master_manager, **kwargs):
        """
        Initialise the import.
        """
        log.debug(u'initialise OpenLyricsImport')
        SongImport.__init__(self, master_manager)
        self.master_manager = master_manager
        self.openLyrics = OpenLyrics(master_manager)
        if kwargs.has_key(u'filename'):
            self.import_source = kwargs[u'filename']
        if kwargs.has_key(u'filenames'):
            self.import_source = kwargs[u'filenames']

    def do_import(self):
        """
        Imports the songs.
        """
        self.import_wizard.importProgressBar.setMaximum(len(self.import_source))
        for file_path in self.import_source:
            if self.stop_import_flag:
                return False
            self.import_wizard.incrementProgressBar(unicode(translate(
                'SongsPlugin.OpenLyricsImport', 'Importing %s...')) %
                os.path.basename(file_path))
            parser = etree.XMLParser(remove_blank_text=True)
            file = etree.parse(file_path, parser)
            xml = unicode(etree.tostring(file))
            if self.openLyrics.xml_to_song(xml) is None:
                log.debug(u'File could not be imported: %s' % file_path)
                # Importing this song failed! For now we stop import.
                return False
        return True