# /path/to/project/sanitize_mermaid.py
# タイトル: Mermaidファイル整形スクリプト
# 役割: Mermaidファイル内の絵文字を除去し、必要に応じてノード定義に引用符を追加する
import re
import sys

def sanitize_mermaid_file(filepath):
    """
    Mermaidファイルを読み込み、整形して上書き保存する関数
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"エラー: ファイル '{filepath}' が見つかりません。")
        return

    # 1. 絵文字を除去
    # Pythonの正規表現では \p{...} が直接使えないため、絵文字のUnicode範囲を指定する
    # これは一般的な範囲であり、すべての絵文字をカバーするわけではない
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    content = emoji_pattern.sub('', content)

    # 2. 引用符で囲まれていないノード定義に引用符を追加
    # 例: node[text] -> node["text"] や node{text} -> node{"text"}
    # スペースや括弧を含むテキストを対象とする
    def add_quotes(match):
        # match.groups() -> ('D[', '自律開発環境サービス (DevEnv)', ']')
        start, text, end = match.groups()
        # テキストの前後の空白を除去してから引用符で囲む
        return f'{start}"{text.strip()}"{end}'

    # [...] 形式のノードを検索
    node_pattern_sq = re.compile(r'(\w+\[)([^"\]\n]+)(\])')
    content = node_pattern_sq.sub(add_quotes, content)

    # {...} 形式のノードを検索
    node_pattern_curly = re.compile(r'(\w+\{)([^"\}\n]+)(\})')
    content = node_pattern_curly.sub(add_quotes, content)

    # 3. 整形した内容でファイルを上書き
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"ファイル '{filepath}' の整形が完了しました。")
    except IOError as e:
        print(f"エラー: ファイルの書き込みに失敗しました: {e}")


if __name__ == '__main__':
    # コマンドライン引数からファイルパスを取得
    if len(sys.argv) > 1:
        file_to_sanitize = sys.argv[1]
        sanitize_mermaid_file(file_to_sanitize)
    else:
        print("使い方: python sanitize_mermaid.py <ファイル名>")