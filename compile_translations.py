# -*- coding: utf-8 -*-
"""
翻訳ファイル再コンパイルスクリプト

既存の .ts ファイルから .qm ファイルのみを再生成します
（翻訳内容は保持されます）
"""

import os
import subprocess
from pathlib import Path

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
    print("翻訳ファイル再コンパイルスクリプト")
    print("=" * 60)
    
    print("\n既存の .ts ファイルから .qm ファイルを再生成します")
    print("（翻訳内容は保持されます）")
    
    success_count = 0
    fail_count = 0
    
    for lang_code, lang_name in LANGUAGES.items():
        ts_file = I18N_DIR / f"geo_report_{lang_code}.ts"
        qm_file = I18N_DIR / f"geo_report_{lang_code}.qm"
        
        print(f"\n[{lang_code}] {lang_name}")
        
        if not ts_file.exists():
            print(f"  × .ts ファイルが見つかりません: {ts_file}")
            fail_count += 1
            continue
        
        print(f"  入力: {ts_file}")
        print(f"  出力: {qm_file}")
        
        if compile_qm_file(ts_file, qm_file):
            print(f"  ✓ .qm ファイルをコンパイルしました")
            success_count += 1
        else:
            print(f"  × .qm ファイルのコンパイルに失敗しました")
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"完了: 成功 {success_count} 件、失敗 {fail_count} 件")
    print("=" * 60)
    print()


if __name__ == '__main__':
    main()
