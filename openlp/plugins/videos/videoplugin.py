# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4
"""
OpenLP - Open Source Lyrics Projection
Copyright (c) 2008 Raoul Snyman
Portions copyright (c) 2008 Martin Thompson, Tim Bentley,

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
import os
from PyQt4 import QtCore, QtGui

from openlp.core.resources import *
from openlp.core.lib import Plugin,PluginUtils,  MediaManagerItem

class VideoPlugin(Plugin, PluginUtils):
    def __init__(self):
        # Call the parent constructor
        Plugin.__init__(self, 'Videos', '1.9.0')
        self.weight = -6
        # Create the plugin icon
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(':/media/media_video.png'),
            QtGui.QIcon.Normal, QtGui.QIcon.Off)

    def get_media_manager_item(self):
        # Create the MediaManagerItem object
        self.MediaManagerItem = MediaManagerItem(self.icon, 'Videos')
        # Add a toolbar
        self.MediaManagerItem.addToolbar()
        # Create buttons for the toolbar
        ## New Song Button ##
        self.MediaManagerItem.addToolbarButton('New Video', 'Load videos into openlp.org',
            ':/videos/video_load.png', self.onVideoNewClick, 'VideoNewItem')
        ## Delete Song Button ##
        self.MediaManagerItem.addToolbarButton('Delete Video', 'Delete the selected video',
            ':/videos/video_delete.png', self.onVideoDeleteClick, 'VideoDeleteItem')
        ## Separator Line ##
        self.MediaManagerItem.addToolbarSeparator()
        ## Preview Song Button ##
        self.MediaManagerItem.addToolbarButton('Preview Video', 'Preview the selected video',
            ':/system/system_preview.png', self.onVideoPreviewClick, 'VideoPreviewItem')
        ## Live Song Button ##
        self.MediaManagerItem.addToolbarButton('Go Live', 'Send the selected video live',
            ':/system/system_live.png', self.onVideoLiveClick, 'VideoLiveItem')
        ## Add Song Button ##
        self.MediaManagerItem.addToolbarButton('Add Video To Service',
            'Add the selected video(s) to the service', ':/system/system_add.png',
            self.onVideoAddClick, 'VideoAddItem')
        ## Add the videolist widget ##
        self.VideoListView = QtGui.QTableWidget()
        self.VideoListView.setColumnCount(2)
        self.VideoListView.setColumnHidden(0, True)
        self.VideoListView.setColumnWidth(1, 275)
        self.VideoListView.setShowGrid(False)
        self.VideoListView.setSortingEnabled(False)        
        self.VideoListView.setAlternatingRowColors(True)
        self.VideoListView.setHorizontalHeaderLabels(QtCore.QStringList(["","Name"]))  
        self.VideoListView.setAlternatingRowColors(True)
        self.VideoListView.setGeometry(QtCore.QRect(10, 100, 256, 591))
        self.VideoListView.setObjectName("VideoListView")
        self.MediaManagerItem.PageLayout.addWidget(self.VideoListView)
        
        #define and add the context menu
        self.VideoListView.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.VideoListView.addAction(self.add_to_context_menu(self.VideoListView, ':/system/system_preview.png', "&Preview Video", self.onVideoPreviewClick))      
        self.VideoListView.addAction(self.add_to_context_menu(self.VideoListView, ':/system/system_live.png', "&Show Live", self.onVideoLiveClick))        
        self.VideoListView.addAction(self.add_to_context_menu(self.VideoListView, ':/system/system_add.png', "&Add to Service", self.onVideoAddClick))     
        return self.MediaManagerItem

    def initialise(self):
        list = self._load_display_list()
        self._load_video_list(list)     

    def onVideoNewClick(self):
        files = QtGui.QFileDialog.getOpenFileNames(None, "Select Image(s)", self._get_last_dir(), "Images (*.avi *.mpeg)")
        if len(files) > 0:
            self._load_video_list(files)
            self._save_last_directory(files[0])
            self._save_display_list(self.VideoListView) 

    def _load_video_list(self, list):
        for f in list:
            fl ,  nm = os.path.split(str(f))            
            c = self.VideoListView.rowCount()
            self.VideoListView.setRowCount(c+1)
            twi = QtGui.QTableWidgetItem(str(f))
            self.VideoListView.setItem(c , 0, twi)
            twi = QtGui.QTableWidgetItem(str(nm))
            self.VideoListView.setItem(c , 1, twi)
            self.VideoListView.setRowHeight(c, 20)        
            
    def onVideoDeleteClick(self):
        cr = self.VideoListView.currentRow()
        self.VideoListView.removeRow(int(cr))
        self._save_display_list(self.VideoListView)     

    def onVideoPreviewClick(self):
        pass

    def onVideoLiveClick(self):
        pass

    def onVideoAddClick(self):
        pass
