# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley,

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA
"""

import logging

from PyQt4 import Qt, QtCore, QtGui

from openlp.core.lib import SongXMLBuilder, SongXMLParser, Event, \
    EventType, EventManager
from openlp.plugins.songs.forms import EditVerseForm
from openlp.plugins.songs.lib.models import Song
from editsongdialog import Ui_EditSongDialog

class EditSongForm(QtGui.QDialog, Ui_EditSongDialog):
    """
    Class to manage the editing of a song
    """
    global log
    log = logging.getLogger(u'EditSongForm')
    log.info(u'Song Editor loaded')

    def __init__(self, songmanager, eventmanager, parent=None):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        # Connecting signals and slots
        QtCore.QObject.connect(self.AuthorAddButton,
            QtCore.SIGNAL(u'clicked()'), self.onAuthorAddButtonClicked)
        QtCore.QObject.connect(self.AuthorRemoveButton,
            QtCore.SIGNAL(u'clicked()'), self.onAuthorRemoveButtonClicked)
        QtCore.QObject.connect(self.AuthorsListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'), self.onAuthorsListViewPressed)
        QtCore.QObject.connect(self.TopicAddButton,
            QtCore.SIGNAL(u'clicked()'), self.onTopicAddButtonClicked)
        QtCore.QObject.connect(self.TopicRemoveButton,
            QtCore.SIGNAL(u'clicked()'), self.onTopicRemoveButtonClicked)
        QtCore.QObject.connect(self.TopicsListView,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'), self.onTopicListViewPressed)
        QtCore.QObject.connect(self.CopyrightInsertButton,
            QtCore.SIGNAL(u'clicked()'), self.onCopyrightInsertButtonTriggered)
        QtCore.QObject.connect(self.VerseAddButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseAddButtonClicked)
        QtCore.QObject.connect(self.VerseEditButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseEditButtonClicked)
        QtCore.QObject.connect(self.VerseDeleteButton,
            QtCore.SIGNAL(u'clicked()'), self.onVerseDeleteButtonClicked)
        QtCore.QObject.connect(self.VerseListWidget,
            QtCore.SIGNAL(u'itemClicked(QListWidgetItem*)'), self.onVerseListViewPressed)
        QtCore.QObject.connect(self.SongbookCombo,
            QtCore.SIGNAL(u'activated(int)'), self.onSongBookComboChanged)
        QtCore.QObject.connect(self.ThemeSelectionComboItem,
            QtCore.SIGNAL(u'activated(int)'), self.onThemeComboChanged)
        QtCore.QObject.connect(self.MaintenanceButton,
            QtCore.SIGNAL(u'clicked()'), self.onMaintenanceButtonClicked)
        # Create other objects and forms
        self.songmanager = songmanager
        self.eventmanager = eventmanager
        self.parent = parent
        self.verse_form = EditVerseForm()
        self.initialise()
        self.AuthorsListView.setSortingEnabled(False)
        self.AuthorsListView.setAlternatingRowColors(True)
        self.TopicsListView.setSortingEnabled(False)
        self.TopicsListView.setAlternatingRowColors(True)

    def initialise(self):
        self.VerseEditButton.setEnabled(False)
        self.VerseDeleteButton.setEnabled(False)
        self.AuthorRemoveButton.setEnabled(False)
        self.TopicRemoveButton.setEnabled(False)
        self.title_change = False

    def loadAuthors(self):
        authors = self.songmanager.get_authors()
        self.AuthorsSelectionComboItem.clear()
        for author in authors:
            row = self.AuthorsSelectionComboItem.count()
            self.AuthorsSelectionComboItem.addItem(author.display_name)
            self.AuthorsSelectionComboItem.setItemData(row, QtCore.QVariant(author.id))

    def loadTopics(self):
        topics = self.songmanager.get_topics()
        self.SongTopicCombo.clear()
        for topic in topics:
            row = self.SongTopicCombo.count()
            self.SongTopicCombo.addItem(topic.name)
            self.SongTopicCombo.setItemData(row, QtCore.QVariant(topic.id))

    def loadBooks(self):
        books = self.songmanager.get_books()
        self.SongbookCombo.clear()
        self.SongbookCombo.addItem(u' ')
        for book in books:
            row = self.SongbookCombo.count()
            self.SongbookCombo.addItem(book.name)
            self.SongbookCombo.setItemData(row, QtCore.QVariant(book.id))

    def loadThemes(self, theme_list):
        self.ThemeSelectionComboItem.clear()
        self.ThemeSelectionComboItem.addItem(u' ')
        for theme in theme_list:
            self.ThemeSelectionComboItem.addItem(theme)

    def newSong(self):
        log.debug(u'New Song')
        self.SongTabWidget.setCurrentIndex(0)
        self.song = Song()
        self.TitleEditItem.setText(u'')
        self.AlternativeEdit.setText(u'')
        self.CopyrightEditItem.setText(u'')
        self.VerseOrderEdit.setText(u'')
        self.CommentsEdit.setText(u'')
        self.CCLNumberEdit.setText(u'')
        self.VerseListWidget.clear()
        self.AuthorsListView.clear()
        self.TopicsListView.clear()
        self.title_change = False
        self.TitleEditItem.setFocus(QtCore.Qt.OtherFocusReason)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()

    def loadSong(self, id):
        log.debug(u'Load Song')
        self.SongTabWidget.setCurrentIndex(0)
        self.loadAuthors()
        self.loadTopics()
        self.loadBooks()
        self.song = self.songmanager.get_song(id)
        self.TitleEditItem.setText(self.song.title)
        title = self.song.search_title.split(u'@')
        if self.song.song_book_id != 0:
            book_name = self.songmanager.get_book(self.song.song_book_id)
            id = self.SongbookCombo.findText(unicode(book_name.name), QtCore.Qt.MatchExactly)
            if id == -1:
                # Not Found
                id = 0
            self.SongbookCombo.setCurrentIndex(id)
        if self.song.theme_name is not None and len(self.song.theme_name) > 0:
            id = self.ThemeSelectionComboItem.findText(unicode(self.song.theme_name), QtCore.Qt.MatchExactly)
            if id == -1:
                # Not Found
                id = 0
                self.song.theme_name = None
            self.ThemeSelectionComboItem.setCurrentIndex(id)
        if len(title) > 1:
            self.AlternativeEdit.setText(title[1])
        if self.song.copyright is not None:
            self.CopyrightEditItem.setText(self.song.copyright)
        else:
            self.CopyrightEditItem.setText(u'')
        self.VerseListWidget.clear()
        if self.song.verse_order is not None:
            self.VerseOrderEdit.setText(self.song.verse_order)
        else:
            self.VerseOrderEdit.setText(u'')
        if self.song.comments is not None:
            self.CommentsEdit.setPlainText(self.song.comments)
        else:
            self.CommentsEdit.setPlainText(u'')
        if self.song.ccli_number is not None:
            self.CCLNumberEdit.setText(self.song.ccli_number)
        else:
            self.CCLNumberEdit.setText(u'')
        #lazy xml migration for now
        if self.song.lyrics.startswith(u'<?xml version='):
            songXML = SongXMLParser(self.song.lyrics)
            verseList = songXML.get_verses()
            for verse in verseList:
                self.VerseListWidget.addItem(verse[1])
        else:
            verses = self.song.lyrics.split(u'\n\n')
            for verse in verses:
                self.VerseListWidget.addItem(verse)
        # clear the results
        self.AuthorsListView.clear()
        for author in self.song.authors:
            author_name = QtGui.QListWidgetItem(unicode(author.display_name))
            author_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListView.addItem(author_name)
        # clear the results
        self.TopicsListView.clear()
        for topic in self.song.topics:
            topic_name = QtGui.QListWidgetItem(unicode(topic.name))
            topic_name.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListView.addItem(topic_name)
        self._validate_song()
        self.title_change = False
        self.TitleEditItem.setFocus(QtCore.Qt.OtherFocusReason)

    def onAuthorAddButtonClicked(self):
        item = int(self.AuthorsSelectionComboItem.currentIndex())
        if item > -1:
            item_id = (self.AuthorsSelectionComboItem.itemData(item)).toInt()[0]
            author = self.songmanager.get_author(item_id)
            self.song.authors.append(author)
            author_item = QtGui.QListWidgetItem(unicode(author.display_name))
            author_item.setData(QtCore.Qt.UserRole, QtCore.QVariant(author.id))
            self.AuthorsListView.addItem(author_item)

    def onAuthorsListViewPressed(self):
        if self.AuthorsListView.count() > 1:
            self.AuthorRemoveButton.setEnabled(True)

    def onAuthorRemoveButtonClicked(self):
        self.AuthorRemoveButton.setEnabled(False)
        item = self.AuthorsListView.currentItem()
        author_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        author = self.songmanager.get_author(author_id)
        self.song.authors.remove(author)
        row = self.AuthorsListView.row(item)
        self.AuthorsListView.takeItem(row)

    def onTopicAddButtonClicked(self):
        item = int(self.SongTopicCombo.currentIndex())
        if item > -1:
            item_id = (self.SongTopicCombo.itemData(item)).toInt()[0]
            topic = self.songmanager.get_topic(item_id)
            self.song.topics.append(topic)
            topic_item = QtGui.QListWidgetItem(unicode(topic.name))
            topic_item.setData(QtCore.Qt.UserRole, QtCore.QVariant(topic.id))
            self.TopicsListView.addItem(topic_item)

    def onTopicListViewPressed(self):
        self.TopicRemoveButton.setEnabled(True)

    def onTopicRemoveButtonClicked(self):
        self.TopicRemoveButton.setEnabled(False)
        item = self.TopicsListView.currentItem()
        topic_id = (item.data(QtCore.Qt.UserRole)).toInt()[0]
        topic = self.songmanager.get_topic(topic_id)
        self.song.topics.remove(topic)
        row = self.TopicsListView.row(item)
        self.TopicsListView.takeItem(row)

    def onSongBookComboChanged(self, item):
        if item == 0:
            self.song.song_book_id = 0
        else:
            item = int(self.SongbookCombo.currentIndex())
            self.song.song_book_id = (self.SongbookCombo.itemData(item)).toInt()[0]

    def onThemeComboChanged(self, item):
        if item == 0:
            #None means no Theme
            self.song.song_theme = None
        else:
            them_name = unicode(self.ThemeSelectionComboItem.itemText(item))
            self.song.theme_name = them_name

    def onVerseListViewPressed(self):
        self.VerseEditButton.setEnabled(True)
        self.VerseDeleteButton.setEnabled(True)

    def onVerseAddButtonClicked(self):
        self.verse_form.setVerse(u'')
        self.verse_form.exec_()
        self.VerseListWidget.addItem(self.verse_form.getVerse())

    def onVerseEditButtonClicked(self):
        item = self.VerseListWidget.currentItem()
        if item is not None:
            self.verse_form.setVerse(item.text())
            self.verse_form.exec_()
            item.setText(self.verse_form.getVerse())
        self.VerseListWidget.repaint()
        self.VerseEditButton.setEnabled(False)
        self.VerseDeleteButton.setEnabled(False)

    def onVerseDeleteButtonClicked(self):
        item = self.VerseListWidget.takeItem(self.VerseListWidget.currentRow())
        item = None
        self.VerseEditButton.setEnabled(False)
        self.VerseDeleteButton.setEnabled(False)

    def _validate_song(self):
        """
        Check the validity of the form. Only display the 'save' if the data can be saved.
        """
        log.debug(u'Validate Song')
        # Lets be nice and assume the data is correct.
        valid = True
        if len(self.TitleEditItem.displayText()) == 0:
            valid = False
            self.TitleEditItem.setStyleSheet(u'background-color: red; color: white')
        else:
            self.TitleEditItem.setStyleSheet(u'')
        if self.VerseListWidget.count() == 0:
            valid = False
            self.VerseListWidget.setStyleSheet(u'background-color: red; color: white')
        else:
            self.VerseListWidget.setStyleSheet(u'')
        if self.AuthorsListView.count() == 0:
            valid = False
            self.AuthorsListView.setStyleSheet(u'background-color: red; color: white')
        else:
            self.AuthorsListView.setStyleSheet(u'')
        return valid

    def on_TitleEditItem_lostFocus(self):
        self.song.title = self.TitleEditItem.text()
        self.title_change = True

    def on_VerseOrderEdit_lostFocus(self):
        self.song.verse_order = self.VerseOrderEdit.text()

    def on_CommentsEdit_lostFocus(self):
        self.song.comments = self.CommentsEdit.text()

    def on_CCLNumberEdit_lostFocus(self):
        self.song.ccli_number = self.CCLNumberEdit.text()

    def onCopyrightInsertButtonTriggered(self):
        text = self.CopyrightEditItem.displayText()
        pos = self.CopyrightEditItem.cursorPosition()
        text = text[:pos] + u'©' + text[pos:]
        self.CopyrightEditItem.setText(text)
        self.CopyrightEditItem.setFocus()
        self.CopyrightEditItem.setCursorPosition(pos + 1)

    def onMaintenanceButtonClicked(self):
        self.parent.song_maintenance_form.exec_()
        self.loadAuthors()
        self.loadBooks()
        self.loadTopics()

    def accept(self):
        log.debug(u'accept')
        if not self._validate_song():
            return
        self.song.title = unicode(self.TitleEditItem.displayText())
        self.song.copyright = unicode(self.CopyrightEditItem.displayText())
        self.song.search_title = unicode(self.TitleEditItem.displayText()) + u'@'+ unicode(self.AlternativeEdit.displayText())
        self.song.comments = unicode(self.CommentsEdit.toPlainText())
        self.song.ccli_number = unicode(self.CCLNumberEdit.displayText())
        self.processLyrics()
        self.processTitle()
        self.songmanager.save_song(self.song)
        if self.title_change:
            self.eventmanager.post_event(Event(u'EditSongForm', EventType.LoadSongList))
        self.close()

    def processLyrics(self):
        log.debug(u'processLyrics')
        sxml = SongXMLBuilder()
        sxml.new_document()
        sxml.add_lyrics_to_song()
        count = 1
        text = u' '
        verse_order = u''
        for i in range (0, self.VerseListWidget.count()):
            sxml.add_verse_to_lyrics(u'Verse', unicode(count),
                unicode(self.VerseListWidget.item(i).text()))
            text = text + unicode(self.VerseListWidget.item(i).text()) + u' '
            verse_order = verse_order + unicode(count) + u' '
            count += 1
        if self.song.verse_order is None:
            self.song.verse_order = verse_order
        text = text.replace(u'\'', u'')
        text = text.replace(u',', u'')
        text = text.replace(u';', u'')
        text = text.replace(u':', u'')
        text = text.replace(u'(', u'')
        text = text.replace(u')', u'')
        text = text.replace(u'{', u'')
        text = text.replace(u'}', u'')
        text = text.replace(u'?', u'')
        self.song.search_lyrics  = unicode(text)
        self.song.lyrics = unicode(sxml.extract_xml())

    def processTitle(self):
        log.debug(u'processTitle')
        self.song.search_title = self.song.search_title.replace(u'\'', u'')
        self.song.search_title = self.song.search_title.replace(u',', u'')
        self.song.search_title = self.song.search_title.replace(u';', u'')
        self.song.search_title = self.song.search_title.replace(u':', u'')
        self.song.search_title = self.song.search_title.replace(u'(', u'')
        self.song.search_title = self.song.search_title.replace(u')', u'')
        self.song.search_title = self.song.search_title.replace(u'{', u'')
        self.song.search_title = self.song.search_title.replace(u'}', u'')
        self.song.search_title = self.song.search_title.replace(u'?', u'')
        self.song.search_title = unicode(self.song.search_title)
