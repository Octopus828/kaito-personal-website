#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML文字化け修正スクリプト
pandocで生成されたHTMLファイルに適切なDOCTYPE、文字コード設定を追加
"""

import os
import re
import sys
from pathlib import Path

def fix_html_file(input_file, output_file=None):
    """
    HTMLファイルを修正する関数
    
    Args:
        input_file (str): 修正対象のHTMLファイルパス
        output_file (str, optional): 出力ファイルパス。Noneの場合は上書き
    """
    
    # ファイルを読み込み
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # UTF-8で読み込めない場合は他の文字コードを試す
        try:
            with open(input_file, 'r', encoding='shift_jis') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='euc-jp') as f:
                content = f.read()
    
    # 修正済みのHTMLヘッダー（高度なレスポンシブデザイン）
    html_header = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        /* ====================
           リセット & 基本設定
        ==================== */
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #ffffff;
            color: #333333;
            font-size: 16px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}

        /* ====================
           ヘッダー階層
        ==================== */
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2.5em;
            margin-bottom: 1em;
            font-weight: 600;
            line-height: 1.3;
        }}

        h1 {{
            font-size: 2.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-top: 0;
        }}

        h2 {{
            font-size: 2em;
            border-bottom: 2px solid #bdc3c7;
            padding-bottom: 10px;
        }}

        h3 {{
            font-size: 1.5em;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 5px;
        }}

        h4 {{
            font-size: 1.25em;
            color: #34495e;
        }}

        h5 {{
            font-size: 1.1em;
            color: #34495e;
        }}

        h6 {{
            font-size: 1em;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* ====================
           テキスト要素
        ==================== */
        p {{
            margin-bottom: 1.5em;
            line-height: 1.7;
        }}

        /* ====================
           コードブロック
        ==================== */
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.5;
            margin: 1.5em 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            font-size: inherit;
        }}

        code {{
            background-color: #f8f9fa;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Consolas', 'Courier New', monospace;
            font-size: 0.9em;
            color: #e74c3c;
            border: 1px solid #e9ecef;
        }}

        /* ====================
           引用
        ==================== */
        blockquote {{
            border-left: 5px solid #3498db;
            margin: 1.5em 0;
            padding: 15px 20px;
            background-color: #f8f9fa;
            font-style: italic;
            color: #555;
            border-radius: 0 8px 8px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        blockquote p:last-child {{
            margin-bottom: 0;
        }}

        /* ====================
           リスト
        ==================== */
        ul, ol {{
            margin-bottom: 1.5em;
            padding-left: 2em;
        }}

        li {{
            margin-bottom: 0.5em;
        }}

        /* ====================
           テーブル
        ==================== */
        .table-container {{
            overflow-x: auto;
            margin: 1.5em 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            min-width: 500px;
            background-color: #ffffff;
        }}

        th, td {{
            border: 1px solid #dee2e6;
            padding: 12px 15px;
            text-align: left;
            vertical-align: top;
        }}

        th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        tr:hover {{
            background-color: #e3f2fd;
        }}

        /* ====================
           画像
        ==================== */
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 1em 0;
        }}

        /* ====================
           動画（iframe）
        ==================== */
        iframe {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 1em 0;
        }}

        /* ====================
           リンク
        ==================== */
        a {{
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.3s ease;
        }}

        a:hover {{
            color: #2980b9;
            border-bottom-color: #2980b9;
        }}

        /* ====================
           レスポンシブ: タブレット
        ==================== */
        @media (max-width: 1024px) {{
            body {{
                padding: 30px 15px;
                font-size: 15px;
            }}

            h1 {{
                font-size: 2.2em;
            }}

            h2 {{
                font-size: 1.8em;
            }}

            h3 {{
                font-size: 1.4em;
            }}

            pre {{
                padding: 15px;
                font-size: 13px;
            }}

            th, td {{
                padding: 10px 12px;
            }}

            iframe {{
                width: 100%;
                height: 250px;
            }}
        }}

        /* ====================
           レスポンシブ: スマホ
        ==================== */
        @media (max-width: 768px) {{
            body {{
                padding: 20px 10px;
                font-size: 14px;
                line-height: 1.6;
            }}

            h1 {{
                font-size: 1.8em;
                margin-top: 0;
                margin-bottom: 0.8em;
            }}

            h2 {{
                font-size: 1.5em;
                margin-top: 2em;
                margin-bottom: 0.8em;
            }}

            h3 {{
                font-size: 1.3em;
                margin-top: 1.5em;
                margin-bottom: 0.6em;
            }}

            h4, h5, h6 {{
                margin-top: 1.2em;
                margin-bottom: 0.5em;
            }}

            pre {{
                padding: 12px;
                font-size: 12px;
                margin: 1em 0;
            }}

            blockquote {{
                padding: 10px 15px;
                margin: 1em 0;
            }}

            ul, ol {{
                padding-left: 1.5em;
            }}

            th, td {{
                padding: 8px 10px;
                font-size: 13px;
            }}

            table {{
                min-width: 400px;
            }}

            iframe {{
                width: 100%;
                height: 200px;
            }}
        }}

        /* ====================
           レスポンシブ: 小さいスマホ
        ==================== */
        @media (max-width: 480px) {{
            body {{
                padding: 15px 8px;
                font-size: 13px;
            }}

            h1 {{
                font-size: 1.6em;
            }}

            h2 {{
                font-size: 1.4em;
            }}

            h3 {{
                font-size: 1.2em;
            }}

            pre {{
                padding: 10px;
                font-size: 11px;
            }}

            th, td {{
                padding: 6px 8px;
                font-size: 12px;
            }}

            table {{
                min-width: 320px;
            }}

            iframe {{
                width: 100%;
                height: 180px;
            }}
        }}

        /* ====================
           印刷スタイル
        ==================== */
        @media print {{
            body {{
                max-width: none;
                padding: 0;
                font-size: 12pt;
                line-height: 1.5;
                color: #000;
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: #000;
                page-break-after: avoid;
            }}

            pre, blockquote {{
                page-break-inside: avoid;
                background-color: #f5f5f5 !important;
                box-shadow: none;
            }}

            a {{
                color: #000;
                text-decoration: underline;
            }}

            img {{
                max-width: 100% !important;
                box-shadow: none;
            }}

            iframe {{
                display: none;
            }}
        }}

        /* ====================
           ダークモード対応
        ==================== */
        @media (prefers-color-scheme: dark) {{
            body {{
                background-color: #1a1a1a;
                color: #e0e0e0;
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: #ffffff;
            }}

            pre {{
                background-color: #2d2d2d;
                border-color: #404040;
            }}

            code {{
                background-color: #2d2d2d;
                color: #ff6b6b;
                border-color: #404040;
            }}

            blockquote {{
                background-color: #2d2d2d;
                border-left-color: #3498db;
            }}

            table {{
                background-color: #1a1a1a;
            }}

            th {{
                background-color: #2d2d2d;
                color: #ffffff;
            }}

            tr:nth-child(even) {{
                background-color: #2d2d2d;
            }}

            tr:hover {{
                background-color: #3d3d3d;
            }}

            th, td {{
                border-color: #404040;
            }}
        }}
    </style>
</head>
<body>
'''
    
    # タイトルを抽出（存在する場合）
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Document"
    
    # body内のコンテンツを抽出
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
    else:
        # bodyタグがない場合は、HTML全体をbodyとして扱う
        # HTMLタグとheadタグを削除
        body_content = re.sub(r'<html[^>]*>', '', content, flags=re.IGNORECASE)
        body_content = re.sub(r'</html>', '', body_content, flags=re.IGNORECASE)
        body_content = re.sub(r'<head>.*?</head>', '', body_content, flags=re.DOTALL | re.IGNORECASE)
    
    # 修正されたHTMLを構築（JavaScriptを追加）
    javascript_section = '''
    <!-- テーブルを自動でラップする JavaScript -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // テーブルを自動でコンテナにラップ
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                if (!table.parentElement.classList.contains('table-container')) {
                    const container = document.createElement('div');
                    container.className = 'table-container';
                    table.parentNode.insertBefore(container, table);
                    container.appendChild(table);
                }
            });
        });
    </script>
'''
    
    fixed_html = html_header.format(title=title) + body_content + javascript_section + '\n</body>\n</html>'
    
    # 出力ファイル名を決定
    if output_file is None:
        output_file = input_file
    
    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_html)
    
    print(f"修正完了: {output_file}")

def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python fix_html.py <HTMLファイルパス> [出力ファイルパス]")
        print("例: python fix_html.py exports/document.html")
        print("例: python fix_html.py exports/document.html exports/document_fixed.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"エラー: ファイル '{input_file}' が見つかりません。")
        sys.exit(1)
    
    fix_html_file(input_file, output_file)

if __name__ == "__main__":
    main() 