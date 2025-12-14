# -*- coding: utf-8 -*-
"""
基本翻訳追加スクリプト

主要な言語（日本語、フランス語、ドイツ語、スペイン語、中国語）に
基本的な翻訳を追加します。
"""

import re
from pathlib import Path

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent
PLUGIN_DIR = PROJECT_ROOT / "geo_report"
I18N_DIR = PLUGIN_DIR / "i18n"

# 基本翻訳辞書
TRANSLATIONS = {
    'ja': {  # 日本語
        'Layout Selection & Item Management': 'レイアウト選択とアイテム管理',
        'Layout List:': 'レイアウト一覧:',
        'Scale:': '縮尺:',
        'Angle:': '角度:',
        'Layout Items:': 'レイアウトアイテム:',
        'Item Name': 'アイテム名',
        'Type': '種類',
        'Visible': '表示',
        'Show Print Area on Map': 'マップにプリント領域を表示',
        'Hide Print Area': 'プリント領域を隠す',
        'Refresh Item Info': 'アイテム情報を更新',
        'Save Layout': 'レイアウトを保存',
        'Load Layout': 'レイアウトを読み込み',
        'Create Report': 'レポートを作成',
        'Selected Item Properties:': '選択されたアイテムのプロパティ:',
        'Layout Information:': 'レイアウト情報:',
        'Item Properties': 'アイテムプロパティ',
        'Layout Info': 'レイアウト情報',
        'Apply Properties': 'プロパティを適用',
        'Error': 'エラー',
        'Cannot load properties: ': 'プロパティを読み込めません: ',
        'Information': '情報',
        'Item information has been updated.': 'アイテム情報が更新されました。',
        'Warning': '警告',
        'Please select a layout.': 'レイアウトを選択してください。',
        'Layout Name: ': 'レイアウト名: ',
        'Page Count: ': 'ページ数: ',
        'Total Objects: ': '合計オブジェクト数: ',
        'Page Information:': 'ページ情報:',
        '  Page ': '  ページ ',
        'All Objects List:': 'すべてのオブジェクト一覧:',
        'Select Layout Property File': 'レイアウトプロパティファイルを選択',
        'Folder: ': 'フォルダ: ',
        'Available Layout Property Files:': '利用可能なレイアウトプロパティファイル:',
        'Select': '選択',
        'Cancel': 'キャンセル',
        'Browse Other Folder...': '他のフォルダを参照...',
        'Size': 'サイズ',
        'Modified': '更新日時',
        'Error getting information': '情報取得エラー',
        'ID': 'ID',
        'Display Name': '表示名',
        'X Position (mm)': 'X位置 (mm)',
        'Y Position (mm)': 'Y位置 (mm)',
        'Width (mm)': '幅 (mm)',
        'Height (mm)': '高さ (mm)',
        'Rotation Angle': '回転角度',
        'Text': 'テキスト',
        'Font Size': 'フォントサイズ',
        'Scale': '縮尺',
        'Image Path': '画像パス',
    },
    'fr': {  # フランス語
        'Layout Selection & Item Management': 'Sélection de mise en page et gestion des éléments',
        'Layout List:': 'Liste des mises en page:',
        'Scale:': 'Échelle:',
        'Angle:': 'Angle:',
        'Layout Items:': 'Éléments de mise en page:',
        'Item Name': 'Nom de l\'élément',
        'Type': 'Type',
        'Visible': 'Visible',
        'Show Print Area on Map': 'Afficher la zone d\'impression sur la carte',
        'Hide Print Area': 'Masquer la zone d\'impression',
        'Refresh Item Info': 'Actualiser les informations sur l\'élément',
        'Save Layout': 'Enregistrer la mise en page',
        'Load Layout': 'Charger la mise en page',
        'Create Report': 'Créer un rapport',
        'Selected Item Properties:': 'Propriétés de l\'élément sélectionné:',
        'Layout Information:': 'Informations sur la mise en page:',
        'Item Properties': 'Propriétés de l\'élément',
        'Layout Info': 'Info de mise en page',
        'Apply Properties': 'Appliquer les propriétés',
        'Error': 'Erreur',
        'Cannot load properties: ': 'Impossible de charger les propriétés: ',
        'Information': 'Information',
        'Item information has been updated.': 'Les informations sur l\'élément ont été mises à jour.',
        'Warning': 'Avertissement',
        'Please select a layout.': 'Veuillez sélectionner une mise en page.',
    },
    'de': {  # ドイツ語
        'Layout Selection & Item Management': 'Layout-Auswahl und Elementverwaltung',
        'Layout List:': 'Layout-Liste:',
        'Scale:': 'Maßstab:',
        'Angle:': 'Winkel:',
        'Layout Items:': 'Layout-Elemente:',
        'Item Name': 'Elementname',
        'Type': 'Typ',
        'Visible': 'Sichtbar',
        'Show Print Area on Map': 'Druckbereich auf Karte anzeigen',
        'Hide Print Area': 'Druckbereich ausblenden',
        'Refresh Item Info': 'Elementinformationen aktualisieren',
        'Save Layout': 'Layout speichern',
        'Load Layout': 'Layout laden',
        'Create Report': 'Bericht erstellen',
        'Selected Item Properties:': 'Eigenschaften des ausgewählten Elements:',
        'Layout Information:': 'Layout-Informationen:',
        'Item Properties': 'Elementeigenschaften',
        'Layout Info': 'Layout-Info',
        'Apply Properties': 'Eigenschaften anwenden',
        'Error': 'Fehler',
        'Cannot load properties: ': 'Eigenschaften können nicht geladen werden: ',
        'Information': 'Information',
        'Item information has been updated.': 'Elementinformationen wurden aktualisiert.',
        'Warning': 'Warnung',
        'Please select a layout.': 'Bitte wählen Sie ein Layout aus.',
    },
    'es': {  # スペイン語
        'Layout Selection & Item Management': 'Selección de diseño y gestión de elementos',
        'Layout List:': 'Lista de diseños:',
        'Scale:': 'Escala:',
        'Angle:': 'Ángulo:',
        'Layout Items:': 'Elementos del diseño:',
        'Item Name': 'Nombre del elemento',
        'Type': 'Tipo',
        'Visible': 'Visible',
        'Show Print Area on Map': 'Mostrar área de impresión en el mapa',
        'Hide Print Area': 'Ocultar área de impresión',
        'Refresh Item Info': 'Actualizar información del elemento',
        'Save Layout': 'Guardar diseño',
        'Load Layout': 'Cargar diseño',
        'Create Report': 'Crear informe',
        'Selected Item Properties:': 'Propiedades del elemento seleccionado:',
        'Layout Information:': 'Información del diseño:',
        'Item Properties': 'Propiedades del elemento',
        'Layout Info': 'Info del diseño',
        'Apply Properties': 'Aplicar propiedades',
        'Error': 'Error',
        'Cannot load properties: ': 'No se pueden cargar las propiedades: ',
        'Information': 'Información',
        'Item information has been updated.': 'Se ha actualizado la información del elemento.',
        'Warning': 'Advertencia',
        'Please select a layout.': 'Por favor, seleccione un diseño.',
    },
    'zh': {  # 中国語
        'Layout Selection & Item Management': '布局选择和项目管理',
        'Layout List:': '布局列表:',
        'Scale:': '比例:',
        'Angle:': '角度:',
        'Layout Items:': '布局项目:',
        'Item Name': '项目名称',
        'Type': '类型',
        'Visible': '可见',
        'Show Print Area on Map': '在地图上显示打印区域',
        'Hide Print Area': '隐藏打印区域',
        'Refresh Item Info': '刷新项目信息',
        'Save Layout': '保存布局',
        'Load Layout': '加载布局',
        'Create Report': '创建报告',
        'Selected Item Properties:': '所选项目属性:',
        'Layout Information:': '布局信息:',
        'Item Properties': '项目属性',
        'Layout Info': '布局信息',
        'Apply Properties': '应用属性',
        'Error': '错误',
        'Cannot load properties: ': '无法加载属性: ',
        'Information': '信息',
        'Item information has been updated.': '项目信息已更新。',
        'Warning': '警告',
        'Please select a layout.': '请选择一个布局。',
    },
}


