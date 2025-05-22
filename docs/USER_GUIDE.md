# FastAPI MCP Template ユーザーガイド

このリポジトリは、FastAPI と Model Context Protocol (MCP) を組み合わせた汎用テンプレートです。  
以下の手順でセットアップし、API と MCP サーバーを起動して動作を確認できます。

## 前提条件

- Python 3.10 以上
- Poetry（依存関係管理）
- Docker（オプション、コンテナ化に使用）

## セットアップ

1. リポジトリをクローン  
   ```bash
   git clone https://github.com/yourusername/fastapi-mcp-template.git
   cd fastapi-mcp-template
   ```

2. 依存関係をインストール  
   ```bash
   poetry install
   ```

3. 開発サーバーを起動  
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

4. ブラウザで以下のURLにアクセス  
   - API: http://localhost:8000/  
   - OpenAPI ドキュメント: http://localhost:8000/docs  
   - MCP エンドポイント: http://localhost:8000/mcp  

## サンプルコード

`example/` フォルダには動作確認用のサンプルプログラムが含まれています：

- `main.py` – FastAPI でホストされたサンプル API クライアント  
- `api_client_example.py` – ホスティングされた MCP API にアクセスするサンプルクライアント  
- `test_api_connection.py` – サンプルクライアントの接続テスト  

環境変数等の設定は不要で、ローカルのサーバーに対して動作を確認できます。

## テスト

このプロジェクトでは以下のテストを提供しています：

- 単体テスト（pytest）  
- 結合テスト（pytest）  
- E2E テスト（schemathesis）  
- MCP Inspector テスト（@modelcontextprotocol/inspector）

```bash
# 全テストを実行
poetry run pytest

# 単体テストのみ
poetry run pytest tests/unit

# 結合テストのみ
poetry run pytest tests/integration

# E2E テストのみ
poetry run pytest tests/e2e
