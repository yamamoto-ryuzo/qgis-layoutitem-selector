# -*- coding: utf-8 -*-
"""
UI ローダー - Qt Designer の .ui ファイルを動的にロード

Qt Designer で作成した .ui ファイルから UI をプログラムで読み込むためのユーティリティ。
QT6 (PyQt6) と QT5 (PyQt5) の両方に対応。
"""

import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QWidget


def load_ui(ui_file_path):
    """
    .ui ファイルから UI をロード
    
    Args:
        ui_file_path: .ui ファイルのパス
        
    Returns:
        ロードされたウィジェットクラス
    """
    if not os.path.exists(ui_file_path):
        raise FileNotFoundError(f"UI file not found: {ui_file_path}")
    
    return uic.loadUiType(ui_file_path)[0]


def load_ui_to_widget(ui_name, parent_widget):
    """
    .ui ファイルを既存のウィジェットにロード
    QT5/QT6の両方に対応
    
    Args:
        ui_name: UI ファイル名（拡張子なし）。例: 'main_dialog' -> 'main_dialog.ui'
        parent_widget: UI を読み込むウィジェット（通常は self）
        
    Raises:
        FileNotFoundError: UI ファイルが見つからない場合
    """
    # UI ファイルのパスを構築
    ui_dir = os.path.dirname(__file__)
    ui_file_path = os.path.join(ui_dir, f"{ui_name}.ui")
    
    if not os.path.exists(ui_file_path):
        raise FileNotFoundError(f"UI file not found: {ui_file_path}")
    
    # UI をウィジェットにロード
    try:
        uic.loadUi(ui_file_path, parent_widget)
    except Exception as e:
        # QT6で問題が発生する可能性があるため、詳細なエラー情報を追加
        raise RuntimeError(f"Failed to load UI from {ui_file_path}: {str(e)}")
