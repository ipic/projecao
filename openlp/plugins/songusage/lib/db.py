# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2010 Raoul Snyman                                        #
# Portions copyright (c) 2008-2010 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Christian Richter, Maikel Stuivenberg, Martin      #
# Thompson, Jon Tibble, Carsten Tinggaard                                     #
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
The :mod:`db` module provides the database and schema that is the backend for
the SongUsage plugin
"""

from sqlalchemy import Column, Table, types
from sqlalchemy.orm import mapper

from openlp.core.lib.db import BaseModel, init_db

class SongUsageItem(BaseModel):
    """
    SongUsageItem model
    """
    pass

def init_schema(url):
    """
    Setup the songusage database connection and initialise the database schema

    ``url``
        The database to setup
    """
    session, metadata = init_db(url)

    songusage_table = Table(u'songusage_data', metadata,
        Column(u'id', types.Integer(), primary_key=True),
        Column(u'usagedate', types.Date, index=True, nullable=False),
        Column(u'usagetime', types.Time, index=True, nullable=False),
        Column(u'title', types.Unicode(255), nullable=False),
        Column(u'authors', types.Unicode(255), nullable=False),
        Column(u'copyright', types.Unicode(255)),
        Column(u'ccl_number', types.Unicode(65))
    )

    mapper(SongUsageItem, songusage_table)

    metadata.create_all(checkfirst=True)
    return session