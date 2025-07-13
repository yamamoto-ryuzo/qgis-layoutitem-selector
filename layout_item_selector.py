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
from qgis.PyQt.QtWidgets import (QAction, QDialog, QVBoxLayout, QListWidget, QListWidgetItem, 
                                QPushButton, QHBoxLayout, QSplitter, QTextEdit, QLabel, 
                                QTreeWidget, QTreeWidgetItem, QGroupBox, QLineEdit, 
                                QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, QFormLayout,
                                QTabWidget, QWidget, QScrollArea, QFileDialog, QMessageBox)
from qgis.core import QgsProject, QgsLayoutManager, QgsLayoutItem, Qgis, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes
from qgis.gui import QgsMessageBar
import json

# Initialize Qt resources from file resources.py
try:
    from .resources import *
    print("リソースファイルを正常に読み込みました")
except ImportError as e:
    print(f"リソースファイルの読み込みに失敗: {e}")
    try:
        import resources
        print("相対パスでリソースファイルを読み込みました")
    except ImportError:
        print("リソースファイルが見つかりません")

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

        # アイコンパスを設定（リソースパスと代替パス）
        icon_path = ':/plugins/layout_item_selector/icon.png'
        
        # フォールバック用のアイコンパス
        import os
        fallback_icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        
        # アイコンが存在するかチェック
        icon = QIcon(icon_path)
        if icon.isNull():
            # リソースからロードできない場合は直接ファイルパスを使用
            icon = QIcon(fallback_icon_path)
            if not icon.isNull():
                icon_path = fallback_icon_path
        
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
                level=Qgis.Warning,
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
        self.current_layout = None
        self.init_ui()
        
    def init_ui(self):
        """UIを初期化"""
        self.setWindowTitle("レイアウト選択・アイテム管理")
        self.setModal(True)
        self.resize(1000, 700)
        
        main_layout = QHBoxLayout()
        
        # 左側パネル - レイアウトリスト
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        layout_label = QLabel("レイアウト一覧:")
        left_layout.addWidget(layout_label)
        
        self.layout_list = QListWidget()
        for qgs_layout in self.layouts:
            item = QListWidgetItem(qgs_layout.name())
            item.setData(Qt.UserRole, qgs_layout)
            self.layout_list.addItem(item)
        
        # レイアウト選択時にアイテム情報を更新
        self.layout_list.currentItemChanged.connect(self.on_layout_selected)
        self.layout_list.itemDoubleClicked.connect(self.open_layout_manager)
        
        left_layout.addWidget(self.layout_list)
        
        # ボタン
        button_layout = QVBoxLayout()
        
        self.open_button = QPushButton("レイアウトマネージャを開く")
        self.open_button.clicked.connect(self.open_layout_manager)
        self.open_button.setEnabled(False)
        button_layout.addWidget(self.open_button)
        
        self.refresh_button = QPushButton("アイテム情報を更新")
        self.refresh_button.clicked.connect(self.refresh_item_info)
        self.refresh_button.setEnabled(False)
        button_layout.addWidget(self.refresh_button)
        
        self.cancel_button = QPushButton("キャンセル")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        left_layout.addLayout(button_layout)
        left_panel.setLayout(left_layout)
        left_panel.setMaximumWidth(250)
        
        # 右側パネル - 垂直分割
        right_splitter = QSplitter(Qt.Vertical)
        
        # 上部: アイテムリスト
        items_widget = QWidget()
        items_layout = QVBoxLayout()
        
        items_label = QLabel("レイアウトアイテム:")
        items_layout.addWidget(items_label)
        
        self.items_tree = QTreeWidget()
        self.items_tree.setHeaderLabels(["アイテム名", "タイプ", "表示", "位置(X,Y)", "サイズ(W×H)"])
        self.items_tree.currentItemChanged.connect(self.on_item_selected)
        # ダブルクリックでプロパティを直接編集画面に移動
        self.items_tree.itemDoubleClicked.connect(self.focus_on_properties)
        
        # カラム幅を調整
        self.items_tree.setColumnWidth(0, 150)  # アイテム名
        self.items_tree.setColumnWidth(1, 80)   # タイプ
        self.items_tree.setColumnWidth(2, 60)   # 表示
        self.items_tree.setColumnWidth(3, 80)   # 位置
        self.items_tree.setColumnWidth(4, 80)   # サイズ
        
        items_layout.addWidget(self.items_tree)
        
        items_widget.setLayout(items_layout)
        right_splitter.addWidget(items_widget)
        
        # 下部: プロパティとレイアウト情報を水平分割
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        # プロパティパネル
        properties_widget = QWidget()
        properties_layout = QVBoxLayout()
        
        properties_label = QLabel("選択アイテムのプロパティ:")
        properties_layout.addWidget(properties_label)
        
        # スクロール可能エリア
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.properties_form = QFormLayout()
        scroll_widget.setLayout(self.properties_form)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        properties_layout.addWidget(scroll_area)
        
        # プロパティ更新ボタン
        properties_buttons_layout = QHBoxLayout()
        
        update_properties_btn = QPushButton("プロパティを適用")
        update_properties_btn.clicked.connect(self.update_item_properties)
        properties_buttons_layout.addWidget(update_properties_btn)
        
        save_properties_btn = QPushButton("プロパティを保存")
        save_properties_btn.clicked.connect(self.save_item_properties)
        properties_buttons_layout.addWidget(save_properties_btn)
        
        load_properties_btn = QPushButton("プロパティを読み込み")
        load_properties_btn.clicked.connect(self.load_item_properties_from_file)
        properties_buttons_layout.addWidget(load_properties_btn)
        
        properties_layout.addLayout(properties_buttons_layout)
        
        properties_widget.setLayout(properties_layout)
        bottom_splitter.addWidget(properties_widget)
        
        # レイアウト情報パネル
        info_widget = QWidget()
        info_layout = QVBoxLayout()
        
        info_label = QLabel("レイアウト情報:")
        info_layout.addWidget(info_label)
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(200)
        info_layout.addWidget(self.info_text)
        
        info_widget.setLayout(info_layout)
        bottom_splitter.addWidget(info_widget)
        
        # スプリッターの比率を設定
        bottom_splitter.setSizes([400, 300])
        
        right_splitter.addWidget(bottom_splitter)
        
        # 上下スプリッターの比率を設定（アイテムリスト：下部パネル = 1:1）
        right_splitter.setSizes([350, 350])
        
        # メインレイアウトに追加
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_splitter)
        
        self.setLayout(main_layout)
        
        # 最初のレイアウトを選択
        if self.layout_list.count() > 0:
            self.layout_list.setCurrentRow(0)
    
    def on_layout_selected(self, current, previous):
        """レイアウトが選択された時の処理"""
        if current is None:
            self.current_layout = None
            self.open_button.setEnabled(False)
            self.refresh_button.setEnabled(False)
            self.clear_item_info()
            return
            
        self.current_layout = current.data(Qt.UserRole)
        self.open_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        self.load_layout_items()
        self.load_layout_info()
    
    def load_layout_items(self):
        """レイアウトアイテムを読み込む"""
        if not self.current_layout:
            return
            
        self.items_tree.clear()
        
        # レイアウトからすべてのアイテムを取得
        items = self.current_layout.items()
        
        # デバッグ情報を追加
        total_items = len(items)
        valid_items = 0
        
        for item in items:
            # すべてのアイテムの情報をデバッグ表示
            try:
                item_class = item.__class__.__name__
                has_display_name = hasattr(item, 'displayName')
                has_uuid = hasattr(item, 'uuid')
                is_layout_item = isinstance(item, QgsLayoutItem)
                
                print(f"アイテム: {item_class}, QgsLayoutItem: {is_layout_item}, displayName: {has_display_name}, uuid: {has_uuid}")
                
                # 有効なレイアウトアイテムかチェック（より緩い条件で）
                if self.is_valid_layout_item_relaxed(item):
                    valid_items += 1
                    tree_item = QTreeWidgetItem()
                    
                    # アイテム名を取得（複数の方法を試行）
                    display_name = self.get_item_display_name(item)
                    item_type = self.get_item_type_name(item)
                    visibility = self.get_item_visibility(item)
                    
                    # 位置とサイズ情報を追加
                    pos_info, size_info = self.get_item_position_size(item)
                    
                    tree_item.setText(0, display_name)
                    tree_item.setText(1, item_type)
                    tree_item.setText(2, visibility)
                    tree_item.setText(3, pos_info)
                    tree_item.setText(4, size_info)
                    tree_item.setData(0, Qt.UserRole, item)
                    
                    # 非表示アイテムは薄いグレーで表示
                    if visibility == "非表示":
                        for col in range(5):
                            tree_item.setForeground(col, Qt.gray)
                    
                    self.items_tree.addTopLevelItem(tree_item)
                    
            except Exception as e:
                print(f"アイテム処理エラー: {e}")
                continue
        
        print(f"総アイテム数: {total_items}, 有効アイテム数: {valid_items}")
        
        # アイテムが見つからない場合のメッセージ
        if valid_items == 0 and total_items > 0:
            placeholder_item = QTreeWidgetItem()
            placeholder_item.setText(0, f"アイテムが見つかりません ({total_items}個のオブジェクトを検出)")
            placeholder_item.setText(1, "情報")
            self.items_tree.addTopLevelItem(placeholder_item)
    
    def refresh_layout_items_with_selection(self, selected_layout_item):
        """選択されたアイテムを保持しながらレイアウトアイテムを更新"""
        # 現在選択されているアイテムのUUIDを保存
        selected_uuid = None
        if selected_layout_item and hasattr(selected_layout_item, 'uuid'):
            selected_uuid = selected_layout_item.uuid()
        
        # アイテム一覧を再読み込み
        self.load_layout_items()
        
        # 選択を復元
        if selected_uuid:
            self.restore_item_selection(selected_uuid)
    
    def restore_item_selection(self, target_uuid):
        """指定されたUUIDのアイテムを選択状態に復元"""
        for i in range(self.items_tree.topLevelItemCount()):
            tree_item = self.items_tree.topLevelItem(i)
            layout_item = tree_item.data(0, Qt.UserRole)
            
            if layout_item and hasattr(layout_item, 'uuid'):
                if layout_item.uuid() == target_uuid:
                    # アイテムを選択
                    self.items_tree.setCurrentItem(tree_item)
                    # プロパティを再表示
                    self.load_item_properties(layout_item)
                    print(f"選択を復元: {tree_item.text(0)}")
                    return
        
        print("選択の復元に失敗: 対象アイテムが見つかりません")
    
    def is_valid_layout_item_relaxed(self, item):
        """より緩い条件でのレイアウトアイテムチェック"""
        try:
            # 基本的なオブジェクトチェック
            if item is None:
                return False
            
            # 除外すべきクラスをチェック
            class_name = item.__class__.__name__
            excluded_classes = [
                'QgsLayoutUndoCommand',
                'QGraphicsRectItem',
                'QGraphicsItem'
            ]
            
            if class_name in excluded_classes:
                return False
            
            # QgsLayoutItemの基本的なチェック
            return hasattr(item, '__class__') and 'QgsLayout' in class_name
        except:
            return False
    
    def get_item_display_name(self, item):
        """アイテムの表示名を取得"""
        try:
            # 複数の方法でアイテム名を取得
            if hasattr(item, 'displayName') and item.displayName():
                return item.displayName()
            elif hasattr(item, 'id') and item.id():
                return item.id()
            elif hasattr(item, 'uuid'):
                return f"アイテム{item.uuid()[:8]}"
            else:
                return f"{item.__class__.__name__}"
        except:
            return "不明なアイテム"
    
    def get_item_visibility(self, item):
        """アイテムの表示状態を取得"""
        try:
            if hasattr(item, 'isVisible'):
                return "表示" if item.isVisible() else "非表示"
            else:
                return "不明"
        except:
            return "不明"
    
    def get_item_position_size(self, item):
        """アイテムの位置とサイズを取得"""
        try:
            pos_info = "N/A"
            size_info = "N/A"
            
            if hasattr(item, 'positionWithUnits'):
                pos = item.positionWithUnits()
                pos_info = f"{pos.x():.1f}, {pos.y():.1f}"
            
            if hasattr(item, 'sizeWithUnits'):
                size = item.sizeWithUnits()
                size_info = f"{size.width():.1f}×{size.height():.1f}"
            
            return pos_info, size_info
        except:
            return "N/A", "N/A"
    
    def is_valid_layout_item(self, item):
        """有効なレイアウトアイテムかどうかをチェック"""
        try:
            # QgsLayoutItemかどうかをチェック
            if not isinstance(item, QgsLayoutItem):
                return False
                
            # 必要なメソッドがあるかチェック
            if not hasattr(item, 'displayName') or not hasattr(item, 'uuid'):
                return False
                
            # 除外すべきクラスをチェック
            class_name = item.__class__.__name__
            excluded_classes = [
                'QgsLayoutUndoCommand', 
                'QgsLayoutItemPage',
                'QGraphicsRectItem',
                'QGraphicsItem'
            ]
            
            if class_name in excluded_classes:
                return False
                
            return True
        except:
            return False
    
    def get_item_type_name(self, item):
        """アイテムタイプの日本語名を取得"""
        try:
            # QgsLayoutItemのタイプを文字列で取得
            type_name = item.__class__.__name__
            
            # クラス名からタイプを判定
            type_map = {
                'QgsLayoutItemGroup': "グループ",
                'QgsLayoutItemPage': "ページ", 
                'QgsLayoutItemMap': "地図",
                'QgsLayoutItemPicture': "画像",
                'QgsLayoutItemLabel': "ラベル",
                'QgsLayoutItemLegend': "凡例",
                'QgsLayoutItemScaleBar': "スケールバー",
                'QgsLayoutItemShape': "図形",
                'QgsLayoutItemPolygon': "ポリゴン",
                'QgsLayoutItemPolyline': "ポリライン",
                'QgsLayoutItemAttributeTable': "テーブル",
                'QgsLayoutItemHtml': "HTML",
                'QgsLayoutItemFrame': "フレーム",
            }
            
            return type_map.get(type_name, f"アイテム({type_name})")
        except AttributeError:
            return "不明"
    
    def on_item_selected(self, current, previous):
        """アイテムが選択された時の処理"""
        if current is None:
            self.clear_properties_form()
            return
            
        item = current.data(0, Qt.UserRole)
        if item:
            # すぐにプロパティを表示
            self.load_item_properties(item)
            
            # アイテム名をウィンドウタイトルに反映（オプション）
            item_name = current.text(0)
            self.setWindowTitle(f"レイアウト選択・アイテム管理 - {item_name}")
        else:
            self.setWindowTitle("レイアウト選択・アイテム管理")
    
    def load_item_properties(self, item):
        """アイテムのプロパティを読み込む"""
        # プロパティフォームをクリア
        self.clear_properties_form()
        
        if not item:
            return
        
        try:
            # 基本プロパティ
            if hasattr(item, 'uuid'):
                self.add_property_field("ID", item.uuid(), readonly=True)
            if hasattr(item, 'displayName'):
                self.add_property_field("表示名", item.displayName() or "")
            if hasattr(item, 'isVisible'):
                self.add_property_field("表示", item.isVisible(), field_type="checkbox")
            
            # 位置とサイズ
            if hasattr(item, 'positionWithUnits') and hasattr(item, 'sizeWithUnits'):
                pos = item.positionWithUnits()
                size = item.sizeWithUnits()
                
                self.add_property_field("X座標 (mm)", pos.x(), field_type="double")
                self.add_property_field("Y座標 (mm)", pos.y(), field_type="double")
                self.add_property_field("幅 (mm)", size.width(), field_type="double")
                self.add_property_field("高さ (mm)", size.height(), field_type="double")
            
            # 回転
            if hasattr(item, 'itemRotation'):
                self.add_property_field("回転角度", item.itemRotation(), field_type="double")
            
            # アイテム固有のプロパティ
            if hasattr(item, '__class__'):
                class_name = item.__class__.__name__
                if class_name == 'QgsLayoutItemLabel':
                    self.add_label_properties(item)
                elif class_name == 'QgsLayoutItemMap':
                    self.add_map_properties(item)
                elif class_name == 'QgsLayoutItemPicture':
                    self.add_picture_properties(item)
                    
        except AttributeError as e:
            # プロパティにアクセスできない場合のエラーハンドリング
            self.add_property_field("エラー", f"プロパティを読み込めません: {str(e)}", readonly=True)
    
    def add_label_properties(self, label_item):
        """ラベルアイテムのプロパティを追加"""
        try:
            if hasattr(label_item, 'text'):
                self.add_property_field("テキスト", label_item.text())
            # フォントサイズなど他のプロパティも追加可能
            if hasattr(label_item, 'font'):
                font = label_item.font()
                self.add_property_field("フォントサイズ", font.pointSize(), field_type="int")
        except AttributeError:
            pass
    
    def add_map_properties(self, map_item):
        """地図アイテムのプロパティを追加"""
        try:
            self.add_property_field("縮尺", map_item.scale(), field_type="double")
            # 他の地図プロパティも追加可能
        except AttributeError:
            pass
    
    def add_picture_properties(self, picture_item):
        """画像アイテムのプロパティを追加"""
        try:
            self.add_property_field("画像パス", picture_item.picturePath())
            # 他の画像プロパティも追加可能
        except AttributeError:
            pass
    
    def add_property_field(self, label, value, field_type="text", readonly=False):
        """プロパティフィールドを追加"""
        if field_type == "text":
            widget = QLineEdit(str(value))
            widget.setReadOnly(readonly)
            if not readonly:
                widget.textChanged.connect(self.on_property_changed)
        elif field_type == "double":
            widget = QDoubleSpinBox()
            widget.setDecimals(2)
            widget.setRange(-999999, 999999)
            widget.setValue(float(value))
            widget.setReadOnly(readonly)
            if not readonly:
                widget.valueChanged.connect(self.on_property_changed)
        elif field_type == "int":
            widget = QSpinBox()
            widget.setRange(-999999, 999999)
            widget.setValue(int(value))
            widget.setReadOnly(readonly)
            if not readonly:
                widget.valueChanged.connect(self.on_property_changed)
        elif field_type == "checkbox":
            widget = QCheckBox()
            widget.setChecked(bool(value))
            widget.setEnabled(not readonly)
            if not readonly:
                widget.toggled.connect(self.on_property_changed)
        else:
            widget = QLineEdit(str(value))
            widget.setReadOnly(readonly)
            if not readonly:
                widget.textChanged.connect(self.on_property_changed)
        
        widget.setProperty("property_name", label)
        self.properties_form.addRow(label + ":", widget)
    
    def focus_on_properties(self, item, column):
        """アイテムダブルクリック時にプロパティエリアにフォーカス"""
        # プロパティフォームの最初の編集可能フィールドにフォーカス
        for i in range(self.properties_form.rowCount()):
            field_item = self.properties_form.itemAt(i, QFormLayout.FieldRole)
            if field_item and field_item.widget():
                widget = field_item.widget()
                if hasattr(widget, 'setFocus') and not widget.isReadOnly() if hasattr(widget, 'isReadOnly') else True:
                    widget.setFocus()
                    break
    
    def on_property_changed(self):
        """プロパティが変更された時の処理（リアルタイム更新のための準備）"""
        # 将来的にリアルタイム更新を実装する場合のプレースホルダー
        pass
    
    def clear_properties_form(self):
        """プロパティフォームをクリア"""
        while self.properties_form.count():
            child = self.properties_form.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def update_item_properties(self):
        """アイテムのプロパティを更新"""
        current_item = self.items_tree.currentItem()
        if not current_item:
            self.iface.messageBar().pushMessage(
                "警告", "アイテムを選択してください。",
                level=Qgis.Warning, duration=3
            )
            return
        
        layout_item = current_item.data(0, Qt.UserRole)
        if not layout_item or not isinstance(layout_item, QgsLayoutItem):
            self.iface.messageBar().pushMessage(
                "警告", "有効なレイアウトアイテムが選択されていません。",
                level=Qgis.Warning, duration=3
            )
            return
        
        try:
            print(f"プロパティ更新開始: {layout_item.__class__.__name__}")
            
            # レイアウトの変更を開始（undo/redoサポート）
            self.current_layout.undoStack().beginCommand(layout_item, "アイテムプロパティ更新")
            
            # 更新フラグ
            updated = False
            
            # フォームから値を取得して適用
            for i in range(self.properties_form.rowCount()):
                label_item = self.properties_form.itemAt(i, QFormLayout.LabelRole)
                field_item = self.properties_form.itemAt(i, QFormLayout.FieldRole)
                
                if label_item and field_item:
                    label_text = label_item.widget().text().replace(":", "")
                    widget = field_item.widget()
                    
                    print(f"プロパティ処理中: {label_text}")
                    
                    # プロパティに応じて値を設定
                    if label_text == "表示名" and hasattr(layout_item, 'setId'):
                        # 表示名の代わりにIDを設定
                        old_id = layout_item.id()
                        new_id = widget.text()
                        if old_id != new_id:
                            layout_item.setId(new_id)
                            updated = True
                            print(f"ID更新: '{old_id}' -> '{new_id}'")
                            
                    elif label_text == "表示" and hasattr(layout_item, 'setVisibility'):
                        old_visibility = layout_item.isVisible()
                        new_visibility = widget.isChecked()
                        if old_visibility != new_visibility:
                            layout_item.setVisibility(new_visibility)
                            updated = True
                            print(f"表示状態更新: {old_visibility} -> {new_visibility}")
                            
                    elif label_text in ["X座標 (mm)", "Y座標 (mm)"]:
                        # 位置の更新は座標をまとめて処理
                        if hasattr(layout_item, 'attemptMove'):
                            pos = layout_item.positionWithUnits()
                            if label_text == "X座標 (mm)":
                                new_x = widget.value()
                                if abs(pos.x() - new_x) > 0.01:  # 小数点誤差を考慮
                                    new_pos = QgsLayoutPoint(new_x, pos.y(), QgsUnitTypes.LayoutMillimeters)
                                    layout_item.attemptMove(new_pos)
                                    updated = True
                                    print(f"X座標更新: {pos.x():.2f} -> {new_x}")
                            elif label_text == "Y座標 (mm)":
                                new_y = widget.value()
                                if abs(pos.y() - new_y) > 0.01:  # 小数点誤差を考慮
                                    new_pos = QgsLayoutPoint(pos.x(), new_y, QgsUnitTypes.LayoutMillimeters)
                                    layout_item.attemptMove(new_pos)
                                    updated = True
                                    print(f"Y座標更新: {pos.y():.2f} -> {new_y}")
                                    
                    elif label_text in ["幅 (mm)", "高さ (mm)"]:
                        # サイズの更新
                        if hasattr(layout_item, 'attemptResize'):
                            size = layout_item.sizeWithUnits()
                            if label_text == "幅 (mm)":
                                new_width = widget.value()
                                if abs(size.width() - new_width) > 0.01:
                                    new_size = QgsLayoutSize(new_width, size.height(), QgsUnitTypes.LayoutMillimeters)
                                    layout_item.attemptResize(new_size)
                                    updated = True
                                    print(f"幅更新: {size.width():.2f} -> {new_width}")
                            elif label_text == "高さ (mm)":
                                new_height = widget.value()
                                if abs(size.height() - new_height) > 0.01:
                                    new_size = QgsLayoutSize(size.width(), new_height, QgsUnitTypes.LayoutMillimeters)
                                    layout_item.attemptResize(new_size)
                                    updated = True
                                    print(f"高さ更新: {size.height():.2f} -> {new_height}")
                                    
                    elif label_text == "回転角度" and hasattr(layout_item, 'setItemRotation'):
                        old_rotation = layout_item.itemRotation()
                        new_rotation = widget.value()
                        if abs(old_rotation - new_rotation) > 0.01:
                            layout_item.setItemRotation(new_rotation)
                            updated = True
                            print(f"回転角度更新: {old_rotation:.2f} -> {new_rotation}")
                            
                    elif label_text == "テキスト" and hasattr(layout_item, 'setText'):
                        # ラベルテキストの更新
                        old_text = layout_item.text() if hasattr(layout_item, 'text') else ""
                        new_text = widget.text()
                        if old_text != new_text:
                            print(f"テキスト更新開始: '{old_text}' -> '{new_text}'")
                            layout_item.setText(new_text)
                            updated = True
                            
                            # テキスト更新後の特別処理
                            if hasattr(layout_item, 'adjustSizeToText'):
                                layout_item.adjustSizeToText()
                            if hasattr(layout_item, 'refresh'):
                                layout_item.refresh()
                            
                            # 更新後のテキストを確認
                            updated_text = layout_item.text() if hasattr(layout_item, 'text') else ""
                            print(f"テキスト更新完了: '{updated_text}'")
                        
                    elif label_text == "フォントサイズ" and hasattr(layout_item, 'setFont'):
                        old_font = layout_item.font()
                        new_size = int(widget.value())
                        if old_font.pointSize() != new_size:
                            font = layout_item.font()
                            font.setPointSize(new_size)
                            layout_item.setFont(font)
                            updated = True
                            print(f"フォントサイズ更新: {old_font.pointSize()} -> {new_size}")
                            
                            # フォント変更後の特別な更新処理
                            if hasattr(layout_item, 'adjustSizeToText'):
                                layout_item.adjustSizeToText()
                                
                    elif label_text == "縮尺" and hasattr(layout_item, 'setScale'):
                        old_scale = layout_item.scale()
                        new_scale = widget.value()
                        if abs(old_scale - new_scale) > 0.01:
                            layout_item.setScale(new_scale)
                            updated = True
                            print(f"縮尺更新: {old_scale} -> {new_scale}")
                            
                    elif label_text == "画像パス" and hasattr(layout_item, 'setPicturePath'):
                        old_path = layout_item.picturePath()
                        new_path = widget.text()
                        if old_path != new_path:
                            layout_item.setPicturePath(new_path)
                            updated = True
                            print(f"画像パス更新: '{old_path}' -> '{new_path}'")
            
            # 更新があった場合のみ処理を続行
            if updated:
                # アイテム固有の更新処理
                item_class = layout_item.__class__.__name__
                if item_class == 'QgsLayoutItemLabel':
                    # ラベルアイテムの特別な更新処理
                    if hasattr(layout_item, 'refresh'):
                        layout_item.refresh()
                elif item_class == 'QgsLayoutItemMap':
                    # 地図アイテムの特別な更新処理
                    if hasattr(layout_item, 'refresh'):
                        layout_item.refresh()
                elif item_class == 'QgsLayoutItemPicture':
                    # 画像アイテムの特別な更新処理
                    if hasattr(layout_item, 'refresh'):
                        layout_item.refresh()
                
                # アイテムの再描画を強制
                if hasattr(layout_item, 'update'):
                    layout_item.update()
                if hasattr(layout_item, 'invalidateCache'):
                    layout_item.invalidateCache()
                
                # レイアウト全体を更新
                self.current_layout.refresh()
                if hasattr(self.current_layout, 'updateBounds'):
                    self.current_layout.updateBounds()
                
                # レイアウトの変更を終了
                self.current_layout.undoStack().endCommand()
                
                self.iface.messageBar().pushMessage(
                    "成功", "プロパティが更新されました。",
                    level=Qgis.Success, duration=3
                )
                
                # アイテム一覧を更新（選択を保持）
                self.refresh_layout_items_with_selection(layout_item)
                
                print("プロパティ更新完了")
            else:
                # 変更がない場合はundoコマンドをキャンセル
                self.current_layout.undoStack().cancelCommand()
                self.iface.messageBar().pushMessage(
                    "情報", "変更はありませんでした。",
                    level=Qgis.Info, duration=2
                )
                print("変更なし")
            
        except Exception as e:
            # エラーが発生した場合はundoコマンドをキャンセル
            try:
                self.current_layout.undoStack().cancelCommand()
            except:
                pass
            
            print(f"プロパティ更新エラー: {str(e)}")
            self.iface.messageBar().pushMessage(
                "エラー", f"プロパティの更新に失敗しました: {str(e)}",
                level=Qgis.Critical, duration=5
            )
    
    def load_layout_info(self):
        """レイアウト情報を読み込む"""
        if not self.current_layout:
            self.info_text.clear()
            return
        
        items = self.current_layout.items()
        total_items = len(items)
        
        info_lines = [
            f"レイアウト名: {self.current_layout.name()}",
            f"ページ数: {self.current_layout.pageCollection().pageCount()}",
            f"総オブジェクト数: {total_items}",
            "",
            "ページ情報:"
        ]
        
        # ページ情報
        for i in range(self.current_layout.pageCollection().pageCount()):
            page = self.current_layout.pageCollection().page(i)
            info_lines.append(f"  ページ {i+1}: {page.pageSize().width():.1f} x {page.pageSize().height():.1f} mm")
        
        info_lines.extend([
            "",
            "すべてのオブジェクト一覧:"
        ])
        
        # すべてのアイテム情報（デバッグ用）
        for i, item in enumerate(items):
            try:
                class_name = item.__class__.__name__
                has_display_name = hasattr(item, 'displayName')
                has_uuid = hasattr(item, 'uuid')
                is_layout_item = isinstance(item, QgsLayoutItem)
                
                info_lines.append(f"  {i+1}. {class_name}")
                info_lines.append(f"     - QgsLayoutItem: {is_layout_item}")
                info_lines.append(f"     - displayName: {has_display_name}")
                info_lines.append(f"     - uuid: {has_uuid}")
                
                if has_display_name:
                    try:
                        display_name = item.displayName()
                        info_lines.append(f"     - 名前: {display_name}")
                    except:
                        pass
                
            except Exception as e:
                info_lines.append(f"  {i+1}. エラー: {str(e)}")
        
        self.info_text.setText("\n".join(info_lines))
    
    def refresh_item_info(self):
        """アイテム情報を更新"""
        if self.current_layout:
            self.load_layout_items()
            self.load_layout_info()
            self.iface.messageBar().pushMessage(
                "情報", "アイテム情報を更新しました。",
                level=Qgis.Info, duration=2
            )
    
    def clear_item_info(self):
        """アイテム情報をクリア"""
        self.items_tree.clear()
        self.info_text.clear()
        self.clear_properties_form()
        
    def open_layout_manager(self):
        """選択されたレイアウトでレイアウトマネージャを開く"""
        if not self.current_layout:
            self.iface.messageBar().pushMessage(
                "警告", "レイアウトを選択してください。",
                level=Qgis.Warning, duration=3
            )
            return
        
        # レイアウトマネージャ（デザイナー）を開く
        self.iface.openLayoutDesigner(self.current_layout)
        self.accept()
    
    def save_item_properties(self):
        """選択されたアイテムのプロパティをファイルに保存"""
        current_item = self.items_tree.currentItem()
        if not current_item:
            self.iface.messageBar().pushMessage(
                "警告", "保存するアイテムを選択してください。",
                level=Qgis.Warning, duration=3
            )
            return
        
        layout_item = current_item.data(0, Qt.UserRole)
        if not layout_item or not isinstance(layout_item, QgsLayoutItem):
            self.iface.messageBar().pushMessage(
                "警告", "有効なレイアウトアイテムが選択されていません。",
                level=Qgis.Warning, duration=3
            )
            return
        
        try:
            # アイテム名を取得してデフォルトファイル名を作成
            item_name = self.get_item_display_name(layout_item)
            default_filename = f"{item_name}_properties.json"
            
            # ファイル保存ダイアログ
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "プロパティファイルを保存",
                default_filename,
                "JSON Files (*.json);;All Files (*)"
            )
            
            if not filename:
                return
            
            # プロパティを収集
            properties = self.collect_item_properties(layout_item)
            
            # JSONファイルに保存
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(properties, f, ensure_ascii=False, indent=2)
            
            self.iface.messageBar().pushMessage(
                "成功", f"プロパティが保存されました: {filename}",
                level=Qgis.Success, duration=3
            )
            
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "エラー", f"プロパティの保存に失敗しました: {str(e)}",
                level=Qgis.Critical, duration=5
            )
    
    def load_item_properties_from_file(self):
        """ファイルからプロパティを読み込んで適用"""
        current_item = self.items_tree.currentItem()
        if not current_item:
            self.iface.messageBar().pushMessage(
                "警告", "プロパティを適用するアイテムを選択してください。",
                level=Qgis.Warning, duration=3
            )
            return
        
        layout_item = current_item.data(0, Qt.UserRole)
        if not layout_item or not isinstance(layout_item, QgsLayoutItem):
            self.iface.messageBar().pushMessage(
                "警告", "有効なレイアウトアイテムが選択されていません。",
                level=Qgis.Warning, duration=3
            )
            return
        
        try:
            # ファイル読み込みダイアログ
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "プロパティファイルを読み込み",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if not filename:
                return
            
            # JSONファイルから読み込み
            with open(filename, 'r', encoding='utf-8') as f:
                properties = json.load(f)
            
            # プロパティの検証
            if not self.validate_properties(properties):
                self.iface.messageBar().pushMessage(
                    "警告", "プロパティファイルの形式が無効です。",
                    level=Qgis.Warning, duration=3
                )
                return
            
            # アイテムタイプの確認
            current_item_type = layout_item.__class__.__name__
            saved_item_type = properties.get('item_type', '')
            
            if current_item_type != saved_item_type:
                reply = QMessageBox.question(
                    self,
                    "アイテムタイプ不一致",
                    f"保存されたプロパティのアイテムタイプ({saved_item_type})と\n"
                    f"選択中のアイテムタイプ({current_item_type})が異なります。\n\n"
                    f"適用しますか？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.No:
                    return
            
            # プロパティを適用
            self.apply_properties_to_item(layout_item, properties)
            
            # プロパティ表示を更新
            self.load_item_properties(layout_item)
            
            self.iface.messageBar().pushMessage(
                "成功", f"プロパティが読み込まれました: {filename}",
                level=Qgis.Success, duration=3
            )
            
        except FileNotFoundError:
            self.iface.messageBar().pushMessage(
                "エラー", "ファイルが見つかりません。",
                level=Qgis.Critical, duration=5
            )
        except json.JSONDecodeError:
            self.iface.messageBar().pushMessage(
                "エラー", "JSONファイルの解析に失敗しました。",
                level=Qgis.Critical, duration=5
            )
        except Exception as e:
            self.iface.messageBar().pushMessage(
                "エラー", f"プロパティの読み込みに失敗しました: {str(e)}",
                level=Qgis.Critical, duration=5
            )
    
    def collect_item_properties(self, item):
        """アイテムのプロパティを収集してディクショナリとして返す"""
        properties = {
            'item_type': item.__class__.__name__,
            'timestamp': QCoreApplication.translate('LayoutItemSelector', '保存日時'),
            'properties': {}
        }
        
        try:
            # 基本プロパティ
            if hasattr(item, 'uuid'):
                properties['properties']['uuid'] = item.uuid()
            if hasattr(item, 'displayName'):
                properties['properties']['display_name'] = item.displayName() or ""
            if hasattr(item, 'id'):
                properties['properties']['id'] = item.id() or ""
            if hasattr(item, 'isVisible'):
                properties['properties']['visible'] = item.isVisible()
            
            # 位置とサイズ
            if hasattr(item, 'positionWithUnits'):
                pos = item.positionWithUnits()
                properties['properties']['position'] = {
                    'x': pos.x(),
                    'y': pos.y(),
                    'units': pos.units()
                }
            
            if hasattr(item, 'sizeWithUnits'):
                size = item.sizeWithUnits()
                properties['properties']['size'] = {
                    'width': size.width(),
                    'height': size.height(),
                    'units': size.units()
                }
            
            # 回転
            if hasattr(item, 'itemRotation'):
                properties['properties']['rotation'] = item.itemRotation()
            
            # アイテム固有のプロパティ
            item_type = item.__class__.__name__
            if item_type == 'QgsLayoutItemLabel':
                self.collect_label_properties(item, properties)
            elif item_type == 'QgsLayoutItemMap':
                self.collect_map_properties(item, properties)
            elif item_type == 'QgsLayoutItemPicture':
                self.collect_picture_properties(item, properties)
            
        except Exception as e:
            print(f"プロパティ収集エラー: {str(e)}")
        
        return properties
    
    def collect_label_properties(self, label_item, properties):
        """ラベルアイテムのプロパティを収集"""
        try:
            if hasattr(label_item, 'text'):
                properties['properties']['text'] = label_item.text()
            if hasattr(label_item, 'font'):
                font = label_item.font()
                properties['properties']['font'] = {
                    'family': font.family(),
                    'size': font.pointSize(),
                    'bold': font.bold(),
                    'italic': font.italic()
                }
        except Exception as e:
            print(f"ラベルプロパティ収集エラー: {str(e)}")
    
    def collect_map_properties(self, map_item, properties):
        """地図アイテムのプロパティを収集"""
        try:
            if hasattr(map_item, 'scale'):
                properties['properties']['scale'] = map_item.scale()
        except Exception as e:
            print(f"地図プロパティ収集エラー: {str(e)}")
    
    def collect_picture_properties(self, picture_item, properties):
        """画像アイテムのプロパティを収集"""
        try:
            if hasattr(picture_item, 'picturePath'):
                properties['properties']['picture_path'] = picture_item.picturePath()
        except Exception as e:
            print(f"画像プロパティ収集エラー: {str(e)}")
    
    def validate_properties(self, properties):
        """プロパティファイルの妥当性をチェック"""
        try:
            # 必須フィールドのチェック
            if 'item_type' not in properties:
                return False
            if 'properties' not in properties:
                return False
            if not isinstance(properties['properties'], dict):
                return False
            
            return True
        except:
            return False
    
    def apply_properties_to_item(self, item, properties):
        """アイテムにプロパティを適用"""
        try:
            # レイアウトの変更を開始
            self.current_layout.undoStack().beginCommand(item, "プロパティファイル適用")
            
            props = properties['properties']
            updated = False
            
            # 基本プロパティの適用
            if 'id' in props and hasattr(item, 'setId'):
                current_id = item.id()
                new_id = props['id']
                if current_id != new_id:
                    item.setId(new_id)
                    updated = True
            
            if 'visible' in props and hasattr(item, 'setVisibility'):
                current_visibility = item.isVisible()
                new_visibility = props['visible']
                if current_visibility != new_visibility:
                    item.setVisibility(new_visibility)
                    updated = True
            
            # 位置の適用
            if 'position' in props and hasattr(item, 'attemptMove'):
                pos_data = props['position']
                new_pos = QgsLayoutPoint(pos_data['x'], pos_data['y'], QgsUnitTypes.LayoutMillimeters)
                item.attemptMove(new_pos)
                updated = True
            
            # サイズの適用
            if 'size' in props and hasattr(item, 'attemptResize'):
                size_data = props['size']
                new_size = QgsLayoutSize(size_data['width'], size_data['height'], QgsUnitTypes.LayoutMillimeters)
                item.attemptResize(new_size)
                updated = True
            
            # 回転の適用
            if 'rotation' in props and hasattr(item, 'setItemRotation'):
                current_rotation = item.itemRotation()
                new_rotation = props['rotation']
                if abs(current_rotation - new_rotation) > 0.01:
                    item.setItemRotation(new_rotation)
                    updated = True
            
            # アイテム固有のプロパティを適用
            item_type = item.__class__.__name__
            if item_type == 'QgsLayoutItemLabel':
                updated = self.apply_label_properties(item, props) or updated
            elif item_type == 'QgsLayoutItemMap':
                updated = self.apply_map_properties(item, props) or updated
            elif item_type == 'QgsLayoutItemPicture':
                updated = self.apply_picture_properties(item, props) or updated
            
            if updated:
                # アイテムの更新
                if hasattr(item, 'refresh'):
                    item.refresh()
                if hasattr(item, 'update'):
                    item.update()
                if hasattr(item, 'invalidateCache'):
                    item.invalidateCache()
                
                # レイアウト全体の更新
                self.current_layout.refresh()
                self.current_layout.undoStack().endCommand()
                
                # アイテム一覧を更新（選択を保持）
                self.refresh_layout_items_with_selection(item)
            else:
                self.current_layout.undoStack().cancelCommand()
            
        except Exception as e:
            try:
                self.current_layout.undoStack().cancelCommand()
            except:
                pass
            raise e
    
    def apply_label_properties(self, label_item, props):
        """ラベルアイテムにプロパティを適用"""
        updated = False
        try:
            if 'text' in props and hasattr(label_item, 'setText'):
                current_text = label_item.text() if hasattr(label_item, 'text') else ""
                new_text = props['text']
                if current_text != new_text:
                    label_item.setText(new_text)
                    updated = True
                    if hasattr(label_item, 'adjustSizeToText'):
                        label_item.adjustSizeToText()
            
            if 'font' in props and hasattr(label_item, 'setFont'):
                font_data = props['font']
                current_font = label_item.font()
                new_font = label_item.font()
                
                font_changed = False
                if 'family' in font_data and current_font.family() != font_data['family']:
                    new_font.setFamily(font_data['family'])
                    font_changed = True
                if 'size' in font_data and current_font.pointSize() != font_data['size']:
                    new_font.setPointSize(font_data['size'])
                    font_changed = True
                if 'bold' in font_data and current_font.bold() != font_data['bold']:
                    new_font.setBold(font_data['bold'])
                    font_changed = True
                if 'italic' in font_data and current_font.italic() != font_data['italic']:
                    new_font.setItalic(font_data['italic'])
                    font_changed = True
                
                if font_changed:
                    label_item.setFont(new_font)
                    updated = True
                    if hasattr(label_item, 'adjustSizeToText'):
                        label_item.adjustSizeToText()
            
        except Exception as e:
            print(f"ラベルプロパティ適用エラー: {str(e)}")
        
        return updated
    
    def apply_map_properties(self, map_item, props):
        """地図アイテムにプロパティを適用"""
        updated = False
        try:
            if 'scale' in props and hasattr(map_item, 'setScale'):
                current_scale = map_item.scale()
                new_scale = props['scale']
                if abs(current_scale - new_scale) > 0.01:
                    map_item.setScale(new_scale)
                    updated = True
        except Exception as e:
            print(f"地図プロパティ適用エラー: {str(e)}")
        
        return updated
    
    def apply_picture_properties(self, picture_item, props):
        """画像アイテムにプロパティを適用"""
        updated = False
        try:
            if 'picture_path' in props and hasattr(picture_item, 'setPicturePath'):
                current_path = picture_item.picturePath()
                new_path = props['picture_path']
                if current_path != new_path:
                    picture_item.setPicturePath(new_path)
                    updated = True
        except Exception as e:
            print(f"画像プロパティ適用エラー: {str(e)}")
        
        return updated
