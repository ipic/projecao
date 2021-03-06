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
"""
The :mod:`advancedtab` provides an advanced settings facility.
"""
import logging
from datetime import datetime, timedelta

from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.common import SlideLimits
from openlp.core.common.applocation import AppLocation
from openlp.core.common.i18n import UiStrings, format_time, translate
from openlp.core.common.settings import Settings
from openlp.core.lib.settingstab import SettingsTab
from openlp.core.ui.icons import UiIcons
from openlp.core.ui.style import HAS_DARK_STYLE
from openlp.core.widgets.edits import PathEdit
from openlp.core.widgets.enums import PathEditType
from openlp.core.widgets.widgets import ProxyWidget


log = logging.getLogger(__name__)


class AdvancedTab(SettingsTab):
    """
    The :class:`AdvancedTab` manages the advanced settings tab including the UI
    and the loading and saving of the displayed settings.
    """
    def __init__(self, parent):
        """
        Initialise the settings tab
        """
        self.data_exists = False
        self.icon_path = UiIcons().settings
        self.autoscroll_map = [None, {'dist': -1, 'pos': 0}, {'dist': -1, 'pos': 1}, {'dist': -1, 'pos': 2},
                               {'dist': 0, 'pos': 0}, {'dist': 0, 'pos': 1}, {'dist': 0, 'pos': 2},
                               {'dist': 0, 'pos': 3}, {'dist': 1, 'pos': 0}, {'dist': 1, 'pos': 1},
                               {'dist': 1, 'pos': 2}, {'dist': 1, 'pos': 3}]
        advanced_translated = translate('OpenLP.AdvancedTab', 'Advanced')
        super(AdvancedTab, self).__init__(parent, 'Advanced', advanced_translated)

    def setup_ui(self):
        """
        Configure the UI elements for the tab.
        """
        self.setObjectName('AdvancedTab')
        super(AdvancedTab, self).setup_ui()
        self.ui_group_box = QtWidgets.QGroupBox(self.left_column)
        self.ui_group_box.setObjectName('ui_group_box')
        self.ui_layout = QtWidgets.QFormLayout(self.ui_group_box)
        self.ui_layout.setObjectName('ui_layout')
        self.recent_label = QtWidgets.QLabel(self.ui_group_box)
        self.recent_label.setObjectName('recent_label')
        self.recent_spin_box = QtWidgets.QSpinBox(self.ui_group_box)
        self.recent_spin_box.setObjectName('recent_spin_box')
        self.recent_spin_box.setMinimum(0)
        self.ui_layout.addRow(self.recent_label, self.recent_spin_box)
        self.media_plugin_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.media_plugin_check_box.setObjectName('media_plugin_check_box')
        self.ui_layout.addRow(self.media_plugin_check_box)
        self.hide_mouse_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.hide_mouse_check_box.setObjectName('hide_mouse_check_box')
        self.ui_layout.addRow(self.hide_mouse_check_box)
        self.double_click_live_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.double_click_live_check_box.setObjectName('double_click_live_check_box')
        self.ui_layout.addRow(self.double_click_live_check_box)
        self.single_click_preview_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.single_click_preview_check_box.setObjectName('single_click_preview_check_box')
        self.ui_layout.addRow(self.single_click_preview_check_box)
        self.single_click_service_preview_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.single_click_service_preview_check_box.setObjectName('single_click_service_preview_check_box')
        self.ui_layout.addRow(self.single_click_service_preview_check_box)
        self.expand_service_item_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.expand_service_item_check_box.setObjectName('expand_service_item_check_box')
        self.ui_layout.addRow(self.expand_service_item_check_box)
        self.slide_max_height_label = QtWidgets.QLabel(self.ui_group_box)
        self.slide_max_height_label.setObjectName('slide_max_height_label')
        self.slide_max_height_combo_box = QtWidgets.QComboBox(self.ui_group_box)
        self.slide_max_height_combo_box.addItem('', userData=0)
        self.slide_max_height_combo_box.addItem('', userData=-4)
        # Generate numeric values for combo box dynamically
        for px in range(60, 801, 5):
            self.slide_max_height_combo_box.addItem(str(px) + 'px', userData=px)
        self.slide_max_height_combo_box.setObjectName('slide_max_height_combo_box')
        self.ui_layout.addRow(self.slide_max_height_label, self.slide_max_height_combo_box)
        self.autoscroll_label = QtWidgets.QLabel(self.ui_group_box)
        self.autoscroll_label.setObjectName('autoscroll_label')
        self.autoscroll_combo_box = QtWidgets.QComboBox(self.ui_group_box)
        self.autoscroll_combo_box.addItems(['', '', '', '', '', '', '', '', '', '', '', ''])
        self.autoscroll_combo_box.setObjectName('autoscroll_combo_box')
        self.ui_layout.addRow(self.autoscroll_label)
        self.ui_layout.addRow(self.autoscroll_combo_box)
        self.search_as_type_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.search_as_type_check_box.setObjectName('SearchAsType_check_box')
        self.ui_layout.addRow(self.search_as_type_check_box)
        self.enable_auto_close_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.enable_auto_close_check_box.setObjectName('enable_auto_close_check_box')
        self.ui_layout.addRow(self.enable_auto_close_check_box)
        self.experimental_check_box = QtWidgets.QCheckBox(self.ui_group_box)
        self.experimental_check_box.setObjectName('experimental_check_box')
        self.ui_layout.addRow(self.experimental_check_box)
        self.left_layout.addWidget(self.ui_group_box)
        if HAS_DARK_STYLE:
            self.use_dark_style_checkbox = QtWidgets.QCheckBox(self.ui_group_box)
            self.use_dark_style_checkbox.setObjectName('use_dark_style_checkbox')
            self.ui_layout.addRow(self.use_dark_style_checkbox)
        # Service Item Slide Limits
        self.slide_group_box = QtWidgets.QGroupBox(self.left_column)
        self.slide_group_box.setObjectName('slide_group_box')
        self.slide_layout = QtWidgets.QVBoxLayout(self.slide_group_box)
        self.slide_layout.setObjectName('slide_layout')
        self.slide_label = QtWidgets.QLabel(self.slide_group_box)
        self.slide_label.setWordWrap(True)
        self.slide_layout.addWidget(self.slide_label)
        self.end_slide_radio_button = QtWidgets.QRadioButton(self.slide_group_box)
        self.end_slide_radio_button.setObjectName('end_slide_radio_button')
        self.slide_layout.addWidget(self.end_slide_radio_button)
        self.wrap_slide_radio_button = QtWidgets.QRadioButton(self.slide_group_box)
        self.wrap_slide_radio_button.setObjectName('wrap_slide_radio_button')
        self.slide_layout.addWidget(self.wrap_slide_radio_button)
        self.next_item_radio_button = QtWidgets.QRadioButton(self.slide_group_box)
        self.next_item_radio_button.setObjectName('next_item_radio_button')
        self.slide_layout.addWidget(self.next_item_radio_button)
        self.left_layout.addWidget(self.slide_group_box)
        # Data Directory
        self.data_directory_group_box = QtWidgets.QGroupBox(self.left_column)
        self.data_directory_group_box.setObjectName('data_directory_group_box')
        self.data_directory_layout = QtWidgets.QFormLayout(self.data_directory_group_box)
        self.data_directory_layout.setObjectName('data_directory_layout')
        self.data_directory_new_label = QtWidgets.QLabel(self.data_directory_group_box)
        self.data_directory_new_label.setObjectName('data_directory_current_label')
        self.data_directory_path_edit = PathEdit(self.data_directory_group_box, path_type=PathEditType.Directories,
                                                 default_path=AppLocation.get_directory(AppLocation.DataDir))
        self.data_directory_layout.addRow(self.data_directory_new_label, self.data_directory_path_edit)
        self.new_data_directory_has_files_label = QtWidgets.QLabel(self.data_directory_group_box)
        self.new_data_directory_has_files_label.setObjectName('new_data_directory_has_files_label')
        self.new_data_directory_has_files_label.setWordWrap(True)
        self.data_directory_cancel_button = QtWidgets.QToolButton(self.data_directory_group_box)
        self.data_directory_cancel_button.setObjectName('data_directory_cancel_button')
        self.data_directory_cancel_button.setIcon(UiIcons().delete)
        self.data_directory_copy_check_layout = QtWidgets.QHBoxLayout()
        self.data_directory_copy_check_layout.setObjectName('data_directory_copy_check_layout')
        self.data_directory_copy_check_box = QtWidgets.QCheckBox(self.data_directory_group_box)
        self.data_directory_copy_check_box.setObjectName('data_directory_copy_check_box')
        self.data_directory_copy_check_layout.addWidget(self.data_directory_copy_check_box)
        self.data_directory_copy_check_layout.addStretch()
        self.data_directory_copy_check_layout.addWidget(self.data_directory_cancel_button)
        self.data_directory_layout.addRow(self.data_directory_copy_check_layout)
        self.data_directory_layout.addRow(self.new_data_directory_has_files_label)
        self.left_layout.addWidget(self.data_directory_group_box)
        # Display Workarounds
        self.display_workaround_group_box = QtWidgets.QGroupBox(self.right_column)
        self.display_workaround_group_box.setObjectName('display_workaround_group_box')
        self.display_workaround_layout = QtWidgets.QVBoxLayout(self.display_workaround_group_box)
        self.display_workaround_layout.setObjectName('display_workaround_layout')
        self.ignore_aspect_ratio_check_box = QtWidgets.QCheckBox(self.display_workaround_group_box)
        self.ignore_aspect_ratio_check_box.setObjectName('ignore_aspect_ratio_check_box')
        self.display_workaround_layout.addWidget(self.ignore_aspect_ratio_check_box)
        self.x11_bypass_check_box = QtWidgets.QCheckBox(self.display_workaround_group_box)
        self.x11_bypass_check_box.setObjectName('x11_bypass_check_box')
        self.display_workaround_layout.addWidget(self.x11_bypass_check_box)
        self.alternate_rows_check_box = QtWidgets.QCheckBox(self.display_workaround_group_box)
        self.alternate_rows_check_box.setObjectName('alternate_rows_check_box')
        self.display_workaround_layout.addWidget(self.alternate_rows_check_box)
        self.right_layout.addWidget(self.display_workaround_group_box)
        # Default service name
        self.service_name_group_box = QtWidgets.QGroupBox(self.right_column)
        self.service_name_group_box.setObjectName('service_name_group_box')
        self.service_name_layout = QtWidgets.QFormLayout(self.service_name_group_box)
        self.service_name_check_box = QtWidgets.QCheckBox(self.service_name_group_box)
        self.service_name_check_box.setObjectName('service_name_check_box')
        self.service_name_layout.setObjectName('service_name_layout')
        self.service_name_layout.addRow(self.service_name_check_box)
        self.service_name_time_label = QtWidgets.QLabel(self.service_name_group_box)
        self.service_name_time_label.setObjectName('service_name_time_label')
        self.service_name_day = QtWidgets.QComboBox(self.service_name_group_box)
        self.service_name_day.addItems(['', '', '', '', '', '', '', ''])
        self.service_name_day.setObjectName('service_name_day')
        self.service_name_time = QtWidgets.QTimeEdit(self.service_name_group_box)
        self.service_name_time.setObjectName('service_name_time')
        self.service_name_time_layout = QtWidgets.QHBoxLayout()
        self.service_name_time_layout.setObjectName('service_name_time_layout')
        self.service_name_time_layout.addWidget(self.service_name_day)
        self.service_name_time_layout.addWidget(self.service_name_time)
        self.service_name_layout.addRow(self.service_name_time_label, self.service_name_time_layout)
        self.service_name_label = QtWidgets.QLabel(self.service_name_group_box)
        self.service_name_label.setObjectName('service_name_label')
        self.service_name_edit = QtWidgets.QLineEdit(self.service_name_group_box)
        self.service_name_edit.setObjectName('service_name_edit')
        self.service_name_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'[^/\\?*|<>\[\]":+]+'), self))
        self.service_name_revert_button = QtWidgets.QToolButton(self.service_name_group_box)
        self.service_name_revert_button.setObjectName('service_name_revert_button')
        self.service_name_revert_button.setIcon(UiIcons().undo)
        self.service_name_button_layout = QtWidgets.QHBoxLayout()
        self.service_name_button_layout.setObjectName('service_name_button_layout')
        self.service_name_button_layout.addWidget(self.service_name_edit)
        self.service_name_button_layout.addWidget(self.service_name_revert_button)
        self.service_name_layout.addRow(self.service_name_label, self.service_name_button_layout)
        self.service_name_example_label = QtWidgets.QLabel(self.service_name_group_box)
        self.service_name_example_label.setObjectName('service_name_example_label')
        self.service_name_example = QtWidgets.QLabel(self.service_name_group_box)
        self.service_name_example.setObjectName('service_name_example')
        self.service_name_layout.addRow(self.service_name_example_label, self.service_name_example)
        self.right_layout.addWidget(self.service_name_group_box)
        # Proxies
        self.proxy_widget = ProxyWidget(self.right_column)
        self.right_layout.addWidget(self.proxy_widget)
        # After the last item on each side, add some spacing
        self.left_layout.addStretch()
        self.right_layout.addStretch()
        # Set up all the connections and things
        self.should_update_service_name_example = False
        self.service_name_check_box.toggled.connect(self.service_name_check_box_toggled)
        self.service_name_day.currentIndexChanged.connect(self.on_service_name_day_changed)
        self.service_name_time.timeChanged.connect(self.update_service_name_example)
        self.service_name_edit.textChanged.connect(self.update_service_name_example)
        self.service_name_revert_button.clicked.connect(self.on_service_name_revert_button_clicked)
        self.alternate_rows_check_box.toggled.connect(self.on_alternate_rows_check_box_toggled)
        self.data_directory_path_edit.pathChanged.connect(self.on_data_directory_path_edit_path_changed)
        self.data_directory_cancel_button.clicked.connect(self.on_data_directory_cancel_button_clicked)
        self.data_directory_copy_check_box.toggled.connect(self.on_data_directory_copy_check_box_toggled)
        self.end_slide_radio_button.clicked.connect(self.on_end_slide_button_clicked)
        self.wrap_slide_radio_button.clicked.connect(self.on_wrap_slide_button_clicked)
        self.next_item_radio_button.clicked.connect(self.on_next_item_button_clicked)
        self.search_as_type_check_box.stateChanged.connect(self.on_search_as_type_check_box_changed)

    def retranslate_ui(self):
        """
        Setup the interface translation strings.
        """
        self.tab_title_visible = UiStrings().Advanced
        self.ui_group_box.setTitle(translate('OpenLP.AdvancedTab', 'UI Settings'))
        self.data_directory_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Data Location'))
        self.recent_label.setText(translate('OpenLP.AdvancedTab', 'Number of recent service files to display:'))
        self.media_plugin_check_box.setText(translate('OpenLP.AdvancedTab',
                                                      'Open the last used Library tab on startup'))
        self.double_click_live_check_box.setText(translate('OpenLP.AdvancedTab',
                                                           'Double-click to send items straight to Live'))
        self.single_click_preview_check_box.setText(translate('OpenLP.AdvancedTab',
                                                              'Preview items when clicked in Library'))
        self.single_click_service_preview_check_box.setText(translate('OpenLP.AdvancedTab',
                                                                      'Preview items when clicked in Service'))
        self.expand_service_item_check_box.setText(translate('OpenLP.AdvancedTab',
                                                             'Expand new service items on creation'))
        self.slide_max_height_label.setText(translate('OpenLP.AdvancedTab',
                                                      'Max height for non-text slides\nin slide controller:'))
        self.slide_max_height_combo_box.setItemText(0, translate('OpenLP.AdvancedTab', 'Disabled'))
        self.slide_max_height_combo_box.setItemText(1, translate('OpenLP.AdvancedTab', 'Automatic'))
        self.autoscroll_label.setText(translate('OpenLP.AdvancedTab',
                                                'When changing slides:'))
        self.autoscroll_combo_box.setItemText(0, translate('OpenLP.AdvancedTab', 'Do not auto-scroll'))
        self.autoscroll_combo_box.setItemText(1, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the previous slide into view'))
        self.autoscroll_combo_box.setItemText(2, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the previous slide to top'))
        self.autoscroll_combo_box.setItemText(3, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the previous slide to middle'))
        self.autoscroll_combo_box.setItemText(4, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the current slide into view'))
        self.autoscroll_combo_box.setItemText(5, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the current slide to top'))
        self.autoscroll_combo_box.setItemText(6, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the current slide to middle'))
        self.autoscroll_combo_box.setItemText(7, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the current slide to bottom'))
        self.autoscroll_combo_box.setItemText(8, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the next slide into view'))
        self.autoscroll_combo_box.setItemText(9, translate('OpenLP.AdvancedTab',
                                                           'Auto-scroll the next slide to top'))
        self.autoscroll_combo_box.setItemText(10, translate('OpenLP.AdvancedTab',
                                                            'Auto-scroll the next slide to middle'))
        self.autoscroll_combo_box.setItemText(11, translate('OpenLP.AdvancedTab',
                                                            'Auto-scroll the next slide to bottom'))
        self.enable_auto_close_check_box.setText(translate('OpenLP.AdvancedTab',
                                                           'Enable application exit confirmation'))
        self.experimental_check_box.setText(translate('OpenLP.GeneralTab',
                                                      'Experimental features (use at your own risk)'))
        if HAS_DARK_STYLE:
            self.use_dark_style_checkbox.setText(translate('OpenLP.AdvancedTab', 'Use dark style (needs restart)'))
        self.service_name_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Default Service Name'))
        self.service_name_check_box.setText(translate('OpenLP.AdvancedTab', 'Enable default service name'))
        self.service_name_time_label.setText(translate('OpenLP.AdvancedTab', 'Date and Time:'))
        self.service_name_day.setItemText(0, translate('OpenLP.AdvancedTab', 'Monday'))
        self.service_name_day.setItemText(1, translate('OpenLP.AdvancedTab', 'Tuesday'))
        self.service_name_day.setItemText(2, translate('OpenLP.AdvancedTab', 'Wednesday'))
        self.service_name_day.setItemText(3, translate('OpenLP.AdvancedTab', 'Thursday'))
        self.service_name_day.setItemText(4, translate('OpenLP.AdvancedTab', 'Friday'))
        self.service_name_day.setItemText(5, translate('OpenLP.AdvancedTab', 'Saturday'))
        self.service_name_day.setItemText(6, translate('OpenLP.AdvancedTab', 'Sunday'))
        self.service_name_day.setItemText(7, translate('OpenLP.AdvancedTab', 'Now'))
        self.service_name_time.setToolTip(translate('OpenLP.AdvancedTab', 'Time when usual service starts.'))
        self.service_name_label.setText(translate('OpenLP.AdvancedTab', 'Name:'))
        self.service_name_edit.setToolTip(translate('OpenLP.AdvancedTab', 'Consult the OpenLP manual for usage.'))
        self.service_name_revert_button.setToolTip(
            translate('OpenLP.AdvancedTab',
                      'Revert to the default service name "{name}".').format(name=UiStrings().DefaultServiceName))
        self.service_name_example_label.setText(translate('OpenLP.AdvancedTab', 'Example:'))
        self.hide_mouse_check_box.setText(translate('OpenLP.AdvancedTab', 'Hide mouse cursor when over display window'))
        self.data_directory_new_label.setText(translate('OpenLP.AdvancedTab', 'Path:'))
        self.data_directory_cancel_button.setText(translate('OpenLP.AdvancedTab', 'Cancel'))
        self.data_directory_cancel_button.setToolTip(
            translate('OpenLP.AdvancedTab', 'Cancel OpenLP data directory location change.'))
        self.data_directory_copy_check_box.setText(translate('OpenLP.AdvancedTab', 'Copy data to new location.'))
        self.data_directory_copy_check_box.setToolTip(translate(
            'OpenLP.AdvancedTab', 'Copy the OpenLP data files to the new location.'))
        self.new_data_directory_has_files_label.setText(
            translate('OpenLP.AdvancedTab', '<strong>WARNING:</strong> New data directory location contains '
                      'OpenLP data files.  These files WILL be replaced during a copy.'))
        self.display_workaround_group_box.setTitle(translate('OpenLP.AdvancedTab', 'Display Workarounds'))
        self.ignore_aspect_ratio_check_box.setText(translate('OpenLP.AdvancedTab', 'Ignore Aspect Ratio'))
        self.x11_bypass_check_box.setText(translate('OpenLP.AdvancedTab', 'Bypass X11 Window Manager'))
        self.alternate_rows_check_box.setText(translate('OpenLP.AdvancedTab', 'Use alternating row colours in lists'))
        # Slide Limits
        self.slide_group_box.setTitle(translate('OpenLP.GeneralTab', 'Service Item Slide Limits'))
        self.slide_label.setText(translate('OpenLP.GeneralTab', 'Behavior of next/previous on the last/first slide:'))
        self.end_slide_radio_button.setText(translate('OpenLP.GeneralTab', '&Remain on Slide'))
        self.wrap_slide_radio_button.setText(translate('OpenLP.GeneralTab', '&Wrap around'))
        self.next_item_radio_button.setText(translate('OpenLP.GeneralTab', '&Move to next/previous service item'))
        self.search_as_type_check_box.setText(translate('SongsPlugin.GeneralTab', 'Enable search as you type'))
        self.proxy_widget.retranslate_ui()

    def load(self):
        """
        Load settings from disk.
        """
        settings = Settings()
        settings.beginGroup(self.settings_section)
        # The max recent files value does not have an interface and so never
        # gets actually stored in the settings therefore the default value of
        # 20 will always be used.
        self.recent_spin_box.setMaximum(settings.value('max recent files'))
        self.recent_spin_box.setValue(settings.value('recent file count'))
        self.media_plugin_check_box.setChecked(settings.value('save current plugin'))
        self.double_click_live_check_box.setChecked(settings.value('double click live'))
        self.single_click_preview_check_box.setChecked(settings.value('single click preview'))
        self.single_click_service_preview_check_box.setChecked(settings.value('single click service preview'))
        self.expand_service_item_check_box.setChecked(settings.value('expand service item'))
        slide_max_height_value = settings.value('slide max height')
        for i in range(0, self.slide_max_height_combo_box.count()):
            if self.slide_max_height_combo_box.itemData(i) == slide_max_height_value:
                self.slide_max_height_combo_box.setCurrentIndex(i)
        autoscroll_value = settings.value('autoscrolling')
        for i in range(0, len(self.autoscroll_map)):
            if self.autoscroll_map[i] == autoscroll_value and i < self.autoscroll_combo_box.count():
                self.autoscroll_combo_box.setCurrentIndex(i)
        self.enable_auto_close_check_box.setChecked(settings.value('enable exit confirmation'))
        self.experimental_check_box.setChecked(settings.value('experimental'))
        if HAS_DARK_STYLE:
            self.use_dark_style_checkbox.setChecked(settings.value('use_dark_style'))
        self.hide_mouse_check_box.setChecked(settings.value('hide mouse'))
        self.service_name_day.setCurrentIndex(settings.value('default service day'))
        self.service_name_time.setTime(QtCore.QTime(settings.value('default service hour'),
                                                    settings.value('default service minute')))
        self.should_update_service_name_example = True
        self.service_name_edit.setText(settings.value('default service name'))
        default_service_enabled = settings.value('default service enabled')
        self.service_name_check_box.setChecked(default_service_enabled)
        self.service_name_check_box_toggled(default_service_enabled)
        self.ignore_aspect_ratio_check_box.setChecked(settings.value('ignore aspect ratio'))
        self.x11_bypass_check_box.setChecked(settings.value('x11 bypass wm'))
        self.slide_limits = settings.value('slide limits')
        self.is_search_as_you_type_enabled = settings.value('search as type')
        self.search_as_type_check_box.setChecked(self.is_search_as_you_type_enabled)
        # Prevent the dialog displayed by the alternate_rows_check_box to display.
        self.alternate_rows_check_box.blockSignals(True)
        self.alternate_rows_check_box.setChecked(settings.value('alternate rows'))
        self.alternate_rows_check_box.blockSignals(False)
        if self.slide_limits == SlideLimits.End:
            self.end_slide_radio_button.setChecked(True)
        elif self.slide_limits == SlideLimits.Wrap:
            self.wrap_slide_radio_button.setChecked(True)
        else:
            self.next_item_radio_button.setChecked(True)
        settings.endGroup()
        self.data_directory_copy_check_box.hide()
        self.new_data_directory_has_files_label.hide()
        self.data_directory_cancel_button.hide()
        # Since data location can be changed, make sure the path is present.
        self.data_directory_path_edit.path = AppLocation.get_data_path()
        # Don't allow data directory move if running portable.
        if settings.value('advanced/is portable'):
            self.data_directory_group_box.hide()

    def save(self):
        """
        Save settings to disk.
        """
        settings = Settings()
        settings.beginGroup(self.settings_section)
        settings.setValue('default service enabled', self.service_name_check_box.isChecked())
        service_name = self.service_name_edit.text()
        preset_is_valid = self.generate_service_name_example()[0]
        if service_name == UiStrings().DefaultServiceName or not preset_is_valid:
            settings.remove('default service name')
            self.service_name_edit.setText(service_name)
        else:
            settings.setValue('default service name', service_name)
        settings.setValue('default service day', self.service_name_day.currentIndex())
        settings.setValue('default service hour', self.service_name_time.time().hour())
        settings.setValue('default service minute', self.service_name_time.time().minute())
        settings.setValue('recent file count', self.recent_spin_box.value())
        settings.setValue('save current plugin', self.media_plugin_check_box.isChecked())
        settings.setValue('double click live', self.double_click_live_check_box.isChecked())
        settings.setValue('single click preview', self.single_click_preview_check_box.isChecked())
        settings.setValue('single click service preview', self.single_click_service_preview_check_box.isChecked())
        settings.setValue('expand service item', self.expand_service_item_check_box.isChecked())
        slide_max_height_index = self.slide_max_height_combo_box.currentIndex()
        slide_max_height_value = self.slide_max_height_combo_box.itemData(slide_max_height_index)
        settings.setValue('slide max height', slide_max_height_value)
        settings.setValue('autoscrolling', self.autoscroll_map[self.autoscroll_combo_box.currentIndex()])
        settings.setValue('experimental', self.experimental_check_box.isChecked())
        settings.setValue('enable exit confirmation', self.enable_auto_close_check_box.isChecked())
        settings.setValue('hide mouse', self.hide_mouse_check_box.isChecked())
        settings.setValue('alternate rows', self.alternate_rows_check_box.isChecked())
        settings.setValue('slide limits', self.slide_limits)
        settings.setValue('ignore aspect ratio', self.ignore_aspect_ratio_check_box.isChecked())
        if self.x11_bypass_check_box.isChecked() != settings.value('x11 bypass wm'):
            settings.setValue('x11 bypass wm', self.x11_bypass_check_box.isChecked())
            self.settings_form.register_post_process('config_screen_changed')
        self.settings_form.register_post_process('slidecontroller_update_slide_limits')
        settings.setValue('search as type', self.is_search_as_you_type_enabled)
        if HAS_DARK_STYLE:
            settings.setValue('use_dark_style', self.use_dark_style_checkbox.isChecked())
        settings.endGroup()
        self.proxy_widget.save()

    def on_search_as_type_check_box_changed(self, check_state):
        self.is_search_as_you_type_enabled = (check_state == QtCore.Qt.Checked)
        self.settings_form.register_post_process('songs_config_updated')
        self.settings_form.register_post_process('custom_config_updated')

    def cancel(self):
        """
        Dialogue was cancelled, remove any pending data path change.
        """
        self.on_data_directory_cancel_button_clicked()
        SettingsTab.cancel(self)

    def service_name_check_box_toggled(self, default_service_enabled):
        """
        Service Name options changed
        """
        self.service_name_day.setEnabled(default_service_enabled)
        time_enabled = default_service_enabled and self.service_name_day.currentIndex() != 7
        self.service_name_time.setEnabled(time_enabled)
        self.service_name_edit.setEnabled(default_service_enabled)
        self.service_name_revert_button.setEnabled(default_service_enabled)

    def generate_service_name_example(self):
        """
        Display an example of the template used
        """
        preset_is_valid = True
        if self.service_name_day.currentIndex() == 7:
            local_time = datetime.now()
        else:
            now = datetime.now()
            day_delta = self.service_name_day.currentIndex() - now.weekday()
            if day_delta < 0:
                day_delta += 7
            time = now + timedelta(days=day_delta)
            local_time = time.replace(
                hour=self.service_name_time.time().hour(),
                minute=self.service_name_time.time().minute()
            )
        try:
            service_name_example = format_time(self.service_name_edit.text(), local_time)
        except ValueError:
            preset_is_valid = False
            service_name_example = translate('OpenLP.AdvancedTab', 'Syntax error.')
        return preset_is_valid, service_name_example

    def update_service_name_example(self, returned_value):
        """
        Update the example service name.
        """
        if not self.should_update_service_name_example:
            return
        name_example = self.generate_service_name_example()[1]
        self.service_name_example.setText(name_example)

    def on_service_name_day_changed(self, service_day):
        """
        React to the day of the service name changing.
        """
        self.service_name_time.setEnabled(service_day != 7)
        self.update_service_name_example(None)

    def on_service_name_revert_button_clicked(self):
        """
        Revert to the default service name.
        """
        self.service_name_edit.setText(UiStrings().DefaultServiceName)
        self.service_name_edit.setFocus()

    def on_data_directory_path_edit_path_changed(self, new_path):
        """
        Handle the `editPathChanged` signal of the data_directory_path_edit

        :param pathlib.Path new_path: The new path
        :rtype: None
        """
        # Make sure they want to change the data.
        answer = QtWidgets.QMessageBox.question(self, translate('OpenLP.AdvancedTab', 'Confirm Data Directory Change'),
                                                translate('OpenLP.AdvancedTab', 'Are you sure you want to change the '
                                                          'location of the OpenLP data directory to:\n\n{path}'
                                                          '\n\nThe data directory will be changed when OpenLP is '
                                                          'closed.').format(path=new_path),
                                                defaultButton=QtWidgets.QMessageBox.No)
        if answer != QtWidgets.QMessageBox.Yes:
            self.data_directory_path_edit.path = AppLocation.get_data_path()
            return
        # Check if data already exists here.
        self.check_data_overwrite(new_path)
        # Save the new location.
        self.main_window.new_data_path = new_path
        self.data_directory_cancel_button.show()

    def on_data_directory_copy_check_box_toggled(self):
        """
        Copy existing data when you change your data directory.
        """
        self.main_window.set_copy_data(self.data_directory_copy_check_box.isChecked())
        if self.data_exists:
            if self.data_directory_copy_check_box.isChecked():
                self.new_data_directory_has_files_label.show()
            else:
                self.new_data_directory_has_files_label.hide()

    def check_data_overwrite(self, data_path):
        """
        Check if there's already data in the target directory.

        :param pathlib.Path data_path: The target directory to check
        """
        if (data_path / 'songs').exists():
            self.data_exists = True
            # Check is they want to replace existing data.
            answer = QtWidgets.QMessageBox.warning(self,
                                                   translate('OpenLP.AdvancedTab', 'Overwrite Existing Data'),
                                                   translate('OpenLP.AdvancedTab',
                                                             'WARNING: \n\nThe location you have selected \n\n{path}'
                                                             '\n\nappears to contain OpenLP data files. Do you wish to '
                                                             'replace these files with the current data '
                                                             'files?'.format(path=data_path)),
                                                   QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Yes |
                                                                                         QtWidgets.QMessageBox.No),
                                                   QtWidgets.QMessageBox.No)
            self.data_directory_copy_check_box.show()
            if answer == QtWidgets.QMessageBox.Yes:
                self.data_directory_copy_check_box.setChecked(True)
                self.new_data_directory_has_files_label.show()
            else:
                self.data_directory_copy_check_box.setChecked(False)
                self.new_data_directory_has_files_label.hide()
        else:
            self.data_exists = False
            self.data_directory_copy_check_box.setChecked(True)
            self.new_data_directory_has_files_label.hide()

    def on_data_directory_cancel_button_clicked(self):
        """
        Cancel the data directory location change
        """
        self.data_directory_path_edit.path = AppLocation.get_data_path()
        self.data_directory_copy_check_box.setChecked(False)
        self.main_window.new_data_path = None
        self.main_window.set_copy_data(False)
        self.data_directory_copy_check_box.hide()
        self.data_directory_cancel_button.hide()
        self.new_data_directory_has_files_label.hide()

    def on_alternate_rows_check_box_toggled(self, checked):
        """
        Notify user about required restart.

        :param checked: The state of the check box (boolean).
        """
        QtWidgets.QMessageBox.information(self, translate('OpenLP.AdvancedTab', 'Restart Required'),
                                          translate('OpenLP.AdvancedTab',
                                                    'This change will only take effect once OpenLP '
                                                    'has been restarted.'))

    def on_end_slide_button_clicked(self):
        """
        Stop at the end either top ot bottom
        """
        self.slide_limits = SlideLimits.End

    def on_wrap_slide_button_clicked(self):
        """
        Wrap round the service item
        """
        self.slide_limits = SlideLimits.Wrap

    def on_next_item_button_clicked(self):
        """
        Advance to the next service item
        """
        self.slide_limits = SlideLimits.Next
