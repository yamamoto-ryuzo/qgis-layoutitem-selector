# -*- coding: utf-8 -*-
"""
翻訳ファイル生成スクリプト（シンプル版）

Pythonコードから直接 .ts ファイルを生成します
"""

import os
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.dom import minidom
import subprocess

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent
PLUGIN_DIR = PROJECT_ROOT / "geo_report"
I18N_DIR = PLUGIN_DIR / "i18n"

# 対応言語のリスト
LANGUAGES = {
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'ru': 'Russian',
    'hi': 'Hindi'
}

# lrelease の場所
LRELEASE_PATH = r"C:\Qt\linguist_6.9.1\lrelease.exe"


def extract_tr_strings(file_path):
    """
    Python ファイルから tr() メソッドで囲まれた文字列を抽出
    """
    strings = set()
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # tr("...") または tr('...') のパターンを検索
    patterns = [
        r'\.tr\("([^"]+)"\)',  # .tr("text")
        r"\.tr\('([^']+)'\)",  # .tr('text')
        r'tr\("([^"]+)"\)',     # tr("text")
        r"tr\('([^']+)'\)",     # tr('text')
        r'self\.tr\("([^"]+)"\)',  # self.tr("text")
        r"self\.tr\('([^']+)'\)",  # self.tr('text')
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        strings.update(matches)
    
    return sorted(strings)


# --- UIファイルから<string>要素のテキストを抽出 ---
def extract_ui_strings(ui_file_path):
    """
    Qt Designerの.uiファイルから<string>要素のテキストを抽出
    """
    strings = set()
    if not os.path.exists(ui_file_path):
        return []
    try:
        tree = ET.parse(ui_file_path)
        root = tree.getroot()
        for elem in root.iter():
            if elem.tag == 'string' and elem.text and elem.text.strip():
                strings.add(elem.text.strip())
    except Exception as e:
        print(f"[extract_ui_strings] Error: {e}")
    return sorted(strings)


def create_ts_file(lang_code, strings):
    """
    .ts ファイルを作成
    """
    # XML ルート要素
    root = ET.Element('TS')
    root.set('version', '2.1')
    root.set('language', lang_code)
    
    # コンテキスト要素
    context = ET.SubElement(root, 'context')
    
    name_elem = ET.SubElement(context, 'name')
    name_elem.text = 'geo_report'
    
    # 各文字列にメッセージ要素を追加
    for string in strings:
        message = ET.SubElement(context, 'message')
        
        source = ET.SubElement(message, 'source')
        source.text = string
        
        translation = ET.SubElement(message, 'translation')
        
        # 英語の場合は同じテキストを設定（ソース言語）
        if lang_code == 'en':
            translation.text = string
            translation.set('type', 'unfinished')
        else:
            # 他の言語は未翻訳
            translation.set('type', 'unfinished')
    
    # XML を整形
    xml_str = ET.tostring(root, encoding='utf-8')
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ', encoding='utf-8')
    
    # XML 宣言を調整
    pretty_xml = pretty_xml.decode('utf-8')
    pretty_xml = '<?xml version="1.0" encoding="utf-8"?>\n' + '\n'.join(pretty_xml.split('\n')[1:])
    
    return pretty_xml


def compile_qm_file(ts_file, qm_file):
    """
    .ts ファイルから .qm ファイルをコンパイル
    """
    if not os.path.exists(LRELEASE_PATH):
        print(f"× lrelease が見つかりません: {LRELEASE_PATH}")
        return False
    
    try:
        result = subprocess.run(
            [LRELEASE_PATH, str(ts_file), '-qm', str(qm_file)],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return True
        else:
            print(f"× エラー: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"× 例外エラー: {e}")
        return False


def main():
    """メイン処理"""
    print("=" * 60)
    print("geo_report 翻訳ファイル生成スクリプト")
    print("=" * 60)
    
    # i18n ディレクトリが存在しない場合は作成
    I18N_DIR.mkdir(exist_ok=True)
    
    # Python ファイルから翻訳文字列を抽出
    print("\n=== 翻訳文字列を抽出中 ===")
    

    all_strings = set()
    source_files = [
        PLUGIN_DIR / "plugin.py",
        PLUGIN_DIR / "__init__.py"
    ]
    ui_files = [PLUGIN_DIR / "ui" / "main_dialog.ui"]

    # Pythonファイルから抽出
    for source_file in source_files:
        if source_file.exists():
            strings = extract_tr_strings(source_file)
            all_strings.update(strings)
            print(f"✓ {source_file.name}: {len(strings)} 件の文字列")

    # UIファイルから抽出
    for ui_file in ui_files:
        if ui_file.exists():
            ui_strings = extract_ui_strings(ui_file)
            all_strings.update(ui_strings)
            print(f"✓ {ui_file.name}: {len(ui_strings)} 件のUI文字列")

    print(f"\n合計: {len(all_strings)} 件の翻訳文字列")
    
    # 各言語の .ts ファイルを生成
    print("\n=== .ts ファイルを生成中 ===")
    
    for lang_code, lang_name in LANGUAGES.items():
        ts_file = I18N_DIR / f"geo_report_{lang_code}.ts"
        
        print(f"\n[{lang_code}] {lang_name}")
        print(f"  出力: {ts_file}")
        
        # .ts ファイルを作成
        ts_content = create_ts_file(lang_code, sorted(all_strings))
        
        with open(ts_file, 'w', encoding='utf-8') as f:
            f.write(ts_content)
        
        print(f"  ✓ .ts ファイルを作成しました")
        
        # .qm ファイルをコンパイル
        qm_file = I18N_DIR / f"geo_report_{lang_code}.qm"
        
        if compile_qm_file(ts_file, qm_file):
            print(f"  ✓ .qm ファイルをコンパイルしました")
        else:
            print(f"  × .qm ファイルのコンパイルに失敗しました")
    
    print("\n" + "=" * 60)
    print("✓ 完了！")
    print("=" * 60)
    print("\n次のステップ:")
    print("1. Qt Linguist で翻訳を編集:")
    print(f"   {os.path.join(r'C:\Qt\linguist_6.9.1', 'linguist.exe')}")
    print(f"2. 翻訳ファイルの場所: {I18N_DIR}")
    print("3. 翻訳後、再度このスクリプトを実行して .qm ファイルを更新")
    print()


if __name__ == '__main__':
    main()
