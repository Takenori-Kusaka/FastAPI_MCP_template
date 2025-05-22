"""
API接続テスト

このスクリプトは、FastAPI MCPテンプレートのAPIへの接続をテストします。
"""
import os
import sys
import requests
import json

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_json(data):
    """JSONデータを整形して表示"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_api_server():
    """
    APIサーバーに接続してテスト
    """
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    print(f"\n=== APIサーバーに接続 ({api_base_url}) ===")
    
    try:
        # ルートエンドポイントにアクセス
        url = f"{api_base_url}/"
        response = requests.get(url)
        print(f"ルートエンドポイント - ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print_json(response.json())
        else:
            print(f"エラーレスポンス: {response.text}")
        
        # サンプル一覧エンドポイントにアクセス
        url = f"{api_base_url}/api/examples"
        response = requests.get(url)
        print(f"\nサンプル一覧 - ステータスコード: {response.status_code}")
        if response.status_code == 200:
            print_json(response.json())
        else:
            print(f"エラーレスポンス: {response.text}")
        
        # MCPエンドポイントにアクセス
        url = f"{api_base_url}/mcp"
        response = requests.get(url)
        print(f"\nMCPエンドポイント - ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text[:200]}...")
    except Exception as e:
        print(f"エラー: {e}")

def test_env_vars():
    """
    環境変数をテスト
    """
    print(f"\n=== 環境変数 ===")
    print(f"API_BASE_URL: {os.getenv('API_BASE_URL', 'http://localhost:8000')} (デフォルト: http://localhost:8000)")

if __name__ == "__main__":
    test_env_vars()
    test_api_server()
