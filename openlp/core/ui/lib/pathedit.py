# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2017 OpenLP Developers                                   #
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
from enum import Enum

from PyQt5 import QtCore, QtWidgets

from openlp.core.common.i18n import UiStrings, translate
from openlp.core.common.path import Path, path_to_str, str_to_path
from openlp.core.lib import build_icon
from openlp.core.ui.lib.filedialog import FileDialog


class PathType(Enum):
    Files = 1
    Directories = 2


class PathEdit(QtWidgets.QWidget):
    """
    The :class:`~openlp.core.ui.lib.pathedit.PathEdit` class subclasses QWidget to create a custom widget for use when
    a file or directory needs to be selected.
    """
    pathChanged = QtCore.pyqtSignal(Path)

    def __init__(self, parent=None, path_type=PathType.Files, default_path=None, dialog_caption=None, show_revert=True):
        """
        Initialise the PathEdit widget

        :param QtWidget.QWidget | None: The parent of the widget. This is just passed to the super method.
        :param str dialog_caption: Used to customise the caption in the QFileDialog.
        :param openlp.core.common.path.Path default_path: The default path. This is set as the path when the revert
            button is clicked
        :param bool show_revert: Used to determine if the 'revert button' should be visible.
        :rtype: None
        """
        super().__init__(parent)
        self.default_path = default_path
        self.dialog_caption = dialog_caption
        self._path_type = path_type
        self._path = None
        self.filters = '{all_files} (*)'.format(all_files=UiStrings().AllFiles)
        self._setup(show_revert)

    def _setup(self, show_revert):
        """
        Set up the widget
        :param bool show_revert: Show or hide the revert button
        :rtype: None
        """
        widget_layout = QtWidgets.QHBoxLayout()
        widget_layout.setContentsMargins(0, 0, 0, 0)
        self.line_edit = QtWidgets.QLineEdit(self)
        widget_layout.addWidget(self.line_edit)
        self.browse_button = QtWidgets.QToolButton(self)
        self.browse_button.setIcon(build_icon(':/general/general_open.png'))
        widget_layout.addWidget(self.browse_button)
        self.revert_button = QtWidgets.QToolButton(self)
        self.revert_button.setIcon(build_icon(':/general/general_revert.png'))
        self.revert_button.setVisible(show_revert)
        widget_layout.addWidget(self.revert_button)
        self.setLayout(widget_layout)
        # Signals and Slots
        self.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.revert_button.clicked.connect(self.on_revert_button_clicked)
        self.line_edit.editingFinished.connect(self.on_line_edit_editing_finished)
        self.update_button_tool_tips()

    @property
    def path(self):
        """
        A property getter method to return the selected path.

        :return: The selected path
        :rtype: openlp.core.common.path.Path
        """
        return self._path

    @path.setter
    def path(self, path):
        """
        A Property setter method to set the selected path

        :param openlp.core.common.path.Path path: The path to set the widget to
        :rtype: None
        """
        self._path = path
        text = path_to_str(path)
        self.line_edit.setText(text)
        self.line_edit.setToolTip(text)

    @property
    def path_type(self):
        """
        A property getter method to return the path_type. Path type allows you to sepecify if the user is restricted to
        selecting a file or directory.

        :return: The type selected
        :rtype: PathType
        """
        return self._path_type

    @path_type.setter
    def path_type(self, path_type):
        """
        A Property setter method to set the path type

        :param PathType path_type: The type of path to select
        :rtype: None
        """
        self._path_type = path_type
        self.update_button_tool_tips()

    def update_button_tool_tips(self):
        """
        Called to update the tooltips on the buttons. This is changing path types, and when the widget is initalised

        :rtype: None
        """
        if self._path_type == PathType.Directories:
            self.browse_button.setToolTip(translate('OpenLP.PathEdit', 'Browse for directory.'))
            self.revert_button.setToolTip(translate('OpenLP.PathEdit', 'Revert to default directory.'))
        else:
            self.browse_button.setToolTip(translate('OpenLP.PathEdit', 'Browse for file.'))
            self.revert_button.setToolTip(translate('OpenLP.PathEdit', 'Revert to default file.'))

    def on_browse_button_clicked(self):
        """
        A handler to handle a click on the browse button.

        Show the QFileDialog and process the input from the user

        :rtype: None
        """
        caption = self.dialog_caption
        path = None
        if self._path_type == PathType.Directories:
            if not caption:
                caption = translate('OpenLP.PathEdit', 'Select Directory')
            path = FileDialog.getExistingDirectory(self, caption, self._path, FileDialog.ShowDirsOnly)
        elif self._path_type == PathType.Files:
            if not caption:
                caption = self.dialog_caption = translate('OpenLP.PathEdit', 'Select File')
            path, filter_used = FileDialog.getOpenFileName(self, caption, self._path, self.filters)
        if path:
            self.on_new_path(path)

    def on_revert_button_clicked(self):
        """
        A handler to handle a click on the revert button.

        Set the new path to the value of the default_path instance variable.

        :rtype: None
        """
        self.on_new_path(self.default_path)

    def on_line_edit_editing_finished(self):
        """
        A handler to handle when the line edit has finished being edited.

        :rtype: None
        """
        path = str_to_path(self.line_edit.text())
        self.on_new_path(path)

    def on_new_path(self, path):
        """
        A method called to validate and set a new path.

        Emits the pathChanged Signal

        :param openlp.core.common.path.Path path: The new path
        :rtype: None
        """
        if self._path != path:
            self.path = path
            self.pathChanged.emit(path)