#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配布用ZIPファイル作成スクリプト

QGIS プラグイン配布用のZIPファイルを作成します。
- metadata.txtのバージョンを+0.0.1更新
- プラグインフォルダのコンテンツをZIP化
- 前のバージョンのZIPをWindowsのごみ箱に移動
"""

import os
import re
import shutil
import zipfile
from pathlib import Path
from typing import Tuple

# Windows環境でのごみ箱移動用
try:
    import send2trash
except ImportError:
    send2trash = None

# プロジェクト設定
PLUGIN_DIR = Path(__file__).parent / "geo_report"
METADATA_FILE = PLUGIN_DIR / "metadata.txt"
PROJECT_ROOT = Path(__file__).parent

# ZIPファイルの親フォルダと名前パターン
ZIP_PATTERN = "geo_report_v*.zip"


def read_version(metadata_path: Path) -> str:
    """
    metadata.txtからバージョンを読み取る
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'version=(\d+\.\d+\.\d+)', content)
    if not match:
        raise ValueError("バージョン情報がmetadata.txtに見つかりません")
    
    return match.group(1)


def increment_version(version: str) -> str:
    """
    バージョン文字列をインクリメント（パッチバージョンを+1）
    例: 2.1.30 -> 2.1.31
    """
    parts = version.split('.')
    if len(parts) != 3:
        raise ValueError(f"無効なバージョン形式: {version}")
    
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    patch += 1
    
    return f"{major}.{minor}.{patch}"


def update_metadata_version(metadata_path: Path, new_version: str) -> None:
    """
    metadata.txtのバージョン情報を更新
    """
    with open(metadata_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # バージョン行を更新
    new_content = re.sub(
        r'version=\d+\.\d+\.\d+',
        f'version={new_version}',
        content
    )
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ metadata.txtを更新: {new_version}")


def should_exclude(file_path: Path, plugin_dir: Path) -> bool:
    """
    ZIPに含めないファイル・フォルダを判定
    """
    rel_path = file_path.relative_to(plugin_dir)
    parts = rel_path.parts
    
    # 除外パターン
    exclude_patterns = {
        '__pycache__',
        '*.pyc',
        '.git',
        '.gitignore',
        '.gitattributes',
        '*.qm',  # コンパイル済み翻訳ファイルは除外
    }
    
    # ファイル名またはパスの一部がパターンにマッチするか確認
    for part in parts:
        if part in exclude_patterns:
            return True
        for pattern in exclude_patterns:
            if pattern.startswith('*') and part.endswith(pattern[1:]):
                return True
    
    return False


def create_distribution_zip(plugin_dir: Path, new_version: str) -> Path:
    """
    配布用ZIPファイルを作成
    """
    zip_filename = f"geo_report_v{new_version}.zip"
    zip_path = PROJECT_ROOT / zip_filename
    
    print(f"\n配布用ZIPを作成中: {zip_filename}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(plugin_dir):
            root_path = Path(root)
            
            # __pycache__などの除外フォルダをスキップ
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d, plugin_dir)]
            
            for file in files:
                file_path = root_path / file
                
                if should_exclude(file_path, plugin_dir):
                    continue
                
                # ZIPアーカイブ内のパス（相対パス）
                arcname = file_path.relative_to(plugin_dir.parent)
                zf.write(file_path, arcname)
                
    print(f"✓ ZIP作成完了: {zip_path}")
    print(f"  ファイルサイズ: {zip_path.stat().st_size / 1024:.1f} KB")
    
    return zip_path


def move_old_zips_to_trash() -> None:
    """
    前のバージョンのZIPファイルをごみ箱に移動
    """
    import glob
    
    old_zips = list(PROJECT_ROOT.glob(ZIP_PATTERN))
    
    if not old_zips:
        return
    
    for zip_file in old_zips:
        try:
            if send2trash:
                send2trash.send2trash(str(zip_file))
                print(f"✓ ごみ箱に移動: {zip_file.name}")
            else:
                # send2trashが利用できない場合は通常削除
                zip_file.unlink()
                print(f"✓ 削除: {zip_file.name}")
        except Exception as e:
            print(f"⚠ 警告: {zip_file.name} の削除に失敗: {e}")


def main():
    """
    メイン処理
    """
    print("=" * 60)
    print("QGIS プラグイン配布用ZIP作成ツール")
    print("=" * 60)
    
    # 1. 現在のバージョンを読み取る
    current_version = read_version(METADATA_FILE)
    print(f"\n現在のバージョン: {current_version}")
    
    # 2. 新しいバージョンを計算
    new_version = increment_version(current_version)
    print(f"新しいバージョン: {new_version}")
    
    # 3. 前のバージョンのZIPをごみ箱に移動
    print(f"\n前のバージョンのZIPをごみ箱に移動...")
    move_old_zips_to_trash()
    
    # 4. metadata.txtを更新
    print(f"\nmetadata.txtを更新中...")
    update_metadata_version(METADATA_FILE, new_version)
    
    # 5. 配布用ZIPを作成
    zip_path = create_distribution_zip(PLUGIN_DIR, new_version)
    
    print("\n" + "=" * 60)
    print("✓ ZIPファイル作成完了！")
    print("=" * 60)
    print(f"バージョン: {current_version} → {new_version}")
    print(f"ZIPファイル: {zip_path.name}")
    print()


if __name__ == "__main__":
    main()
