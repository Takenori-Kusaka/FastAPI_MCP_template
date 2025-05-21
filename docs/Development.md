# 開発ガイド

このドキュメントでは、FastAPI MCP Templateの開発に関するガイドラインを提供します。

## 開発環境のセットアップ

### 必要条件

- Python 3.10以上
- Poetry（依存関係管理）
- Docker（オプション、コンテナ化に使用）
- Node.js（CDKデプロイに使用）

### 開発環境のセットアップ

1. リポジトリをクローン

```bash
git clone https://github.com/yourusername/fastapi-mcp-template.git
cd fastapi-mcp-template
```

2. Poetryを使用して依存関係をインストール

```bash
poetry install
```

3. 開発用の環境変数を設定

```bash
cp .env.example .env
# .envファイルを編集して必要な環境変数を設定
```

4. 開発サーバーを起動

```bash
poetry run python -m app.main
```

または

```bash
poetry run uvicorn app.main:app --reload
```

## コード規約

### Pythonコード規約

- [PEP 8](https://peps.python.org/pep-0008/)に従ってコードを書く
- [Black](https://black.readthedocs.io/en/stable/)を使用してコードをフォーマット
- [isort](https://pycqa.github.io/isort/)を使用してインポートを整理
- [mypy](https://mypy.readthedocs.io/en/stable/)を使用して型チェックを行う
- [flake8](https://flake8.pycqa.org/en/latest/)を使用して静的解析を行う

### コミットメッセージ規約

コミットメッセージは以下の形式に従ってください：

```
<type>(<scope>): <subject>

<body>

<footer>
```

- `<type>`: コミットの種類（feat, fix, docs, style, refactor, test, chore）
- `<scope>`: コミットの範囲（オプション）
- `<subject>`: コミットの概要
- `<body>`: コミットの詳細（オプション）
- `<footer>`: 関連するIssueやBreaking Changesなど（オプション）

例：

```
feat(api): サンプルAPIエンドポイントを追加

- GET /api/examples エンドポイントを追加
- GET /api/examples/{example_id} エンドポイントを追加

Closes #123
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

## 新しいAPIエンドポイントの追加

1. `app/presentation/api/`ディレクトリに新しいルーターファイルを作成

```python
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/your-endpoint",
    tags=["your-tag"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_items():
    """
    アイテム一覧を取得するエンドポイント
    """
    return [{"id": 1, "name": "Item 1"}]

@router.get("/{item_id}")
async def get_item(item_id: int):
    """
    特定のアイテムを取得するエンドポイント
    """
    return {"id": item_id, "name": f"Item {item_id}"}
```

2. `app/main.py`ファイルに新しいルーターを登録

```python
from app.presentation.api.your_router import router as your_router

# APIルーターの登録
app.include_router(your_router)
```

## 新しいMCPツールの追加

FastAPI MCP 0.3.3では、FastAPIのエンドポイントを自動的にMCPツールとして登録します。そのため、新しいAPIエンドポイントを追加するだけで、自動的にMCPツールとして登録されます。

## テスト

### 単体テスト

単体テストは`tests/unit/`ディレクトリに配置します。

```python
def test_your_function():
    """
    あなたの関数のテスト
    """
    result = your_function()
    assert result == expected_result
```

### 結合テスト

結合テストは`tests/integration/`ディレクトリに配置します。

```python
def test_your_api(test_client):
    """
    あなたのAPIのテスト
    """
    response = test_client.get("/api/your-endpoint/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
```

### E2Eテスト

E2Eテストは`tests/e2e/`ディレクトリに配置します。

```python
def test_your_api_e2e(base_url):
    """
    あなたのAPIのE2Eテスト
    """
    response = requests.get(f"{base_url}/api/your-endpoint/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
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

## CI/CD

このプロジェクトはGitHub Actionsを使用してCI/CDを実装しています。

### CI/CDパイプライン

- プルリクエストが作成されたときに自動的にテストを実行
- mainブランチにマージされたときに自動的にデプロイを実行

### GitHub Actionsの設定

`.github/workflows/`ディレクトリにGitHub Actionsの設定ファイルを配置しています。

## トラブルシューティング

### よくある問題と解決策

1. **依存関係のインストールに失敗する**

```bash
# Poetryのキャッシュをクリア
poetry cache clear --all pypi

# 依存関係を再インストール
poetry install
```

2. **開発サーバーの起動に失敗する**

```bash
# ポートが使用中かどうかを確認
lsof -i :8000

# 別のポートを使用して起動
poetry run uvicorn app.main:app --port 8001 --reload
```

3. **テストの実行に失敗する**

```bash
# テストのデバッグモードを有効にして実行
poetry run pytest -vv --pdb
```

## 参考リンク

- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/ja/)
- [FastMCP公式ドキュメント](https://fastapi-mcp.tadata.com/getting-started/welcome)
- [Poetry公式ドキュメント](https://python-poetry.org/docs/)
- [AWS CDK公式ドキュメント](https://docs.aws.amazon.com/cdk/latest/guide/home.html)
