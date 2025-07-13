@echo off
chcp 65001 >nul
echo QGISプラグイン配布用ZIPファイル作成ツール
echo ==========================================
echo.

REM Pythonの実行可能性をチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonが見つかりません
    echo Pythonがインストールされていることを確認してください
    echo.
    pause
    exit /b 1
)

REM metadata.txtの存在確認
if not exist "metadata.txt" (
    echo エラー: metadata.txt が見つかりません
    echo プラグインのルートディレクトリで実行してください
    echo.
    pause
    exit /b 1
)

echo Pythonスクリプトを実行中...
echo.
python create_zip.py

echo.
echo 処理完了
pause
