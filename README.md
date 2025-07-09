# Kaito's Personal Website

Kaito の個人ウェブサイト用プロジェクト。研究活動とブラジル音楽の情報を発信します。

## 📁 プロジェクト構造

```
website_personal/
├── docs/           # GitHub Pages用の公開ディレクトリ
│   ├── index.html  # メインページ
│   └── *.html      # 各コンテンツページ
├── scripts/        # 変換・管理ツール
│   ├── batch_convert.py  # KaitoVault→HTML一括変換
│   └── fix_html.py       # HTML修正ツール（内蔵）
├── src/            # 開発用ソースファイル
├── public/         # 静的アセット
├── content/        # 下書きコンテンツ
└── README.md       # このファイル
```

## 🌐 サイトURL

- **本番サイト**: https://octopus828.github.io/kaito-personal-website/

## 🔧 コンテンツ変換ツール

### 1. 個別ファイル変換（推奨）

**最も安全で確実な方法**です。一つずつファイルを確認しながら変換できます。

```bash
# 基本的な変換
python scripts/fix_html.py input.md output.html

# Markdownファイルがある場合は事前にpandocでHTML化
pandoc input.md -o temp.html
python scripts/fix_html.py temp.html output.html
```

### 2. 一括変換（要注意）

**必ず事前にバックアップを取り、変換対象を確認してください**。

```bash
# KaitoVaultから一括変換
python scripts/batch_convert.py ../KaitoVault docs

# 変換されるファイル例:
# - 30_Music/PracticeLogs/bass_repertoire.md → bass_repertoire.html
# - 10_Research/10_Projects/*/README.md → research_*.html
```

#### ⚠️ 一括変換の注意事項

一括変換を実行する前に、以下をチェックしてください：

- [ ] 変換対象ファイルに**機密情報**が含まれていないか
- [ ] 変換対象ファイルに**個人的すぎる内容**が含まれていないか  
- [ ] 変換対象ファイルが**公開可能な状態**になっているか
- [ ] 変換前にGitで現在の状態をコミットしているか

### 3. 安全な変換フロー

1. **事前確認**: 変換対象のファイルを手動で確認
2. **バックアップ**: `git add . && git commit -m "Before batch conversion"`
3. **変換実行**: `python scripts/batch_convert.py ../KaitoVault docs`
4. **結果確認**: 生成されたHTMLファイルを確認
5. **公開**: 問題なければ `git push origin main`

## 🎵 音楽コンテンツ変換例

```bash
# ベース練習記録を変換
python scripts/fix_html.py ../KaitoVault/30_Music/PracticeLogs/bass_repertoire.md docs/bass_repertoire.html
```

## 🔬 研究コンテンツ変換例

```bash
# 研究プロジェクトREADMEを変換
python scripts/fix_html.py ../KaitoVault/10_Research/10_Projects/project_name/README.md docs/research_project_name.html
```

## 🔄 更新フロー

1. **KaitoVault**でコンテンツを更新
2. **変換ツール**でHTMLファイルを生成
3. **index.html**にリンクを追加（必要に応じて）
4. **Git**にコミット・プッシュ
5. **GitHub Pages**で自動デプロイ

## 🛠️ 技術スタック

- **HTML/CSS**: 手書きのレスポンシブデザイン
- **変換ツール**: Python (Pandoc + カスタムスクリプト)
- **ホスティング**: GitHub Pages
- **バージョン管理**: Git

## 📝 コンテンツ管理

- **原稿**: `KaitoVault/` で管理（Obsidian）
- **変換**: `scripts/` のツールで自動化
- **公開**: `docs/` に配置してGitHub Pagesで公開

---

**Last Updated**: 2025-07-09  
**Version**: 1.1.0  
**Author**: Kaito Sano

## 🔄 変更履歴

- **v1.1.0**: batch_convert.pyの依存関係を内蔵化、fix_html.pyを統合
- **v1.0.0**: 初期リリース、基本的な変換機能