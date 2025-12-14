#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
geo_report 翻訳ファイル生成スクリプト

Qt Linguist の .ts（翻訳ソースファイル）を生成します。
lrelease.exe で .qm ファイルにコンパイルする前のステップです。

使用方法:
    python generate_translations.py
    
生成されるファイル:
    - geo_report/i18n/geo_report_en.ts (英語テンプレート)
    - geo_report/i18n/geo_report_ja.ts (日本語)
    - geo_report/i18n/geo_report_fr.ts (フランス語)
    - geo_report/i18n/geo_report_de.ts (ドイツ語)
    - geo_report/i18n/geo_report_es.ts (スペイン語)
    - geo_report/i18n/geo_report_it.ts (イタリア語)
    - geo_report/i18n/geo_report_pt.ts (ポルトガル語)
    - geo_report/i18n/geo_report_zh.ts (中国語)
    - geo_report/i18n/geo_report_ru.ts (ロシア語)
    - geo_report/i18n/geo_report_hi.ts (ヒンディー語)
"""

import os
import re
from xml.dom import minidom


def extract_strings_from_python(plugin_dir):
    """
    Python ファイルから UI 文字列を抽出
    """
    strings = set()
    
    plugin_file = os.path.join(plugin_dir, 'geo_report', 'plugin.py')
    if not os.path.exists(plugin_file):
        plugin_file = os.path.join(plugin_dir, 'plugin.py')
    
    if os.path.exists(plugin_file):
        with open(plugin_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # tr(...) パターン（寛容な正規表現）
        pattern_tr = r'tr\s*\(\s*[\'\"](.*?)[\'\"]'
        for match in re.finditer(pattern_tr, content):
            text = match.group(1).strip()
            if text:
                strings.add(text)
    
    return strings


def create_ts_file(output_path, language_code, strings):
    """
    .ts ファイルを作成
    
    Args:
        output_path: 出力ファイルパス
        language_code: 言語コード（例: ja, fr, de）
        strings: 翻訳対象文字列のセット
    """
    # XML ドキュメント構造を構築
    xml_doc = minidom.Document()
    root = xml_doc.createElement('TS')
    root.setAttribute('version', '2.1')
    root.setAttribute('language', language_code)
    xml_doc.appendChild(root)
    
    context = xml_doc.createElement('context')
    root.appendChild(context)
    
    name = xml_doc.createElement('name')
    name.appendChild(xml_doc.createTextNode('geo_report'))
    context.appendChild(name)
    
    # 各文字列に対してメッセージエントリを作成
    for text in sorted(strings):
        message = xml_doc.createElement('message')
        context.appendChild(message)
        
        source = xml_doc.createElement('source')
        source.appendChild(xml_doc.createTextNode(text))
        message.appendChild(source)
        
        translation = xml_doc.createElement('translation')
        # 英語の場合はソースと同じ、他言語は空
        if language_code == 'en':
            translation.appendChild(xml_doc.createTextNode(text))
        else:
            translation.setAttribute('type', 'unfinished')
        message.appendChild(translation)
    
    # ファイルに書き込み
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_doc.toprettyxml(indent='  ', encoding=None))


def main():
    """メイン処理"""
    plugin_dir = os.path.dirname(__file__)
    i18n_dir = os.path.join(plugin_dir, 'i18n')
    
    print("[geo_report] 翻訳ファイルを生成中...")
    
    # Python ファイルから文字列を抽出
    strings = extract_strings_from_python(plugin_dir)
    print(f"[geo_report] {len(strings)} 個の翻訳対象文字列を検出")
    
    # サポート言語
    languages = {
        'en': 'English',
        'ja': '日本語',
        'fr': 'Français',
        'de': 'Deutsch',
        'es': 'Español',
        'it': 'Italiano',
        'pt': 'Português',
        'zh': '中文',
        'ru': 'Русский',
        'hi': 'हिन्दी',
    }
    
    # 各言語の .ts ファイルを生成
    for lang_code, lang_name in languages.items():
        output_file = os.path.join(i18n_dir, f'geo_report_{lang_code}.ts')
        create_ts_file(output_file, lang_code, strings)
        print(f"[geo_report] 生成完了: {output_file} ({lang_name})")
    
    print("[geo_report] 翻訳ファイルの生成が完了しました")
    print("[geo_report] 次のステップ:")
    print("[geo_report]   1. linguist.exe で .ts ファイルを開いて翻訳を入力")
    print(f"[geo_report]   2. lrelease.exe でコンパイル: lrelease.exe {i18n_dir}/*.ts")


if __name__ == '__main__':
    main()
