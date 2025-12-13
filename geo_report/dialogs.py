# -*- coding: utf-8 -*-
"""
メインダイアログクラス

geo_reportプラグインのメインUI実装です。
Qt Designer形式のUIをロードして使用します。
"""

from qgis.PyQt.QtWidgets import QDialog, QTableWidgetItem
from qgis.PyQt.QtCore import Qt
from .ui.loader import load_ui_to_widget


class GeoReportDialog(QDialog):
    """
    geo_reportプラグインのメインダイアログ
    
    レイアウト選択、アイテム管理、テンプレート機能を提供します。
    """
    
    def __init__(self, iface, parent=None):
        """
        ダイアログを初期化
        
        Args:
            iface: QGISインターフェース
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.iface = iface
        
        # UIを動的にロード
        try:
            load_ui_to_widget('main_dialog', self)
        except Exception as e:
            self.iface.messageBar().pushCritical(
                "geo_report",
                f"UIロードエラー: {str(e)}"
            )
            raise
        
        # ウィンドウ設定
        self.setWindowTitle("geo_report - Layout Item Selector")
        self.setModal(True)
        
        # シグナル接続
        self._connect_signals()
        
        # 初期化処理
        self._initialize()
    
    def _connect_signals(self):
        """
        UI要素のシグナルをスロットに接続
        """
        # ボタンシグナル
        self.closeButton.clicked.connect(self.reject)
        self.openLayoutButton.clicked.connect(self._on_open_layout)
        self.editItemButton.clicked.connect(self._on_edit_item)
        
        # リスト選択シグナル
        self.layoutListWidget.itemSelectionChanged.connect(
            self._on_layout_selected
        )
    
    def _initialize(self):
        """
        ダイアログを初期化
        
        利用可能なレイアウト一覧を取得してリストウィジェットに表示します。
        """
        try:
            self._load_layouts()
        except Exception as e:
            self.iface.messageBar().pushWarning(
                "geo_report",
                f"レイアウト読み込みエラー: {str(e)}"
            )
    
    def _load_layouts(self):
        """
        プロジェクトから利用可能なレイアウトを読み込み
        """
        # QGISプロジェクトのレイアウトマネージャーを取得
        project = self.iface.project()
        layout_manager = project.layoutManager()
        
        # レイアウト一覧をクリア
        self.layoutListWidget.clear()
        
        # レイアウト一覧を取得して表示
        layouts = layout_manager.layouts()
        if layouts:
            for layout in layouts:
                self.layoutListWidget.addItem(layout.name())
        else:
            self.layoutListWidget.addItem("(No layouts available)")
    
    def _on_layout_selected(self):
        """
        レイアウトが選択されたときの処理
        
        選択されたレイアウトのアイテム一覧を表示します。
        """
        current_item = self.layoutListWidget.currentItem()
        if not current_item or current_item.text() == "(No layouts available)":
            self.itemTableWidget.setRowCount(0)
            return
        
        layout_name = current_item.text()
        self._load_layout_items(layout_name)
    
    def _load_layout_items(self, layout_name):
        """
        指定されたレイアウトのアイテムを読み込んで表示
        
        Args:
            layout_name (str): レイアウト名
        """
        try:
            project = self.iface.project()
            layout_manager = project.layoutManager()
            
            # レイアウトを取得
            layout = layout_manager.layoutByName(layout_name)
            if not layout:
                return
            
            # テーブルをクリア
            self.itemTableWidget.setRowCount(0)
            
            # レイアウトのアイテムを取得
            items = layout.items()
            self.itemTableWidget.setRowCount(len(items))
            
            for row, item in enumerate(items):
                # アイテムID
                id_item = QTableWidgetItem(item.id())
                self.itemTableWidget.setItem(row, 0, id_item)
                
                # アイテムタイプ
                type_item = QTableWidgetItem(item.__class__.__name__)
                self.itemTableWidget.setItem(row, 1, type_item)
                
                # アイテム位置
                pos_text = f"({item.positionWithUnits().x():.1f}, {item.positionWithUnits().y():.1f})"
                pos_item = QTableWidgetItem(pos_text)
                self.itemTableWidget.setItem(row, 2, pos_item)
        
        except Exception as e:
            self.iface.messageBar().pushWarning(
                "geo_report",
                f"アイテム読み込みエラー: {str(e)}"
            )
    
    def _on_open_layout(self):
        """
        選択されたレイアウトをレイアウトマネージャーで開く
        """
        current_item = self.layoutListWidget.currentItem()
        if not current_item or current_item.text() == "(No layouts available)":
            self.iface.messageBar().pushWarning(
                "geo_report",
                "レイアウトを選択してください"
            )
            return
        
        layout_name = current_item.text()
        
        try:
            project = self.iface.project()
            layout_manager = project.layoutManager()
            layout = layout_manager.layoutByName(layout_name)
            
            if layout:
                self.iface.openLayoutDesignerFromLayout(layout)
                self.accept()
        except Exception as e:
            self.iface.messageBar().pushWarning(
                "geo_report",
                f"レイアウト開放エラー: {str(e)}"
            )
    
    def _on_edit_item(self):
        """
        選択されたアイテムを編集
        """
        selected_rows = self.itemTableWidget.selectedIndexes()
        if not selected_rows:
            self.iface.messageBar().pushWarning(
                "geo_report",
                "編集するアイテムを選択してください"
            )
            return
        
        # アイテム編集機能はここに実装
        self.iface.messageBar().pushInfo(
            "geo_report",
            "アイテム編集機能は今後実装予定です"
        )
