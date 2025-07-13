@echo off
REM QGISプラグイン用のリソースファイルをコンパイル

echo Compiling resource file...
pyrcc5 -o resources.py resources.qrc

echo Done!
pause
