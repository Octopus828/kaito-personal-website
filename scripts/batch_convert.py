#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KaitoVaultからWebサイト用HTMLファイルを一括生成するスクリプト
内蔵のfix_html.pyを使用してHTML変換を行う
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path
from datetime import datetime

class KaitoVaultConverter:
    def __init__(self, vault_path, output_path):
        self.vault_path = Path(vault_path)
        self.output_path = Path(output_path)
        # 同じディレクトリのfix_html.pyを参照
        self.fix_html_script = Path(__file__).parent / "fix_html.py"
        
    def convert_file(self, md_file, html_file):
        """単一ファイルを変換"""
        cmd = [
            "python", str(self.fix_html_script),
            str(md_file), str(html_file)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ 変換完了: {md_file.name} → {html_file.name}")
                return True
            else:
                print(f"❌ 変換失敗: {md_file.name}")
                print(f"エラー: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 実行エラー: {e}")
            return False
    
    def get_file_title(self, md_file):
        """MarkdownファイルからタイトルYAMLを取得"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    yaml_end = content.find('---', 3)
                    if yaml_end != -1:
                        yaml_content = content[3:yaml_end]
                        metadata = yaml.safe_load(yaml_content)
                        return metadata.get('title', md_file.stem)
                        
            # YAMLがない場合は最初のh1を探す
            lines = content.split('\n')
            for line in lines:
                if line.startswith('# '):
                    return line[2:].strip()
                    
        except Exception:
            pass
            
        return md_file.stem
    
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
        
        if music_files:
            print("\n🎵 Music セクションに追加:")
            for file_info in music_files:
                print(f"  <li><a href=\"{file_info['file']}\">{file_info['title']}</a></li>")
        
        if research_files:
            print("\n🔬 Research セクションに追加:")
            for file_info in research_files:
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
        
        # 変換実行
        converted_files = []
        converted_files.extend(self.convert_music_content())
        converted_files.extend(self.convert_research_content())
        
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