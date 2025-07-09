# Kaito's Personal Website

GitHub Pagesを使用したブラジル音楽と研究をテーマにした個人ウェブサイトです。

## 🎯 コンセプト

- **Research**: 認知科学、心理学、リスク認知に関する研究
- **Brazilian Music**: サンバ、ボサノヴァ、ショーロなどブラジル音楽の探求
- **Life**: 日常の気づきや学びの共有

## 📁 プロジェクト構成

```
personal_website/
├── docs/                    # GitHub Pages公開用ディレクトリ
│   ├── index.html          # メインページ
│   ├── research.html       # 研究ページ（予定）
│   ├── music.html          # 音楽ページ（予定）
│   ├── about.html          # プロフィールページ（予定）
│   └── blog.html           # ブログページ（予定）
├── src/                     # ソースファイル
├── public/                  # 静的ファイル（画像、CSS、JS）
├── content/                 # コンテンツ管理
│   ├── about/
│   ├── research/
│   ├── music/
│   └── blog/
└── README.md               # このファイル
```

## 🚀 GitHub Pages設定手順

### 1. GitHubリポジトリの作成

```bash
# リポジトリを作成（GitHub上で）
# 例: kaito-personal-website

# ローカルでGit初期化
cd personal_website
git init
git add .
git commit -m "Initial commit: Add basic HTML structure"
git branch -M main
git remote add origin https://github.com/yourusername/kaito-personal-website.git
git push -u origin main
```

### 2. GitHub Pages設定

1. GitHubリポジトリの**Settings**に移動
2. 左サイドバーから**Pages**を選択
3. Source設定:
   - **Deploy from a branch**を選択
   - Branch: **main**
   - Folder: **/ (root)**または**/docs**
4. **Save**をクリック

### 3. カスタムドメイン（オプション）

独自ドメインを使用する場合：
1. `docs/CNAME`ファイルを作成
2. ドメイン名を記入（例: `kaito.example.com`）
3. DNS設定でGitHub Pagesを指定

## 🛠️ 開発・更新方法

### 基本的なHTMLファイル更新

```bash
# ファイルを編集
vim docs/index.html

# 変更をプッシュ
git add .
git commit -m "Update homepage content"
git push origin main
```

### KaitoVaultからのコンテンツ変換

#### 個別ファイル変換（推奨）
```bash
# 個別のMarkdownファイルをHTMLに変換
python ../dev_projects/temp_html/fix_html.py \
  ../KaitoVault/30_Music/PracticeLogs/bass_repertoire.md \
  docs/bass_repertoire.html
```

#### バッチ処理（要注意）
```bash
# 複数ファイルを一括変換（公開対象を事前に確認すること）
python scripts/batch_convert.py ../KaitoVault docs ../dev_projects/temp_html
```

**⚠️ 注意**: KaitoVaultには個人的・機密的な内容も含まれています。バッチ処理使用前に、公開対象ファイルを必ず確認してください。

### Jekyll使用への移行（将来的）

より高度な機能が必要になった場合：

```bash
# Jekyll Gem Install
gem install bundler jekyll

# Jekyll初期化
jekyll new . --force

# 設定ファイル編集
vim _config.yml
```

## 📝 コンテンツ管理

### KaitoVaultとの連携

既存のObsidianコンテンツを活用：

```bash
# 研究関連コンテンツ
../KaitoVault/10_Research/ → content/research/

# 音楽関連コンテンツ
../KaitoVault/30_Music/ → content/music/

# ブログ記事
../KaitoVault/10_Research/20_Memos/ → content/blog/
```

### コンテンツ変換スクリプト（今後作成予定）

```bash
# Markdown → HTML変換
python scripts/convert_obsidian_to_html.py

# 画像ファイルの処理
python scripts/process_images.py
```

## 🎨 デザインカスタマイズ

現在のデザイン特徴：
- **レスポンシブデザイン**: モバイル対応
- **グラデーション**: 紫系のモダンな配色
- **カードレイアウト**: 各セクションをカード形式で表示
- **アニメーション**: ホバーエフェクトなど

### CSS変更

```css
/* メインカラーの変更 */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ffd700;
}
```

## 📊 アクセス解析

Google Analyticsの追加：

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## 🤖 自動化ツール

### batch_convert.py
KaitoVaultから選択的にコンテンツを変換するPythonスクリプト

**現在の変換対象**:
- `KaitoVault/30_Music/PracticeLogs/bass_repertoire.md` → `docs/bass_repertoire.html`
- `KaitoVault/10_Research/10_Projects/*/README.md` → `docs/research_*.html`

**使用前チェックリスト**:
- [ ] 変換対象ファイルに機密情報が含まれていないか確認
- [ ] YAMLメタデータのタイトルが適切か確認
- [ ] 変換後にindex.htmlのナビゲーションを手動更新

## 🔧 今後の拡張予定

- [ ] Jekyllへの移行
- [ ] ブログ機能の実装
- [ ] 検索機能の追加
- [ ] 多言語対応（英語）
- [ ] コンテンツ管理システム（CMS）連携
- [ ] 自動デプロイ（GitHub Actions）
- [ ] バッチ処理の公開対象ファイル設定機能

## 📞 サポート

質問や問題がある場合は、GitHubのIssuesまたはKaitoVaultの関連ノートで管理してください。

---

**Last Updated**: 2025-07-09  
**Version**: 1.0.0  
**Author**: Kaito Sano