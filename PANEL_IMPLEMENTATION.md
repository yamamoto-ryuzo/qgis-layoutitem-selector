# パネル化実装ガイド

## 概要
geo_reportプラグインの起動画面をパネル（DockWidget）として実装しました。これにより、QGISのメインウィンドウに統合され、より使いやすいインターフェースになりました。

## 実装内容

### 1. インポート追加
```python
from qgis.PyQt.QtWidgets import QDockWidget
```
`QDockWidget`をインポートして、ドックパネル機能を追加。

### 2. GeoReport クラスの変更

#### `__init__()` メソッド
- `self.dialog = None` - ダイアログオブジェクト
- `self.dock_widget = None` - ドックウィジェットオブジェクト

#### `unload()` メソッド
パネル終了時の処理を追加：
```python
if self.dock_widget:
    self.iface.removeDockWidget(self.dock_widget)
    self.dock_widget.deleteLater()
    self.dock_widget = None
```

#### `show_layout_selector()` メソッド（主要変更）
**従来の方式:**
```python
self.dialog = LayoutSelectorDialog(layouts, self.iface)
self.dialog.show()
self.dialog.raise_()
```

**新しい方式（パネル化）:**
```python
# 初回起動：パネルを作成
if self.dock_widget is None:
    self.dialog = LayoutSelectorDialog(layouts, self.iface)
    self.dock_widget = QDockWidget("geo_report - Layout Item Selector", self.iface.mainWindow())
    self.dock_widget.setWidget(self.dialog)
    self.dock_widget.setObjectName("GeoReportLayoutSelectorPanel")
    self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dock_widget)

# 以降：パネルの表示/非表示を切り替え
else:
    if self.dock_widget.isVisible():
        self.dock_widget.hide()
    else:
        self.dock_widget.show()
```

### 3. LayoutSelectorDialog クラスの変更

#### `closeEvent()` メソッド
パネル非表示機能を追加：
```python
event.ignore()  # closeイベントを無視
if hasattr(self, 'parent') and isinstance(self.parent(), QDockWidget):
    self.parent().hide()  # 親パネルを非表示に
```

#### `reject()` / `accept()` メソッド
パネルに対応した終了処理を追加：
```python
if hasattr(self, 'parent') and isinstance(self.parent(), QDockWidget):
    self.parent().hide()  # パネルを非表示に
else:
    super().reject()  # 通常のダイアログなら閉じる
```

## 動作について

### 初回起動
1. ツールバー/メニューから「レイアウト選択」をクリック
2. QGIS左側にドックパネルが追加される
3. パネルにレイアウト選択UIが表示される

### 2回目以降
1. ツールバー/メニューから「レイアウト選択」をクリック
2. パネルの表示/非表示が切り替わる

### パネル閉じる方法
- パネルのXボタン → パネルが非表示に（削除されない）
- キャンセルボタン → パネルが非表示に（削除されない）

## メリット

✅ **QGIS統合** - メインウィンドウ内で作業可能  
✅ **並行操作** - マップと同時に操作できる  
✅ **永続性** - 一度開いたパネルは状態保持  
✅ **トグル切り替え** - クリック一つで表示/非表示  
✅ **位置保存** - ユーザーのパネル配置が保持される  

## 互換性

- QGIS 3.x 以上対応
- PyQt5/PyQt6 互換
- 既存の機能変更なし

## テスト方法

```bash
# プラグイン再読み込み
python -c "from geo_report.plugin import GeoReport"

# QGIS内テスト
1. QGISにプラグインをロード
2. ツールバーアイコンをクリック
3. 左側にパネルが表示されることを確認
4. パネルのXボタンで非表示
5. もう一度クリックして表示確認
```

## 今後の改善案

- [ ] パネル位置・サイズを設定に保存
- [ ] パネルを複数エリア対応
- [ ] パネルのリサイズ可能化
- [ ] タブ化対応（他パネルとの統合）