def update_ts_file(lang_code, translations):
    """
    .ts ファイルに翻訳を追加
    """
    ts_file = I18N_DIR / f"geo_report_{lang_code}.ts"
    
    if not ts_file.exists():
        print(f"× ファイルが見つかりません: {ts_file}")
        return False
    
    # ファイルを読み込み
    with open(ts_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 各翻訳を適用
    for source, target in translations.items():
        # エスケープ処理
        source_escaped = source.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        target_escaped = target.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # パターン: <source>...</source>\n    <translation type="unfinished"/>
        pattern1 = f'<source>{re.escape(source_escaped)}</source>\\s*<translation type="unfinished"/>'
        replacement1 = f'<source>{source_escaped}</source>\n    <translation>{target_escaped}</translation>'
        content = re.sub(pattern1, replacement1, content)
        
        # パターン: <source>...</source>\n    <translation type="unfinished"></translation>
        pattern2 = f'<source>{re.escape(source_escaped)}</source>\\s*<translation type="unfinished"></translation>'
        replacement2 = f'<source>{source_escaped}</source>\n    <translation>{target_escaped}</translation>'
        content = re.sub(pattern2, replacement2, content)
    
    # ファイルに書き戻し
    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def main():
    """メイン処理"""
    print("=" * 60)
    print("基本翻訳追加スクリプト")
    print("=" * 60)
    
    for lang_code, translations in TRANSLATIONS.items():
        print(f"\n[{lang_code}] 翻訳を追加中...")
        
        if update_ts_file(lang_code, translations):
            print(f"  ✓ {len(translations)} 件の翻訳を追加しました")
        else:
            print(f"  × 失敗しました")
    
    print("\n" + "=" * 60)
    print("✓ 完了！")
    print("=" * 60)
    print("\n次のステップ:")
    print("1. generate_translations.py を実行して .qm ファイルを再コンパイル")
    print("2. または Qt Linguist で翻訳を確認・編集")
    print()


if __name__ == '__main__':
    main()
