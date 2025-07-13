# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LayoutItemSelector
                                 A QGIS plugin
 レイアウト印刷を選択してレイアウトマネージャを開くプラグイン
                              -------------------
        begin                : 2025-07-13
        git sha              : $Format:%H$
        copyright            : (C) 2025 by yamamoto-ryuzo
        email                : 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import os.path

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout
from qgis.core import QgsProject, QgsLayoutManager
from qgis.gui import QgsMessageBar

# Initialize Qt resources from file resources.py
try:
    from .resources import *
except ImportError:
    pass

class LayoutItemSelector:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LayoutItemSelector_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Layout Item Selector')
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LayoutItemSelector', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/layout_item_selector/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'レイアウト選択'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Layout Item Selector'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""
        self.show_layout_selector()

    def show_layout_selector(self):
        """レイアウト選択ダイアログを表示"""
        project = QgsProject.instance()
        layout_manager = project.layoutManager()
        layouts = layout_manager.layouts()
        
        if not layouts:
            self.iface.messageBar().pushMessage(
                "警告",
                "プロジェクトにレイアウトがありません。",
                level=QgsMessageBar.WARNING,
                duration=3
            )
            return
        
        dialog = LayoutSelectorDialog(layouts, self.iface)
        dialog.exec_()


class LayoutSelectorDialog(QDialog):
    """レイアウト選択ダイアログ"""
    
    def __init__(self, layouts, iface):
        super().__init__()
        self.layouts = layouts
        self.iface = iface
        self.init_ui()
        
    def init_ui(self):
        """UIを初期化"""
        self.setWindowTitle("レイアウト選択")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # レイアウトリスト
        self.layout_list = QListWidget()
        for qgs_layout in self.layouts:
            item = QListWidgetItem(qgs_layout.name())
            item.setData(Qt.UserRole, qgs_layout)
            self.layout_list.addItem(item)
        
        # ダブルクリックでレイアウトマネージャを開く
        self.layout_list.itemDoubleClicked.connect(self.open_layout_manager)
        
        layout.addWidget(self.layout_list)
        
        # ボタン
        button_layout = QHBoxLayout()
        
        self.open_button = QPushButton("レイアウトマネージャを開く")
        self.open_button.clicked.connect(self.open_layout_manager)
        button_layout.addWidget(self.open_button)
        
        self.cancel_button = QPushButton("キャンセル")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def open_layout_manager(self):
        """選択されたレイアウトでレイアウトマネージャを開く"""
        current_item = self.layout_list.currentItem()
        if current_item is None:
            self.iface.messageBar().pushMessage(
                "警告",
                "レイアウトを選択してください。",
                level=QgsMessageBar.WARNING,
                duration=3
            )
            return
            
        selected_layout = current_item.data(Qt.UserRole)
        
        # レイアウトマネージャ（デザイナー）を開く
        self.iface.openLayoutDesigner(selected_layout)
        
        self.accept()
