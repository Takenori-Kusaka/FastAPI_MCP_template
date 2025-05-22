# FastAPI MCP Template

FastAPIとModel Context Protocol (MCP)を使用してAPIをホスティングするためのテンプレートリポジトリです。

## 概要

このプロジェクトは以下の技術を使用しています：

- [FastAPI](https://fastapi.tiangolo.com/ja/): 高性能なPythonウェブフレームワーク
- [FastMCP](https://fastapi-mcp.tadata.com/getting-started/welcome): FastAPIとModel Context Protocol (MCP)を統合するライブラリ
- [OpenAPI 3.0.3](https://swagger.io/specification/): APIドキュメントの自動生成

## 機能

- FastAPIを使用したAPIホスティング
- FastMCPを使用したMCPサーバーホスティング
- OpenAPI 3.0.3に準拠したAPIドキュメントの自動生成
- サンプルAPIエンドポイントの実装
- サンプルMCPツールの実装

## 開発環境

### 必要条件

- Python 3.10以上
- Poetry（依存関係管理）
- Docker（オプション、コンテナ化に使用）

### セットアップ

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/fastapi-mcp-template.git
cd fastapi-mcp-template
```

2. Poetryを使用して依存関係をインストール

```bash
poetry install
```

3. 開発サーバーを起動

```bash
poetry run python -m app.main
```

または

```bash
poetry run uvicorn app.main:app --reload
```

4. ブラウザで以下のURLにアクセス

- API: http://localhost:8000/
- APIドキュメント: http://localhost:8000/docs
- MCPサーバー: http://localhost:8000/mcp

## テスト

### テスト環境

このプロジェクトでは以下のテスト環境を提供しています：

1. pytestによる単体テスト
2. pytest-covによるカバレッジ計測
3. flake8による静的解析
4. pytestによる結合テスト
5. schemathesisによるE2Eテスト
6. MCP InspectorによるMCPサーバーのテスト
7. actによるGitHub Actionsのローカル実行

### テストの実行

```bash
# すべてのテストを実行
poetry run pytest

# 単体テストのみ実行
poetry run pytest tests/unit

# 結合テストのみ実行
poetry run pytest tests/integration

# E2Eテストのみ実行
poetry run pytest tests/e2e

# カバレッジレポートを生成
poetry run pytest --cov=app --cov-report=html
```

## デプロイ

### Dockerを使用したデプロイ

```bash
# Dockerイメージをビルド
docker build -t fastapi-mcp-template -f docker/Dockerfile .

# Dockerコンテナを実行
docker run -p 8000:8000 fastapi-mcp-template
```

### AWS CDKを使用したデプロイ

```bash
# CDKディレクトリに移動
cd cdk

# 依存関係をインストール
npm install

# CDKをデプロイ
npm run cdk deploy
```

## プロジェクト構造

```
fastapi-mcp-template/
├── app/                      # アプリケーションコード
│   ├── __init__.py
│   ├── main.py               # アプリケーションのエントリーポイント
│   ├── core/                 # コア機能
│   │   └── config.py         # 設定
│   ├── presentation/         # プレゼンテーション層
│   │   ├── api/              # APIエンドポイント
│   │   │   └── example_router.py
│   │   └── mcp/              # MCPツール
│   │       └── example_tools.py
├── cdk/                      # AWS CDKコード
├── docker/                   # Dockerファイル
├── docs/                     # ドキュメント
├── scripts/                  # スクリプト
├── tests/                    # テスト
│   ├── unit/                 # 単体テスト
│   ├── integration/          # 結合テスト
│   └── e2e/                  # E2Eテスト
├── pyproject.toml            # Poetryの設定
└── README.md                 # このファイル
```

## ライセンス

MITライセンス
