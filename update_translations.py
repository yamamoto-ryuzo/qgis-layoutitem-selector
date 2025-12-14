# -*- coding: utf-8 -*-
"""
翻訳ファイル更新スクリプト

pylupdate5 で .ts ファイルを更新し、lrelease で .qm ファイルを生成します。
対応言語：英語、フランス語、ドイツ語、スペイン語、イタリア語、ポルトガル語、
          日本語、中国語、ロシア語、ヒンディー語
"""

import os
import sys
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

# Qt Linguist ツールの場所
LINGUIST_DIR = r"C:\Qt\linguist_6.9.1"
LRELEASE_PATH = os.path.join(LINGUIST_DIR, "lrelease.exe")
LUPDATE_PATH = os.path.join(LINGUIST_DIR, "lupdate.exe")

# PRO ファイルの場所
PRO_FILE = PROJECT_ROOT / "geo_report.pro"


def update_ts_files():
    """
    .pro ファイルを使って .ts ファイルを生成・更新
    """
    print("\n=== 翻訳ソースファイル (.ts) を更新中 ===")
    
    # i18n ディレクトリが存在しない場合は作成
    I18N_DIR.mkdir(exist_ok=True)
    
    # lupdate が存在するか確認
    if not os.path.exists(LUPDATE_PATH):
        print(f"× lupdate が見つかりません: {LUPDATE_PATH}")
        print("  Qt Linguist ツールをインストールしてください")
        return False
    
    # .pro ファイルが存在するか確認
    if not PRO_FILE.exists():
        print(f"× プロジェクトファイルが見つかりません: {PRO_FILE}")
        return False
    
    print(f"lupdate を使用: {LUPDATE_PATH}")
    print(f"プロジェクトファイル: {PRO_FILE}")
    
    # lupdate コマンドを実行
    try:
        result = subprocess.run(
            [LUPDATE_PATH, str(PRO_FILE)],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(PROJECT_ROOT)
        )
        
        if result.returncode == 0:
            print(f"✓ .ts ファイルを更新しました")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"× エラー: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"× 例外エラー: {e}")
        return False


def compile_qm_files():
    """
    .ts ファイルから .qm ファイルをコンパイル
    """
    print("\n=== 翻訳バイナリファイル (.qm) をコンパイル中 ===")
    
    if not os.path.exists(LRELEASE_PATH):
        print(f"× lrelease が見つかりません: {LRELEASE_PATH}")
        print("  lrelease.exe のパスを確認してください")
        return
    
    for lang_code, lang_name in LANGUAGES.items():
        ts_file = I18N_DIR / f"geo_report_{lang_code}.ts"
        qm_file = I18N_DIR / f"geo_report_{lang_code}.qm"
        
        if not ts_file.exists():
            print(f"[{lang_code}] × .ts ファイルが見つかりません: {ts_file}")
            continue
        
        print(f"\n[{lang_code}] {lang_name}")
        print(f"  入力: {ts_file}")
        print(f"  出力: {qm_file}")
        
        try:
            result = subprocess.run(
                [LRELEASE_PATH, str(ts_file), '-qm', str(qm_file)],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                print(f"  ✓ .qm ファイルをコンパイルしました")
            else:
                print(f"  × エラー: {result.stderr}")
                
        except Exception as e:
            print(f"  × 例外エラー: {e}")


def main():
    """メイン処理"""
    print("=" * 60)
    print("geo_report 翻訳ファイル更新スクリプト")
    print("=" * 60)
    
    # .ts ファイルを更新
    if not update_ts_files():
        print("\n× .ts ファイルの更新に失敗しました")
        sys.exit(1)
    
    # .qm ファイルをコンパイル
    compile_qm_files()
    
    print("\n" + "=" * 60)
    print("✓ 完了！")
    print("=" * 60)
    print("\n次のステップ:")
    linguist_path = os.path.join(LINGUIST_DIR, "linguist.exe")
    print(f"1. Qt Linguist で翻訳を編集: {linguist_path}")
    print(f"2. 翻訳ファイルの場所: {I18N_DIR}")
    print("3. 翻訳後、再度このスクリプトを実行して .qm ファイルを更新")
    print()


if __name__ == '__main__':
    main()
