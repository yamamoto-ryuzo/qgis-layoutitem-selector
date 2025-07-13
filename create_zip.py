#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QGISプラグイン配布用ZIPファイル作成スクリプト
"""

import os
import zipfile
import shutil
import datetime
from pathlib import Path

def read_metadata():
    """metadata.txtからプラグイン情報を読み取る"""
    metadata = {}
    try:
        with open('metadata.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    metadata[key.strip()] = value.strip()
    except FileNotFoundError:
        print("エラー: metadata.txt が見つかりません")
        return None
    return metadata

def get_plugin_name():
    """PEP 8準拠のプラグイン名を取得"""
    current_dir = os.path.basename(os.getcwd())
    # ハイフンをアンダースコアに変換してPEP 8準拠にする
    plugin_name = current_dir.replace('-', '_')
    return plugin_name

def get_repo_name():
    """現在のディレクトリからリポジトリ名を取得"""
    current_dir = os.path.basename(os.getcwd())
    return current_dir

def create_plugin_zip():
    """プラグインのZIPファイルを作成"""
    
    # メタデータを読み取り
    metadata = read_metadata()
    if not metadata:
        return False
    
    # リポジトリ名を自動取得
    repo_name = get_repo_name()
    plugin_name = get_plugin_name()  # PEP 8準拠の名前
    version = metadata.get('version', '1.0.0')
    
    # 配布用ディレクトリ名（PEP 8準拠）
    dist_dir = plugin_name
    zip_filename = f"{repo_name}_v{version}.zip"
    
    # 含めるファイルのリスト
    include_files = [
        '__init__.py',
        'layout_item_selector.py',
        'metadata.txt',
        'resources.py',
        'resources.qrc',
        'icon.png',
        'README.md',
        'LICENSE'
    ]
    
    # 除外するファイル/ディレクトリ
    exclude_patterns = [
        '.git',
        '.gitignore',
        '.gitattributes',
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.vscode',
        '.idea',
        'compile.bat',
        'create_zip.py',
        '*.zip'
    ]
    
    print(f"プラグイン配布用ZIPファイルを作成中: {zip_filename}")
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 指定されたファイルを追加
            for file_name in include_files:
                if os.path.exists(file_name):
                    # ZIP内でのパス: plugin_name/filename
                    zip_path = f"{dist_dir}/{file_name}"
                    zipf.write(file_name, zip_path)
                    print(f"  追加: {file_name} -> {zip_path}")
                else:
                    print(f"  警告: {file_name} が見つかりません（スキップ）")
            
            # 追加でディレクトリがあれば含める（例: i18n, help等）
            for root, dirs, files in os.walk('.'):
                # 除外パターンをチェック
                dirs[:] = [d for d in dirs if not any(d.startswith(pattern.rstrip('*')) for pattern in exclude_patterns)]
                
                if root == '.':
                    continue
                    
                for file in files:
                    file_path = os.path.join(root, file)
                    # 除外パターンをチェック
                    if any(file.endswith(pattern.lstrip('*')) for pattern in exclude_patterns if '*' in pattern):
                        continue
                    if any(pattern in file_path for pattern in exclude_patterns if '*' not in pattern):
                        continue
                    if file_path.replace('.\\', '') not in include_files:
                        zip_path = f"{dist_dir}/{file_path.replace('.\\', '').replace('\\', '/')}"
                        zipf.write(file_path, zip_path)
                        print(f"  追加: {file_path} -> {zip_path}")
        
        # ファイルサイズを取得
        file_size = os.path.getsize(zip_filename)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n✓ 配布用ZIPファイルの作成が完了しました!")
        print(f"  ファイル名: {zip_filename}")
        print(f"  ファイルサイズ: {file_size:,} bytes ({file_size_mb:.2f} MB)")
        print(f"  作成日時: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"エラー: ZIPファイルの作成に失敗しました - {e}")
        return False

def verify_zip_contents(zip_filename):
    """作成されたZIPファイルの内容を確認"""
    print(f"\n{zip_filename} の内容:")
    print("-" * 50)
    
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            file_list = zipf.namelist()
            file_list.sort()
            
            for file_path in file_list:
                file_info = zipf.getinfo(file_path)
                size = file_info.file_size
                print(f"  {file_path} ({size:,} bytes)")
            
            print(f"\n総ファイル数: {len(file_list)}")
            
    except Exception as e:
        print(f"エラー: ZIPファイルの確認に失敗しました - {e}")

def main():
    """メイン処理"""
    print("QGISプラグイン配布用ZIPファイル作成ツール")
    print("=" * 50)
    
    # 現在のディレクトリがプラグインディレクトリかチェック
    if not os.path.exists('metadata.txt'):
        print("エラー: metadata.txt が見つかりません")
        print("プラグインのルートディレクトリで実行してください")
        return
    
    # ZIPファイル作成
    if create_plugin_zip():
        # 作成されたZIPファイルを確認
        metadata = read_metadata()
        repo_name = get_repo_name()
        version = metadata.get('version', '1.0.0')
        zip_filename = f"{repo_name}_v{version}.zip"
        
        verify_zip_contents(zip_filename)
        
        print(f"\n📦 配布準備完了!")
        print(f"QGISプラグインマネージャーで {zip_filename} をインストールできます。")
    else:
        print("\n❌ ZIPファイルの作成に失敗しました")

if __name__ == "__main__":
    main()
