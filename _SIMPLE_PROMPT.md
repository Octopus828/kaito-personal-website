# 新しいチャットセッション用 - 簡易プロンプト

## 基本情報
- **作業ディレクトリ**: `/Users/kaito-sa/KaitoEnv/website_personal`
- **KaitoVault**: `../KaitoVault`（相対パス）
- **公開サイト**: https://octopus828.github.io/kaito-personal-website/

## 主要ツール
```bash
# 個別変換
python scripts/fix_html.py ../KaitoVault/path/to/file.md docs/output.html

# 一括変換（要注意）
python scripts/batch_convert.py ../KaitoVault docs
```

## 重要事項
- KaitoVaultは外部ディレクトリ（../KaitoVault）
- 機密情報チェック必須
- 変更後はgit push origin main

## 詳細情報
完全なガイドは `CONTEXT_FOR_NEW_CHAT.md` を参照 