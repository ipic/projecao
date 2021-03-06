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

from PyQt5 import QtCore, QtWidgets

from openlp.core.common.i18n import translate
from openlp.core.lib.settingstab import SettingsTab
from openlp.plugins.songs.lib.db import AuthorType


class SongsTab(SettingsTab):
    """
    SongsTab is the Songs settings tab in the settings dialog.
    """
    def setup_ui(self):
        """
        Set up the configuration tab UI.
        """
        self.setObjectName('SongsTab')
        super(SongsTab, self).setup_ui()
        self.mode_group_box = QtWidgets.QGroupBox(self.left_column)
        self.mode_group_box.setObjectName('mode_group_box')
        self.mode_layout = QtWidgets.QVBoxLayout(self.mode_group_box)
        self.mode_layout.setObjectName('mode_layout')
        self.tool_bar_active_check_box = QtWidgets.QCheckBox(self.mode_group_box)
        self.tool_bar_active_check_box.setObjectName('tool_bar_active_check_box')
        self.mode_layout.addWidget(self.tool_bar_active_check_box)
        self.update_on_edit_check_box = QtWidgets.QCheckBox(self.mode_group_box)
        self.update_on_edit_check_box.setObjectName('update_on_edit_check_box')
        self.mode_layout.addWidget(self.update_on_edit_check_box)
        self.add_from_service_check_box = QtWidgets.QCheckBox(self.mode_group_box)
        self.add_from_service_check_box.setObjectName('add_from_service_check_box')
        self.mode_layout.addWidget(self.add_from_service_check_box)
        self.songbook_slide_check_box = QtWidgets.QCheckBox(self.mode_group_box)
        self.songbook_slide_check_box.setObjectName('songbook_slide_check_box')
        self.mode_layout.addWidget(self.songbook_slide_check_box)
        self.left_layout.addWidget(self.mode_group_box)
        # Chords group box
        self.chords_group_box = QtWidgets.QGroupBox(self.left_column)
        self.chords_group_box.setObjectName('chords_group_box')
        self.chords_group_box.setCheckable(True)
        self.chords_layout = QtWidgets.QVBoxLayout(self.chords_group_box)
        self.chords_layout.setObjectName('chords_layout')
        self.chords_info_label = QtWidgets.QLabel(self.chords_group_box)
        self.chords_info_label.setWordWrap(True)
        self.chords_layout.addWidget(self.chords_info_label)
        self.mainview_chords_check_box = QtWidgets.QCheckBox(self.mode_group_box)
        self.mainview_chords_check_box.setObjectName('mainview_chords_check_box')
        self.chords_layout.addWidget(self.mainview_chords_check_box)
        self.disable_chords_import_check_box = QtWidgets.QCheckBox(self.mode_group_box)
        self.disable_chords_import_check_box.setObjectName('disable_chords_import_check_box')
        self.chords_layout.addWidget(self.disable_chords_import_check_box)
        # Chords notation group box
        self.chord_notation_label = QtWidgets.QLabel(self.chords_group_box)
        self.chord_notation_label.setWordWrap(True)
        self.chords_layout.addWidget(self.chord_notation_label)
        self.english_notation_radio_button = QtWidgets.QRadioButton(self.chords_group_box)
        self.english_notation_radio_button.setObjectName('english_notation_radio_button')
        self.chords_layout.addWidget(self.english_notation_radio_button)
        self.german_notation_radio_button = QtWidgets.QRadioButton(self.chords_group_box)
        self.german_notation_radio_button.setObjectName('german_notation_radio_button')
        self.chords_layout.addWidget(self.german_notation_radio_button)
        self.neolatin_notation_radio_button = QtWidgets.QRadioButton(self.chords_group_box)
        self.neolatin_notation_radio_button.setObjectName('neolatin_notation_radio_button')
        self.chords_layout.addWidget(self.neolatin_notation_radio_button)
        self.left_layout.addWidget(self.chords_group_box)
        # Footer group box
        self.footer_group_box = QtWidgets.QGroupBox(self.left_column)
        self.footer_group_box.setObjectName('footer_group_box')
        self.footer_layout = QtWidgets.QVBoxLayout(self.footer_group_box)
        self.footer_layout.setObjectName('footer_layout')
        self.footer_info_label = QtWidgets.QLabel(self.footer_group_box)
        self.footer_layout.addWidget(self.footer_info_label)
        self.footer_placeholder_info = QtWidgets.QTextEdit(self.footer_group_box)
        self.footer_layout.addWidget(self.footer_placeholder_info)
        self.footer_desc_label = QtWidgets.QLabel(self.footer_group_box)
        self.footer_layout.addWidget(self.footer_desc_label)
        self.footer_edit_box = QtWidgets.QTextEdit(self.footer_group_box)
        self.footer_layout.addWidget(self.footer_edit_box)
        self.footer_reset_button = QtWidgets.QPushButton(self.footer_group_box)
        self.footer_layout.addWidget(self.footer_reset_button, alignment=QtCore.Qt.AlignRight)
        self.right_layout.addWidget(self.footer_group_box)
        self.left_layout.addStretch()
        self.right_layout.addStretch()
        self.tool_bar_active_check_box.stateChanged.connect(self.on_tool_bar_active_check_box_changed)
        self.update_on_edit_check_box.stateChanged.connect(self.on_update_on_edit_check_box_changed)
        self.add_from_service_check_box.stateChanged.connect(self.on_add_from_service_check_box_changed)
        self.songbook_slide_check_box.stateChanged.connect(self.on_songbook_slide_check_box_changed)
        self.mainview_chords_check_box.stateChanged.connect(self.on_mainview_chords_check_box_changed)
        self.disable_chords_import_check_box.stateChanged.connect(self.on_disable_chords_import_check_box_changed)
        self.english_notation_radio_button.clicked.connect(self.on_english_notation_button_clicked)
        self.german_notation_radio_button.clicked.connect(self.on_german_notation_button_clicked)
        self.neolatin_notation_radio_button.clicked.connect(self.on_neolatin_notation_button_clicked)
        self.footer_reset_button.clicked.connect(self.on_footer_reset_button_clicked)

    def retranslate_ui(self):
        self.mode_group_box.setTitle(translate('SongsPlugin.SongsTab', 'Song related settings'))
        self.tool_bar_active_check_box.setText(translate('SongsPlugin.SongsTab',
                                                         'Enable "Go to verse" button in Live panel'))
        self.update_on_edit_check_box.setText(translate('SongsPlugin.SongsTab', 'Update service from song edit'))
        self.add_from_service_check_box.setText(translate('SongsPlugin.SongsTab',
                                                          'Import missing songs from Service files'))
        self.songbook_slide_check_box.setText(translate('SongsPlugin.SongsTab',
                                                        'Add Songbooks as first slide'))
        self.chords_info_label.setText(translate('SongsPlugin.SongsTab', 'If enabled all text between "[" and "]" will '
                                                                         'be regarded as chords.'))
        self.chords_group_box.setTitle(translate('SongsPlugin.SongsTab', 'Chords'))
        self.mainview_chords_check_box.setText(translate('SongsPlugin.SongsTab', 'Display chords in the main view'))
        self.disable_chords_import_check_box.setText(translate('SongsPlugin.SongsTab',
                                                               'Ignore chords when importing songs'))
        self.chord_notation_label.setText(translate('SongsPlugin.SongsTab', 'Chord notation to use:'))
        self.english_notation_radio_button.setText(translate('SongsPlugin.SongsTab', 'English') + ' (C-D-E-F-G-A-B)')
        self.german_notation_radio_button.setText(translate('SongsPlugin.SongsTab', 'German') + ' (C-D-E-F-G-A-H)')
        self.neolatin_notation_radio_button.setText(
            translate('SongsPlugin.SongsTab', 'Neo-Latin') + ' (Do-Re-Mi-Fa-Sol-La-Si)')
        self.footer_group_box.setTitle(translate('SongsPlugin.SongsTab', 'Footer'))
        # Keep this in sync with the list in mediaitem.py
        const = '<code>"{}"</code>'
        placeholders = [
            # placeholder, description, can be empty, is a list
            ['title', translate('SongsPlugin.SongsTab', 'Song Title'), False, False],
            ['alternate_title', translate('SongsPlugin.SongsTab', 'Alternate Title'), True, False],
            ['written_by', const.format(translate('SongsPlugin.SongsTab', 'Written By')), True, False],
            ['authors_none', translate('SongsPlugin.SongsTab', 'Authors when type is not set'), False, True],
            ['authors_words_label', const.format(AuthorType.Types[AuthorType.Words]), False, False],
            ['authors_words', translate('SongsPlugin.SongsTab', 'Authors (Type "Words")'), False, True],
            ['authors_music_label', const.format(AuthorType.Types[AuthorType.Music]), False, False],
            ['authors_music', translate('SongsPlugin.SongsTab', 'Authors (Type "Music")'), False, True],
            ['authors_words_music_label', const.format(AuthorType.Types[AuthorType.WordsAndMusic]), False, False],
            ['authors_words_music', translate('SongsPlugin.SongsTab', 'Authors (Type "Words and Music")'), False, True],
            ['authors_translation_label', const.format(AuthorType.Types[AuthorType.Translation]), False, False],
            ['authors_translation', translate('SongsPlugin.SongsTab', 'Authors (Type "Translation")'), False, True],
            ['authors_words_all', translate('SongsPlugin.SongsTab', 'Authors (Type "Words" & "Words and Music")'),
             False, True],
            ['authors_music_all', translate('SongsPlugin.SongsTab', 'Authors (Type "Music" & "Words and Music")'),
             False, True],
            ['copyright', translate('SongsPlugin.SongsTab', 'Copyright information'), True, False],
            ['songbook_entries', translate('SongsPlugin.SongsTab', 'Songbook Entries'), False, True],
            ['ccli_license', translate('SongsPlugin.SongsTab', 'CCLI License'), True, False],
            ['ccli_license_label', const.format(translate('SongsPlugin.SongsTab', 'CCLI License')), False, False],
            ['ccli_number', translate('SongsPlugin.SongsTab', 'Song CCLI Number'), True, False],
            ['topics', translate('SongsPlugin.SongsTab', 'Topics'), False, True],
        ]
        placeholder_info = '<table style="background: #eee">\n<tr><th><b>{ph}</b></th><th><b>{desc}</b></th></tr>\n'\
            .format(ph=translate('SongsPlugin.SongsTab', 'Placeholder'),
                    desc=translate('SongsPlugin.SongsTab', 'Description'))
        for placeholder in placeholders:
            placeholder_info += '<tr><td>${{{pl}}}</td><td>{des}{opt}</td></tr>\n'\
                                .format(pl=placeholder[0], des=placeholder[1],
                                        opt=('&nbsp;¹' if placeholder[2] else '') +
                                            ('&nbsp;²' if placeholder[3] else ''))
        placeholder_info += '</table>'
        placeholder_info += '\n<br/>¹ {}'.format(translate('SongsPlugin.SongsTab', 'can be empty'))
        placeholder_info += '\n<br/>² {}'.format(translate('SongsPlugin.SongsTab', 'list of entries, can be empty'))
        self.footer_placeholder_info.setHtml(placeholder_info)
        self.footer_placeholder_info.setReadOnly(True)

        self.footer_info_label.setText(translate('SongsPlugin.SongsTab', 'How to use Footers:'))
        self.footer_desc_label.setText('{} (<a href="http://docs.makotemplates.org">{}</a>):'
                                       .format(translate('SongsPlugin.SongsTab', 'Footer Template'),
                                               translate('SongsPlugin.SongsTab', 'Mako Syntax')))
        self.footer_reset_button.setText(translate('SongsPlugin.SongsTab', 'Reset Template'))

    def on_search_as_type_check_box_changed(self, check_state):
        self.song_search = (check_state == QtCore.Qt.Checked)

    def on_tool_bar_active_check_box_changed(self, check_state):
        self.tool_bar = (check_state == QtCore.Qt.Checked)

    def on_update_on_edit_check_box_changed(self, check_state):
        self.update_edit = (check_state == QtCore.Qt.Checked)

    def on_add_from_service_check_box_changed(self, check_state):
        self.update_load = (check_state == QtCore.Qt.Checked)

    def on_songbook_slide_check_box_changed(self, check_state):
        self.songbook_slide = (check_state == QtCore.Qt.Checked)

    def on_mainview_chords_check_box_changed(self, check_state):
        self.mainview_chords = (check_state == QtCore.Qt.Checked)

    def on_disable_chords_import_check_box_changed(self, check_state):
        self.disable_chords_import = (check_state == QtCore.Qt.Checked)

    def on_english_notation_button_clicked(self):
        self.chord_notation = 'english'

    def on_german_notation_button_clicked(self):
        self.chord_notation = 'german'

    def on_neolatin_notation_button_clicked(self):
        self.chord_notation = 'neo-latin'

    def on_footer_reset_button_clicked(self):
        self.footer_edit_box.setPlainText(self.settings.get_default_value('songs/footer template'))

    def load(self):
        self.settings.beginGroup(self.settings_section)
        self.tool_bar = self.settings.value('display songbar')
        self.update_edit = self.settings.value('update service on edit')
        self.update_load = self.settings.value('add song from service')
        self.songbook_slide = self.settings.value('add songbook slide')
        self.enable_chords = self.settings.value('enable chords')
        self.chord_notation = self.settings.value('chord notation')
        self.mainview_chords = self.settings.value('mainview chords')
        self.disable_chords_import = self.settings.value('disable chords import')
        self.tool_bar_active_check_box.setChecked(self.tool_bar)
        self.update_on_edit_check_box.setChecked(self.update_edit)
        self.add_from_service_check_box.setChecked(self.update_load)
        self.chords_group_box.setChecked(self.enable_chords)
        self.mainview_chords_check_box.setChecked(self.mainview_chords)
        self.disable_chords_import_check_box.setChecked(self.disable_chords_import)
        if self.chord_notation == 'german':
            self.german_notation_radio_button.setChecked(True)
        elif self.chord_notation == 'neo-latin':
            self.neolatin_notation_radio_button.setChecked(True)
        else:
            self.english_notation_radio_button.setChecked(True)
        self.footer_edit_box.setPlainText(self.settings.value('footer template'))
        self.settings.endGroup()

    def save(self):
        self.settings.beginGroup(self.settings_section)
        self.settings.setValue('display songbar', self.tool_bar)
        self.settings.setValue('update service on edit', self.update_edit)
        self.settings.setValue('add song from service', self.update_load)
        self.settings.setValue('enable chords', self.chords_group_box.isChecked())
        self.settings.setValue('mainview chords', self.mainview_chords)
        self.settings.setValue('disable chords import', self.disable_chords_import)
        self.settings.setValue('chord notation', self.chord_notation)
        # Only save footer template if it has been changed. This allows future updates
        if self.footer_edit_box.toPlainText() != self.settings.get_default_value('songs/footer template'):
            self.settings.setValue('footer template', self.footer_edit_box.toPlainText())
        self.settings.setValue('add songbook slide', self.songbook_slide)
        self.settings.endGroup()
        if self.tab_visited:
            self.self.settings_form.register_post_process('songs_config_updated')
        self.tab_visited = False
