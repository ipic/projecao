# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
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

class VerseReferenceList(object):
    """
    The VerseReferenceList class encapsulates a list of verse references, but
    maintains the order in which they were added.
    """

    def __init__(self):
        self.verse_list = []
        self.version_list = []
        self.current_index = -1

    def add(self, book, chapter, verse, version, copyright, permission):
        self.add_version(version, copyright, permission)
        if not self.verse_list or \
            self.verse_list[self.current_index][u'book'] != book:
            self.verse_list.append({u'version': version, u'book': book,
                u'chapter': chapter, u'start': verse, u'end': verse})
            self.current_index += 1
        elif self.verse_list[self.current_index][u'chapter'] != chapter:
            self.verse_list.append({u'version': version, u'book': book,
                u'chapter': chapter, u'start': verse, u'end': verse})
            self.current_index += 1
        elif (self.verse_list[self.current_index][u'end'] + 1) == verse:
            self.verse_list[self.current_index][u'end'] = verse
        else:
            self.verse_list.append({u'version': version, u'book': book,
                u'chapter': chapter, u'start': verse, u'end': verse})
            self.current_index += 1

    def add_version(self, version, copyright, permission):
        for bible_version in self.version_list:
            if bible_version[u'version'] == version:
                return
        self.version_list.append({u'version': version, u'copyright': copyright,
            u'permission': permission})

    def format_verses(self):
        result = u''
        for index, verse in enumerate(self.verse_list):
            if index == 0:
                result = u'%s %s:%s' % (verse[u'book'], verse[u'chapter'],
                    verse[u'start'])
                if verse[u'start'] != verse[u'end']:
                    result = u'%s-%s' % (result, verse[u'end'])
                continue
            prev = index - 1
            if self.verse_list[prev][u'version'] != verse[u'version']:
                result = u'%s (%s)' % (result, self.verse_list[prev][u'version'])
            result = result + u', '
            if self.verse_list[prev][u'book'] != verse[u'book']:
                result = u'%s%s %s:' % (result, verse[u'book'],
                    verse[u'chapter'])
            elif self.verse_list[prev][u'chapter'] != verse[u'chapter']:
                result = u'%s%s:' % (result, verse[u'chapter'])
            result = result + str(verse[u'start'])
            if verse[u'start'] != verse[u'end']:
                result = u'%s-%s' % (result, verse[u'end'])
        if len(self.version_list) > 1:
            result = u'%s (%s)' % (result, verse[u'version'])
        return result

    def format_versions(self):
        result = u''
        for index, version in enumerate(self.version_list):
            if index > 0:
                if result[-1] not in [u';', u',', u'.']:
                    result = result + u';'
                result = result + u' '
            result = u'%s%s, %s' % (result, version[u'version'],
                version[u'copyright'])
            if version[u'permission'].strip():
                result = result + u', ' + version[u'permission']
        return result