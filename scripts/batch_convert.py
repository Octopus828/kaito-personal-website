#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KaitoVaultからWebサイト用HTMLファイルを一括生成するスクリプト
内蔵のfix_html.pyを使用してHTML変換を行う
"""

import os
import re
import sys
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime

class KaitoVaultConverter:
    def __init__(self, vault_path, output_path):
        self.vault_path = Path(vault_path)
        self.output_path = Path(output_path)
        # 同じディレクトリのfix_html.pyを参照
        self.fix_html_script = Path(__file__).parent / "fix_html.py"
        
    def _md_to_html_minimal(self, md_path):
        """pandoc が使えない場合の簡易 md→HTML（frontmatter 除去・見出しと段落のみ）"""
        text = Path(md_path).read_text(encoding='utf-8')
        if text.startswith('---'):
            end = text.find('---', 3)
            if end != -1:
                text = text[end + 3:].lstrip()
        lines = text.split('\n')
        out = []
        in_para = False
        in_blockquote = False
        for line in lines:
            # Markdown 引用: 行頭が >
            if line.startswith('> '):
                if in_para:
                    out.append('</p>')
                    in_para = False
                if not in_blockquote:
                    out.append('<blockquote><p>')
                    in_blockquote = True
                else:
                    out.append('</p><p>')
                out.append(line[2:].strip().replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            elif line.strip() == '>' or (line.startswith('>') and not line.startswith('> ')):
                # 行が ">" のみ、または ">テキスト"（スペースなし）のとき
                if in_para:
                    out.append('</p>')
                    in_para = False
                q = line.lstrip('>').strip()
                if not in_blockquote:
                    out.append('<blockquote><p>')
                    in_blockquote = True
                else:
                    out.append('</p><p>')
                if q:
                    out.append(q.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
            elif line.strip():
                if in_blockquote:
                    out.append('</p></blockquote>')
                    in_blockquote = False
                if not in_para:
                    out.append('<p>')
                    in_para = True
                out.append(line.strip())
                out.append(' ')
            else:
                if in_blockquote:
                    out.append('</p></blockquote>')
                    in_blockquote = False
                if in_para:
                    out.append('</p>')
                    in_para = False
        if in_blockquote:
            out.append('</p></blockquote>')
        if in_para:
            out.append('</p>')
        body = '\n'.join(out).strip()
        return f'<!DOCTYPE html><html><head><title>Document</title></head><body>{body}</body></html>'
    
    def convert_file(self, md_file, html_file):
        """単一ファイルを変換（.md の場合は pandoc で HTML 化してから fix_html）"""
        md_file = Path(md_file)
        html_file = Path(html_file)
        try:
            if md_file.suffix.lower() == '.md':
                tmp_path = None
                try:
                    r = subprocess.run(
                        ['pandoc', str(md_file), '-o', '-', '--standalone'],
                        capture_output=True, text=True
                    )
                    if r.returncode == 0 and r.stdout:
                        tmp_path = tempfile.mktemp(suffix='.html')
                        Path(tmp_path).write_text(r.stdout, encoding='utf-8')
                    else:
                        # pandoc がない or 失敗 → 簡易変換
                        html_content = self._md_to_html_minimal(md_file)
                        tmp_path = tempfile.mktemp(suffix='.html')
                        Path(tmp_path).write_text(html_content, encoding='utf-8')
                except FileNotFoundError:
                    html_content = self._md_to_html_minimal(md_file)
                    tmp_path = tempfile.mktemp(suffix='.html')
                    Path(tmp_path).write_text(html_content, encoding='utf-8')
                if tmp_path:
                    try:
                        cmd = [
                            "python", str(self.fix_html_script),
                            tmp_path, str(html_file)
                        ]
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode != 0:
                            print(f"❌ 変換失敗: {md_file.name}")
                            print(f"エラー: {result.stderr}")
                            return False
                    finally:
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
                else:
                    return False
            else:
                cmd = [
                    "python", str(self.fix_html_script),
                    str(md_file), str(html_file)
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"❌ 変換失敗: {md_file.name}")
                    print(f"エラー: {result.stderr}")
                    return False
            print(f"✅ 変換完了: {md_file.name} → {html_file.name}")
            return True
        except Exception as e:
            print(f"❌ 実行エラー: {e}")
            return False
    
    def get_file_title(self, md_file):
        """Markdownファイルからタイトル（YAML frontmatter または最初の h1）を取得"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if content.startswith('---'):
                yaml_end = content.find('---', 3)
                if yaml_end != -1:
                    yaml_content = content[3:yaml_end]
                    m = re.search(r'^title:\s*(.+)$', yaml_content, re.MULTILINE)
                    if m:
                        return m.group(1).strip().strip('"\'')
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    return line[2:].strip()
        except Exception:
            pass
        return Path(md_file).stem
    
    def convert_music_content(self):
        """音楽関連コンテンツを変換"""
        music_path = self.vault_path / "30_Music"
        if not music_path.exists():
            return []
            
        converted = []
        
        # ベースレパートリー
        bass_file = music_path / "PracticeLogs" / "bass_repertoire.md"
        if bass_file.exists():
            output_file = self.output_path / "bass_repertoire.html"
            if self.convert_file(bass_file, output_file):
                converted.append({
                    'file': 'bass_repertoire.html',
                    'title': 'ベース練習記録',
                    'category': 'music'
                })
        
        return converted
    
    def convert_research_content(self):
        """研究関連コンテンツを変換"""
        research_path = self.vault_path / "10_Research"
        if not research_path.exists():
            return []
            
        converted = []
        
        # プロジェクトREADMEファイル
        projects_path = research_path / "10_Projects"
        if projects_path.exists():
            for project_dir in projects_path.iterdir():
                if project_dir.is_dir():
                    readme_file = project_dir / "README.md"
                    if readme_file.exists():
                        output_file = self.output_path / f"research_{project_dir.name}.html"
                        if self.convert_file(readme_file, output_file):
                            title = self.get_file_title(readme_file)
                            converted.append({
                                'file': f"research_{project_dir.name}.html",
                                'title': title,
                                'category': 'research'
                            })
        
        return converted
    
    def convert_diary_content(self):
        """日記コンテンツを変換（40_LifeLog/Diary/*.md → docs/diary/YYYY-MM-DD.html）"""
        diary_path = self.vault_path / "40_LifeLog" / "Diary"
        if not diary_path.exists():
            return []
        out_diary = self.output_path / "diary"
        out_diary.mkdir(parents=True, exist_ok=True)
        converted = []
        # YYYY-MM-DD.md 形式のファイルを日付の新しい順で処理
        md_files = sorted(
            [f for f in diary_path.iterdir() if f.suffix.lower() == '.md' and f.is_file()],
            key=lambda p: p.stem,
            reverse=True
        )
        for md_file in md_files:
            # ファイル名が YYYY-MM-DD 形式か簡易チェック
            stem = md_file.stem
            output_file = out_diary / f"{stem}.html"
            if self.convert_file(md_file, output_file):
                title = self.get_file_title(md_file)
                converted.append({
                    'file': f"diary/{stem}.html",
                    'title': title,
                    'date': stem,
                    'category': 'diary'
                })
        return converted
    
    def write_diary_index(self, diary_entries):
        """日記一覧ページ docs/diary/index.html を生成"""
        if not diary_entries:
            return
        out_diary = self.output_path / "diary"
        out_diary.mkdir(parents=True, exist_ok=True)
        index_file = out_diary / "index.html"
        # ナビは docs/diary/ からなので ../ でトップへ
        nav_base = "../"
        # 一覧は docs/diary/index.html なので、リンクは同階層の YYYY-MM-DD.html
        items_html = "\n".join(
            f'                <li><a href="{e["date"]}.html">{e["date"]}: {e["title"]}</a></li>'
            for e in diary_entries
        )
        html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日記 - Kaito's Personal Website</title>
    <style>
        body {{ font-family: 'Arial', sans-serif; line-height: 1.6; margin: 0; padding: 0; color: #333; background-color: #f4f4f4; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; text-align: center; }}
        nav {{ background: #333; padding: 1rem 0; }}
        nav ul {{ list-style: none; padding: 0; margin: 0; display: flex; justify-content: center; }}
        nav ul li {{ margin: 0 20px; }}
        nav ul li a {{ color: white; text-decoration: none; padding: 10px 15px; border-radius: 5px; transition: background-color 0.3s; }}
        nav ul li a:hover {{ background-color: #555; }}
        main {{ background: white; margin: 2rem 0; padding: 2rem; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        main h2 {{ color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 0.5rem; }}
        main ul {{ list-style: none; padding: 0; }}
        main ul li {{ margin: 0.8em 0; }}
        main ul li a {{ color: #667eea; text-decoration: none; }}
        main ul li a:hover {{ text-decoration: underline; }}
        footer {{ background: #333; color: white; text-align: center; padding: 2rem 0; margin-top: 3rem; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>📝 日記</h1>
            <p>Kaito's Personal Website</p>
        </div>
    </header>
    <nav>
        <div class="container">
            <ul>
                <li><a href="{nav_base}index.html">Home</a></li>
                <li><a href="{nav_base}index.html#research">Research</a></li>
                <li><a href="{nav_base}index.html#music">Music</a></li>
                <li><a href="{nav_base}index.html#blog">Blog</a></li>
                <li><a href="index.html">Diary</a></li>
            </ul>
        </div>
    </nav>
    <div class="container">
        <main>
            <h2>日記一覧</h2>
            <ul>
{items_html}
            </ul>
        </main>
    </div>
    <footer>
        <div class="container">
            <p>&copy; 2025 Kaito's Personal Website. Built with ❤️ and hosted on GitHub Pages.</p>
        </div>
    </footer>
</body>
</html>
'''
        index_file.write_text(html, encoding='utf-8')
        print(f"✅ 日記一覧: {index_file}")
    
    def update_navigation(self, converted_files):
        """index.htmlのナビゲーションを更新"""
        index_file = self.output_path / "index.html"
        if not index_file.exists():
            return
            
        # 簡単な文字列置換でリンクを追加
        # 実際の実装では、より適切なHTML解析を使用
        print("📝 ナビゲーション更新は手動で行ってください:")
        
        music_files = [f for f in converted_files if f['category'] == 'music']
        research_files = [f for f in converted_files if f['category'] == 'research']
        diary_files = [f for f in converted_files if f['category'] == 'diary']
        
        if music_files:
            print("\n🎵 Music セクションに追加:")
            for file_info in music_files:
                print(f"  <li><a href=\"{file_info['file']}\">{file_info['title']}</a></li>")
        
        if research_files:
            print("\n🔬 Research セクションに追加:")
            for file_info in research_files:
                print(f"  <li><a href=\"{file_info['file']}\">{file_info['title']}</a></li>")
        
        if diary_files:
            print("\n📝 Diary セクションに追加:")
            for file_info in diary_files:
                print(f"  <li><a href=\"{file_info['file']}\">{file_info['title']}</a></li>")
    
    def run(self):
        """メイン実行"""
        print("🚀 KaitoVault → Website 変換を開始...")
        print(f"📁 Vault: {self.vault_path}")
        print(f"📁 Output: {self.output_path}")
        print(f"🔧 HTML変換ツール: {self.fix_html_script}")
        
        if not self.fix_html_script.exists():
            print(f"❌ fix_html.pyが見つかりません: {self.fix_html_script}")
            return
        
        # 出力ディレクトリを作成
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # 変換実行（現在は日記のみ。音楽・研究は将来必要時に convert_music_content / convert_research_content を復活）
        converted_files = []
        diary_files = self.convert_diary_content()
        converted_files.extend(diary_files)
        self.write_diary_index(diary_files)
        
        # 結果表示
        print(f"\n✅ 変換完了: {len(converted_files)} ファイル")
        for file_info in converted_files:
            print(f"  - {file_info['title']} ({file_info['file']})")
        
        # ナビゲーション更新の提案
        self.update_navigation(converted_files)
        
        print(f"\n🌐 サイトURL: https://octopus828.github.io/kaito-personal-website/")
        print("💡 変更をGitHubにプッシュしてください:")
        print("   git add . && git commit -m \"Add batch converted content\" && git push origin main")

def main():
    if len(sys.argv) != 3:
        print("使用法: python batch_convert.py <vault_path> <output_path>")
        print("例: python batch_convert.py ../KaitoVault docs")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    output_path = sys.argv[2]
    
    converter = KaitoVaultConverter(vault_path, output_path)
    converter.run()

if __name__ == "__main__":
    main() 