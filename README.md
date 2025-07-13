# Layout Item Selector / レイアウトアイテム選択プラグイン
**[EN] A QGIS plugin for using one layout as multiple drawings and registers.**  
**[JP] 一つのレイアウトを複数の図面・台帳として利用するためのQGISプラグインです。**  
<img width="994" height="724" alt="image" src="https://github.com/user-attachments/assets/737318cf-7e4b-4657-aac7-272c69f87144" />
## Main Features / 主な機能

**[EN]**
- **Layout Selection & Management**: Display project layout lists and launch manager
- **Item Pre-editing**: Pre-adjust layout item properties (position, size, content)
- **Template Save & Utilization**: Save entire layout properties as JSON and batch apply to other layouts
- **Efficient Workflow**: Efficiently create multiple drawings and registers with unified design
- **Multilingual Support**: English and Japanese language support

**[JP]**
- **レイアウト選択・管理**: プロジェクト内のレイアウト一覧表示とマネージャ起動
- **アイテム事前編集**: レイアウトアイテムのプロパティ（位置・サイズ・内容）を事前調整
- **テンプレート保存・活用**: レイアウト全体のプロパティをJSONで保存し、他のレイアウトに一括適用
- **効率的なワークフロー**: 統一されたデザインで複数の図面・台帳を効率的に作成
- **多言語対応**: 英語・日本語対応

## Usage / 使用方法

**[EN]**
1. Click "Layout Item Selector" → "Layout Selection" from the plugin menu
2. Select target layout from the layout list
3. Pre-check and edit item properties (optional)
4. Use "Save Layout" to create templates (first time)
5. Use "Load Layout" on new layouts to apply templates

**[JP]**
1. プラグインメニューから「Layout Item Selector」→「レイアウト選択」をクリック
2. レイアウト一覧から目的のレイアウトを選択
3. アイテムのプロパティを事前確認・編集（オプション）
4. 「レイアウト全体を保存」でテンプレート化（初回時）
5. 新しいレイアウトで「レイアウト全体を読み込み」してテンプレートを適用

## Installation / インストール

**[EN]**
1. Install from QGIS Plugin Manager, or
2. Copy this folder to QGIS plugin directory and enable

**[JP]**
1. QGISプラグインマネージャーからインストール、または
2. このフォルダをQGISプラグインディレクトリにコピーして有効化

## 活用例

### 🎯 **効率的な図面・台帳作成**
- **図面テンプレート**: 同じレイアウト構成で複数地域の図面作成
- **台帳フォーマット**: 標準レイアウトの複数案件での再利用
- **シリーズ地図**: 統一デザインでの主題図作成

### ✏️ **具体的な編集作業**
- **タイトル一括変更**: 「○○地区現況図」→「△△地区現況図」へレイアウトごとに変更
- **凡例の置き換え**: 土地利用図の凡例を用途地域図の凡例に一括更新
- **スケールバー調整**: 縮尺に応じたスケールバーの位置・サイズを統一設定
- **ロゴ・印影配置**: 会社ロゴや承認印の位置を全図面で統一
- **注記・説明文更新**: 法的記載事項や作成日時を一括で最新化
- **座標系表示変更**: 測地系情報やグリッド表示を案件に応じて調整

## 開発者

yamamoto-ryuzo

## ライセンス

GPL v2.0
