# Kaito's Personal Website Project Context

**新しいチャットセッション用のコンテキスト情報**

## 📍 プロジェクトの現在地

- **作業ディレクトリ**: `/Users/kaito-sa/KaitoEnv/website_personal`
- **KaitoVault（コンテンツ元）**: `/Users/kaito-sa/KaitoEnv/KaitoVault`
- **公開サイト**: https://octopus828.github.io/kaito-personal-website/
- **GitHubリポジトリ**: https://github.com/Octopus828/kaito-personal-website
- **プロジェクト状態**: 稼働中（GitHub Pages公開済み）

**⚠️ 重要**: KaitoVaultはwebsite_personalの外部にあります（../KaitoVault）

## 🎯 プロジェクトの目的

Kaito（認知科学研究者）の個人ウェブサイト。研究活動とブラジル音楽の両方を発信するプラットフォーム。

## 📁 プロジェクト構造

```
/Users/kaito-sa/KaitoEnv/
├── website_personal/          # 👈 作業ディレクトリ
│   ├── docs/                  # GitHub Pages公開ディレクトリ
│   │   ├── index.html        # メインページ（稼働中）
│   │   └── samba_carnaval.html # サンバ記事（公開済み）
│   ├── scripts/               # 変換ツール（独立・統合済み）
│   │   ├── batch_convert.py  # KaitoVault→HTML一括変換
│   │   └── fix_html.py       # HTML修正ツール
│   ├── src/                   # 開発用ソース
│   ├── public/                # 静的アセット
│   ├── content/               # 下書きコンテンツ
│   └── README.md             # プロジェクトドキュメント
│
└── KaitoVault/                # 👈 コンテンツ元（../KaitoVault）
    ├── 30_Music/
    │   └── PracticeLogs/
    │       └── bass_repertoire.md
    └── 10_Research/
        └── 10_Projects/
            └── */README.md
```

## 🔧 主要ツール

### 1. 個別ファイル変換
```bash
python scripts/fix_html.py input.md output.html
```

### 2. 一括変換（要注意）
```bash
# 作業ディレクトリ: /Users/kaito-sa/KaitoEnv/website_personal
python scripts/batch_convert.py ../KaitoVault docs
```

**⚠️ 重要**: 
- KaitoVaultはwebsite_personalの外部（../KaitoVault）にあります
- 機密情報が含まれる可能性があるため、一括変換前に必ず内容を確認すること

## 🌐 現在公開中のコンテンツ

- **メインページ**: `index.html` - 研究・音楽・プロフィール・ブログセクション
- **サンバ記事**: `samba_carnaval.html` - 浅草サンバカーニバルの詳細解説

## 🔄 標準的な更新フロー

1. **KaitoVault** でコンテンツを作成・編集
2. **変換ツール** でHTMLファイルを生成
3. **リンク追加** index.htmlにナビゲーションを追加
4. **Git操作** `git add . && git commit -m "..." && git push origin main`
5. **自動デプロイ** GitHub Pagesで数分後に反映

## 🛠️ 技術スタック

- **HTML/CSS**: 手書きレスポンシブデザイン（紫グラデーション）
- **変換**: Python + Pandoc + カスタムスクリプト
- **ホスティング**: GitHub Pages（自動デプロイ）
- **コンテンツ管理**: Obsidian（KaitoVault）
- **バージョン管理**: Git

## 📊 現在の変換対象

- `../KaitoVault/30_Music/PracticeLogs/bass_repertoire.md` → `bass_repertoire.html`
- `../KaitoVault/10_Research/10_Projects/*/README.md` → `research_*.html`

## 🔐 セキュリティ考慮事項

- **機密情報チェック**: 変換前に必ずファイル内容を確認
- **公開範囲限定**: 研究・音楽関連の適切なコンテンツのみ
- **バックアップ**: 変換前に必ずgitコミット

## 🎨 デザイン特徴

- **レスポンシブデザイン**: モバイル・タブレット対応
- **カラーテーマ**: 紫系グラデーション（#667eea → #764ba2）
- **レイアウト**: カードベース、グリッドシステム
- **アニメーション**: ホバーエフェクト、トランジション

## 🚀 よくある作業

### 新しいコンテンツの追加
```bash
# 作業ディレクトリ: /Users/kaito-sa/KaitoEnv/website_personal

# 1. KaitoVaultでMarkdownを作成
# 2. HTMLに変換
python scripts/fix_html.py ../KaitoVault/path/to/file.md docs/new_content.html

# 3. index.htmlにリンク追加
# 4. Git操作
git add . && git commit -m "Add new content" && git push origin main
```

### 既存コンテンツの更新
```bash
# 作業ディレクトリ: /Users/kaito-sa/KaitoEnv/website_personal

# 1. KaitoVaultで編集
# 2. 再変換
python scripts/fix_html.py ../KaitoVault/path/to/file.md docs/existing_content.html

# 3. プッシュ
git add . && git commit -m "Update content" && git push origin main
```

## 🎯 今後の展開予定

- [ ] ブログ機能の実装
- [ ] 研究プロジェクトページの追加
- [ ] 音楽コンテンツの拡充
- [ ] 検索機能の追加
- [ ] 多言語対応

## 💡 作業時の注意点

1. **コンテンツの質を重視** - 一般公開に適した内容か確認
2. **リンクの整合性** - 新しいページを追加したらナビゲーションも更新
3. **レスポンシブ確認** - モバイルでの表示も確認
4. **バックアップ重要** - 変更前に必ずgitコミット
5. **プライバシー配慮** - 個人情報や機密情報の漏洩防止

---

**このプロンプトは `/Users/kaito-sa/KaitoEnv/website_personal` での作業開始時に新しいチャットセッションに提供してください。** 