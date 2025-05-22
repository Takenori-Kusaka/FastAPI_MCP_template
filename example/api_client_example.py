"""
FastAPI MCP API クライアント使用例

このスクリプトは、FastAPI MCPテンプレートのホスティングされたAPIに
HTTPリクエストを送信して、サンプルデータを操作する方法を示します。
"""
import os
import json
import requests
from datetime import datetime

# APIのベースURL（デフォルトはローカルのDocker環境）
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
# APIのエンドポイントプレフィックス
API_PREFIX = "/api"

def print_json(data):
    """JSONデータを整形して表示"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    # APIサーバーに接続
    print("\n=== FastAPI MCPテンプレートAPIに接続 ===")
    
    # 1. ルートエンドポイントにアクセス
    print("\n=== ルートエンドポイント ===")
    try:
        response = requests.get(f"{API_BASE_URL}")
        response.raise_for_status()
        print_json(response.json())
    except requests.exceptions.RequestException as e:
        print(f"ルートエンドポイントへのアクセスに失敗しました: {e}")
        return

    # 2. サンプル一覧の取得
    print("\n=== サンプル一覧 ===")
    try:
        response = requests.get(f"{API_BASE_URL}{API_PREFIX}/examples")
        response.raise_for_status()
        examples = response.json()
        
        print_json(examples)
        
        if not examples:
            print("サンプルデータがありません。")
            return
            
        # 最初のサンプルIDを取得
        first_example_id = examples[0]["id"]
    except requests.exceptions.RequestException as e:
        print(f"サンプル一覧の取得に失敗しました: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"エラーレスポンス: {e.response.text}")
        return
    
    # 3. 特定のサンプルデータを取得
    print(f"\n=== サンプルID {first_example_id} の詳細 ===")
    try:
        response = requests.get(f"{API_BASE_URL}{API_PREFIX}/examples/{first_example_id}")
        response.raise_for_status()
        example = response.json()
        
        print_json(example)
    except requests.exceptions.RequestException as e:
        print(f"サンプル詳細の取得に失敗しました: {e}")
        return
    
    # 4. MCPエンドポイントの情報を取得
    print("\n=== MCPエンドポイント情報 ===")
    try:
        response = requests.get(f"{API_BASE_URL}/mcp")
        response.raise_for_status()
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"MCPエンドポイントへのアクセスに失敗しました: {e}")

if __name__ == "__main__":
    main()
