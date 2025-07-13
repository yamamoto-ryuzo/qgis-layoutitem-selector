#!/usr/bin/env python3
"""
簡易翻訳ファイル作成スクリプト
TSファイルからQMファイルを作成する代替手段
"""

import os
import json

def create_simple_translation_dict():
    """簡単な翻訳辞書を作成"""
    
    # 英語（デフォルト）
    en_translations = {
        "Layout Selection & Item Management": "Layout Selection & Item Management",
        "Layout List:": "Layout List:",
        "Open Layout Manager": "Open Layout Manager",
        "Refresh Item Info": "Refresh Item Info",
        "Save Layout": "Save Layout",
        "Load Layout": "Load Layout",
        "Cancel": "Cancel",
        "Layout Items:": "Layout Items:",
        "Item Name": "Item Name",
        "Type": "Type",
        "Visible": "Visible",
        "Position(X,Y)": "Position(X,Y)",
        "Size(W×H)": "Size(W×H)",
        "Selected Item Properties:": "Selected Item Properties:",
        "Apply Properties": "Apply Properties",
        "Layout Information:": "Layout Information:",
        # アイテムタイプ
        "Group": "Group",
        "Page": "Page",
        "Map": "Map",
        "Picture": "Picture",
        "Label": "Label",
        "Legend": "Legend",
        "Scale Bar": "Scale Bar",
        "Shape": "Shape",
        "Polygon": "Polygon",
        "Polyline": "Polyline",
        "Table": "Table",
        "HTML": "HTML",
        "Frame": "Frame",
        "Item": "Item",
        "Unknown": "Unknown",
        "Hidden": "Hidden",
        "Unknown Item": "Unknown Item",
        # プロパティ
        "ID": "ID",
        "Display Name": "Display Name",
        "X Position (mm)": "X Position (mm)",
        "Y Position (mm)": "Y Position (mm)",
        "Width (mm)": "Width (mm)",
        "Height (mm)": "Height (mm)",
        "Rotation Angle": "Rotation Angle",
        "Text": "Text",
        "Font Size": "Font Size",
        "Scale": "Scale",
        "Image Path": "Image Path",
        # メッセージ
        "Warning": "Warning",
        "Error": "Error",
        "Success": "Success",
        "Information": "Information",
        "Please select an item.": "Please select an item.",
        "Please select a layout.": "Please select a layout.",
        "No valid layout item selected.": "No valid layout item selected.",
        "Properties have been updated.": "Properties have been updated.",
        "No changes were made.": "No changes were made.",
        "Item information has been updated.": "Item information has been updated.",
        "No items found": "No items found",
        "objects detected": "objects detected",
    }
    
    # 日本語
    ja_translations = {
        "Layout Selection & Item Management": "レイアウト選択・アイテム管理",
        "Layout List:": "レイアウト一覧:",
        "Open Layout Manager": "レイアウトマネージャを開く",
        "Refresh Item Info": "アイテム情報を更新",
        "Save Layout": "レイアウト全体を保存",
        "Load Layout": "レイアウト全体を読み込み",
        "Cancel": "キャンセル",
        "Layout Items:": "レイアウトアイテム:",
        "Item Name": "アイテム名",
        "Type": "タイプ",
        "Visible": "表示",
        "Position(X,Y)": "位置(X,Y)",
        "Size(W×H)": "サイズ(W×H)",
        "Selected Item Properties:": "選択アイテムのプロパティ:",
        "Apply Properties": "プロパティを適用",
        "Layout Information:": "レイアウト情報:",
        # アイテムタイプ
        "Group": "グループ",
        "Page": "ページ",
        "Map": "地図",
        "Picture": "画像",
        "Label": "ラベル",
        "Legend": "凡例",
        "Scale Bar": "スケールバー",
        "Shape": "図形",
        "Polygon": "ポリゴン",
        "Polyline": "ポリライン",
        "Table": "テーブル",
        "HTML": "HTML",
        "Frame": "フレーム",
        "Item": "アイテム",
        "Unknown": "不明",
        "Hidden": "非表示",
        "Unknown Item": "不明なアイテム",
        # プロパティ
        "ID": "ID",
        "Display Name": "表示名",
        "X Position (mm)": "X座標 (mm)",
        "Y Position (mm)": "Y座標 (mm)",
        "Width (mm)": "幅 (mm)",
        "Height (mm)": "高さ (mm)",
        "Rotation Angle": "回転角度",
        "Text": "テキスト",
        "Font Size": "フォントサイズ",
        "Scale": "縮尺",
        "Image Path": "画像パス",
        # メッセージ
        "Warning": "警告",
        "Error": "エラー",
        "Success": "成功",
        "Information": "情報",
        "Please select an item.": "アイテムを選択してください。",
        "Please select a layout.": "レイアウトを選択してください。",
        "No valid layout item selected.": "有効なレイアウトアイテムが選択されていません。",
        "Properties have been updated.": "プロパティが更新されました。",
        "No changes were made.": "変更はありませんでした。",
        "Item information has been updated.": "アイテム情報を更新しました。",
        "No items found": "アイテムが見つかりません",
        "objects detected": "個のオブジェクトを検出",
    }
    
    return {
        'en': en_translations,
        'ja': ja_translations
    }

def save_translations():
    """翻訳辞書をJSONファイルとして保存"""
    translations = create_simple_translation_dict()
    
    # i18nディレクトリが存在しない場合は作成
    i18n_dir = "i18n"
    if not os.path.exists(i18n_dir):
        os.makedirs(i18n_dir)
    
    # 各言語の翻訳をJSONファイルに保存
    for lang, trans_dict in translations.items():
        filename = os.path.join(i18n_dir, f"layout_item_selector_{lang}.json")
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(trans_dict, f, ensure_ascii=False, indent=2)
        print(f"Created translation file: {filename}")

if __name__ == "__main__":
    save_translations()
    print("Translation files created successfully!")
