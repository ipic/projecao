# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2009 Raoul Snyman                                        #
# Portions copyright (c) 2008-2009 Martin Thompson, Tim Bentley, Carsten      #
# Tinggaard, Jon Tibble, Jonathan Corwin, Maikel Stuivenberg, Scott Guerrieri #
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

from PyQt4 import QtCore, QtGui

class Ui_OpenLPImportDialog(object):
    def setupUi(self, OpenLPImportDialog):
        OpenLPImportDialog.setObjectName(u'OpenLPImportDialog')
        OpenLPImportDialog.resize(473, 459)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(u':/icon/openlp.org-icon-32.bmp'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        OpenLPImportDialog.setWindowIcon(icon)
        self.verticalLayout_5 = QtGui.QVBoxLayout(OpenLPImportDialog)
        self.verticalLayout_5.setMargin(8)
        self.verticalLayout_5.setObjectName(u'verticalLayout_5')
        self.ImportFileWidget = QtGui.QWidget(OpenLPImportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImportFileWidget.sizePolicy().hasHeightForWidth())
        self.ImportFileWidget.setSizePolicy(sizePolicy)
        self.ImportFileWidget.setObjectName(u'ImportFileWidget')
        self.horizontalLayout = QtGui.QHBoxLayout(self.ImportFileWidget)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(u'horizontalLayout')
        self.ImportFileLabel = QtGui.QLabel(self.ImportFileWidget)
        self.ImportFileLabel.setObjectName(u'ImportFileLabel')
        self.horizontalLayout.addWidget(self.ImportFileLabel)
        self.ImportFileLineEdit = QtGui.QLineEdit(self.ImportFileWidget)
        self.ImportFileLineEdit.setObjectName(u'ImportFileLineEdit')
        self.horizontalLayout.addWidget(self.ImportFileLineEdit)
        self.ImportFileSelectPushButton = QtGui.QPushButton(self.ImportFileWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(u':/imports/import_load.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ImportFileSelectPushButton.setIcon(icon1)
        self.ImportFileSelectPushButton.setObjectName(u'ImportFileSelectPushButton')
        self.horizontalLayout.addWidget(self.ImportFileSelectPushButton)
        self.verticalLayout_5.addWidget(self.ImportFileWidget)
        self.SongListFrame = QtGui.QFrame(OpenLPImportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SongListFrame.sizePolicy().hasHeightForWidth())
        self.SongListFrame.setSizePolicy(sizePolicy)
        self.SongListFrame.setFrameShape(QtGui.QFrame.Box)
        self.SongListFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.SongListFrame.setObjectName(u'SongListFrame')
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.SongListFrame)
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setMargin(8)
        self.horizontalLayout_6.setObjectName(u'horizontalLayout_6')
        self.ImportFileSongListWidget = QtGui.QWidget(self.SongListFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImportFileSongListWidget.sizePolicy().hasHeightForWidth())
        self.ImportFileSongListWidget.setSizePolicy(sizePolicy)
        self.ImportFileSongListWidget.setObjectName(u'ImportFileSongListWidget')
        self.verticalLayout = QtGui.QVBoxLayout(self.ImportFileSongListWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(u'verticalLayout')
        self.ImportListLabel = QtGui.QLabel(self.ImportFileSongListWidget)
        self.ImportListLabel.setObjectName(u'ImportListLabel')
        self.verticalLayout.addWidget(self.ImportListLabel)
        self.ImportListTable = QtGui.QTableWidget(self.ImportFileSongListWidget)
        self.ImportListTable.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.ImportListTable.setShowGrid(False)
        self.ImportListTable.setWordWrap(False)
        self.ImportListTable.setCornerButtonEnabled(False)
        self.ImportListTable.setObjectName(u'ImportListTable')
        self.ImportListTable.setColumnCount(2)
        self.ImportListTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.ImportListTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.ImportListTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.ImportListTable)
        self.ImportSelectAllWidget = QtGui.QWidget(self.ImportFileSongListWidget)
        self.ImportSelectAllWidget.setObjectName(u'ImportSelectAllWidget')
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.ImportSelectAllWidget)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(u'horizontalLayout_2')
        self.ImportSelectAllPushButton = QtGui.QPushButton(self.ImportSelectAllWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImportSelectAllPushButton.sizePolicy().hasHeightForWidth())
        self.ImportSelectAllPushButton.setSizePolicy(sizePolicy)
        self.ImportSelectAllPushButton.setMinimumSize(QtCore.QSize(100, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(u':/imports/import_selectall.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ImportSelectAllPushButton.setIcon(icon2)
        self.ImportSelectAllPushButton.setObjectName(u'ImportSelectAllPushButton')
        self.horizontalLayout_2.addWidget(self.ImportSelectAllPushButton)
        spacerItem = QtGui.QSpacerItem(89, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.ImportSelectAllWidget)
        self.importFilterWidget = QtGui.QWidget(self.ImportFileSongListWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importFilterWidget.sizePolicy().hasHeightForWidth())
        self.importFilterWidget.setSizePolicy(sizePolicy)
        self.importFilterWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.importFilterWidget.setObjectName(u'importFilterWidget')
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.importFilterWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(u'horizontalLayout_3')
        self.ImportFilterComboBox = QtGui.QComboBox(self.importFilterWidget)
        self.ImportFilterComboBox.setMinimumSize(QtCore.QSize(70, 0))
        self.ImportFilterComboBox.setObjectName(u'ImportFilterComboBox')
        self.ImportFilterComboBox.addItem(QtCore.QString())
        self.ImportFilterComboBox.addItem(QtCore.QString())
        self.ImportFilterComboBox.addItem(QtCore.QString())
        self.horizontalLayout_3.addWidget(self.ImportFilterComboBox)
        self.importFilterLineEdit = QtGui.QLineEdit(self.importFilterWidget)
        self.importFilterLineEdit.setObjectName(u'importFilterLineEdit')
        self.horizontalLayout_3.addWidget(self.importFilterLineEdit)
        self.verticalLayout.addWidget(self.importFilterWidget)
        self.horizontalLayout_6.addWidget(self.ImportFileSongListWidget)
        self.AddSelectedWidget = QtGui.QWidget(self.SongListFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddSelectedWidget.sizePolicy().hasHeightForWidth())
        self.AddSelectedWidget.setSizePolicy(sizePolicy)
        self.AddSelectedWidget.setObjectName(u'AddSelectedWidget')
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.AddSelectedWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(u'verticalLayout_3')
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.AddSelectedPushButton = QtGui.QPushButton(self.AddSelectedWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddSelectedPushButton.sizePolicy().hasHeightForWidth())
        self.AddSelectedPushButton.setSizePolicy(sizePolicy)
        self.AddSelectedPushButton.setMinimumSize(QtCore.QSize(25, 25))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(u':/imports/import_move_to_list.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AddSelectedPushButton.setIcon(icon3)
        self.AddSelectedPushButton.setObjectName(u'AddSelectedPushButton')
        self.verticalLayout_3.addWidget(self.AddSelectedPushButton)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_6.addWidget(self.AddSelectedWidget)
        self.SelectedFileListWidget = QtGui.QWidget(self.SongListFrame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedFileListWidget.sizePolicy().hasHeightForWidth())
        self.SelectedFileListWidget.setSizePolicy(sizePolicy)
        self.SelectedFileListWidget.setObjectName(u'SelectedFileListWidget')
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.SelectedFileListWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(u'verticalLayout_2')
        self.SelectedListLabel = QtGui.QLabel(self.SelectedFileListWidget)
        self.SelectedListLabel.setObjectName(u'SelectedListLabel')
        self.verticalLayout_2.addWidget(self.SelectedListLabel)
        self.SelectedListTable = QtGui.QTableWidget(self.SelectedFileListWidget)
        self.SelectedListTable.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.SelectedListTable.setShowGrid(False)
        self.SelectedListTable.setWordWrap(False)
        self.SelectedListTable.setCornerButtonEnabled(False)
        self.SelectedListTable.setObjectName(u'SelectedListTable')
        self.SelectedListTable.setColumnCount(2)
        self.SelectedListTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.SelectedListTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.SelectedListTable.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.SelectedListTable)
        self.SelectedSelectAllWidget = QtGui.QWidget(self.SelectedFileListWidget)
        self.SelectedSelectAllWidget.setObjectName(u'SelectedSelectAllWidget')
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.SelectedSelectAllWidget)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(u'horizontalLayout_4')
        self.SelectedSelectAllPushButton = QtGui.QPushButton(self.SelectedSelectAllWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedSelectAllPushButton.sizePolicy().hasHeightForWidth())
        self.SelectedSelectAllPushButton.setSizePolicy(sizePolicy)
        self.SelectedSelectAllPushButton.setMinimumSize(QtCore.QSize(100, 0))
        self.SelectedSelectAllPushButton.setIcon(icon2)
        self.SelectedSelectAllPushButton.setObjectName(u'SelectedSelectAllPushButton')
        self.horizontalLayout_4.addWidget(self.SelectedSelectAllPushButton)
        spacerItem3 = QtGui.QSpacerItem(92, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_2.addWidget(self.SelectedSelectAllWidget)
        self.SelectedRemoveSelectedWidget = QtGui.QWidget(self.SelectedFileListWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedRemoveSelectedWidget.sizePolicy().hasHeightForWidth())
        self.SelectedRemoveSelectedWidget.setSizePolicy(sizePolicy)
        self.SelectedRemoveSelectedWidget.setObjectName(u'SelectedRemoveSelectedWidget')
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.SelectedRemoveSelectedWidget)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(u'horizontalLayout_5')
        self.SelectedRemoveSelectedButton = QtGui.QPushButton(self.SelectedRemoveSelectedWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SelectedRemoveSelectedButton.sizePolicy().hasHeightForWidth())
        self.SelectedRemoveSelectedButton.setSizePolicy(sizePolicy)
        self.SelectedRemoveSelectedButton.setMinimumSize(QtCore.QSize(140, 0))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(u':/imports/import_remove.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SelectedRemoveSelectedButton.setIcon(icon4)
        self.SelectedRemoveSelectedButton.setObjectName(u'SelectedRemoveSelectedButton')
        self.horizontalLayout_5.addWidget(self.SelectedRemoveSelectedButton)
        spacerItem4 = QtGui.QSpacerItem(49, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.verticalLayout_2.addWidget(self.SelectedRemoveSelectedWidget)
        self.horizontalLayout_6.addWidget(self.SelectedFileListWidget)
        self.verticalLayout_5.addWidget(self.SongListFrame)
        self.ProgressGroupBox = QtGui.QGroupBox(OpenLPImportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ProgressGroupBox.sizePolicy().hasHeightForWidth())
        self.ProgressGroupBox.setSizePolicy(sizePolicy)
        self.ProgressGroupBox.setObjectName(u'ProgressGroupBox')
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ProgressGroupBox)
        self.verticalLayout_4.setSpacing(8)
        self.verticalLayout_4.setContentsMargins(8, 0, 8, 8)
        self.verticalLayout_4.setObjectName(u'verticalLayout_4')
        self.ProgressLabel = QtGui.QLabel(self.ProgressGroupBox)
        self.ProgressLabel.setObjectName(u'ProgressLabel')
        self.verticalLayout_4.addWidget(self.ProgressLabel)
        self.ProgressBar = QtGui.QProgressBar(self.ProgressGroupBox)
        self.ProgressBar.setProperty(u'value', QtCore.QVariant(24))
        self.ProgressBar.setObjectName(u'ProgressBar')
        self.verticalLayout_4.addWidget(self.ProgressBar)
        self.verticalLayout_5.addWidget(self.ProgressGroupBox)
        self.ButtonBarWidget = QtGui.QWidget(OpenLPImportDialog)
        self.ButtonBarWidget.setObjectName(u'ButtonBarWidget')
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.ButtonBarWidget)
        self.horizontalLayout_7.setSpacing(8)
        self.horizontalLayout_7.setMargin(0)
        self.horizontalLayout_7.setObjectName(u'horizontalLayout_7')
        spacerItem5 = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.ImportPushButton = QtGui.QPushButton(self.ButtonBarWidget)
        self.ImportPushButton.setObjectName(u'ImportPushButton')
        self.horizontalLayout_7.addWidget(self.ImportPushButton)
        self.ClosePushButton = QtGui.QPushButton(self.ButtonBarWidget)
        self.ClosePushButton.setObjectName(u'ClosePushButton')
        self.horizontalLayout_7.addWidget(self.ClosePushButton)
        self.verticalLayout_5.addWidget(self.ButtonBarWidget)

        self.retranslateUi(OpenLPImportDialog)
        QtCore.QObject.connect(self.ClosePushButton, QtCore.SIGNAL(u'clicked()'), OpenLPImportDialog.close)
        QtCore.QObject.connect(self.ImportSelectAllPushButton, QtCore.SIGNAL(u'clicked()'), self.ImportListTable.selectAll)
        QtCore.QObject.connect(self.SelectedSelectAllPushButton, QtCore.SIGNAL(u'clicked()'), self.SelectedListTable.selectAll)
        QtCore.QObject.connect(self.SelectedRemoveSelectedButton, QtCore.SIGNAL(u'clicked()'), self.SelectedListTable.clear)
        QtCore.QMetaObject.connectSlotsByName(OpenLPImportDialog)

    def retranslateUi(self, OpenLPImportDialog):
        OpenLPImportDialog.setWindowTitle(self.trUtf8(u'openlp.org Song Importer'))
        self.ImportFileLabel.setText(self.trUtf8(u'Select openlp.org songfile to import:'))
        self.ImportListLabel.setText(self.trUtf8(u'Import File Song List'))
        self.ImportListTable.horizontalHeaderItem(0).setText(self.trUtf8(u'Song Title'))
        self.ImportListTable.horizontalHeaderItem(1).setText(self.trUtf8(u'Author'))
        self.ImportSelectAllPushButton.setText(self.trUtf8(u'Select All'))
        self.ImportFilterComboBox.setItemText(0, self.trUtf8(u'Lyrics'))
        self.ImportFilterComboBox.setItemText(1, self.trUtf8(u'Title'))
        self.ImportFilterComboBox.setItemText(2, self.trUtf8(u'Author'))
        self.SelectedListLabel.setText(self.trUtf8(u'Song Import List'))
        self.SelectedListTable.horizontalHeaderItem(0).setText(self.trUtf8(u'Song Title'))
        self.SelectedListTable.horizontalHeaderItem(1).setText(self.trUtf8(u'Author'))
        self.SelectedSelectAllPushButton.setText(self.trUtf8(u'Select All'))
        self.SelectedRemoveSelectedButton.setText(self.trUtf8(u'Remove Selected'))
        self.ProgressGroupBox.setTitle(self.trUtf8(u'Progress:'))
        self.ProgressLabel.setText(self.trUtf8(u'Ready to import'))
        self.ImportPushButton.setText(self.trUtf8(u'Import'))
        self.ClosePushButton.setText(self.trUtf8(u'Close'))

