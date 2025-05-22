# E2Eテストガイド

> ドキュメントファイル: [`tests/TEST_STRATEGY.md`](tests/TEST_STRATEGY.md:1)

## 1. ローカルE2Eテスト

### 1.1 Uvicornによるホスティング (CLI)

#### 1.1.0 CLIでUvicornを起動する

```bash
uvicorn [`app.main:app`](app/main.py:1) --reload
```

#### 1.1.1 OpenAPI仕様書を出力する

```bash
curl http://127.0.0.1:8000/docs/openapi.yaml -o [`openapi.yaml`](docs/openapi.yaml:1)
```

#### 1.1.2 Schemathesisテスト

```bash
schemathesis run openapi.yaml --checks all
```

#### 1.1.3 MCP Inspectorテスト

スクリプト: [`scripts/run_inspector_test_suite.sh`](scripts/run_inspector_test_suite.sh:1)

```bash
./scripts/run_inspector_test_suite.sh
```

### 1.2 Docker Composeによるホスティング

#### 1.2.0 Dockerイメージを再ビルドし起動

```bash
docker-compose up --build
```

#### 1.2.1 OpenAPI仕様書を出力する

```bash
curl http://127.0.0.1:8000/docs/openapi.yaml -o [`openapi.yaml`](docs/openapi.yaml:1)
```

#### 1.2.2 Schemathesisテスト

```bash
schemathesis run openapi.yaml --checks all
```

#### 1.2.3 MCP Inspectorテスト

スクリプト: [`scripts/run_inspector_test_suite.sh`](scripts/run_inspector_test_suite.sh:1)

```bash
./scripts/run_inspector_test_suite.sh
```

## 2. リモートE2Eテスト

### 2.1 AWS CDKホスティング

#### 2.1.0 CDKデプロイ

```bash
cdk deploy
```

– または GitHub Actions による自動デプロイ

#### 2.1.1 APIキー発行とエンドポイント取得

AWS マネジメントコンソールまたは CDK 出力から API キーを発行し、エンドポイント URL を控えます。

#### 2.1.2 Schemathesisテスト

```bash
schemathesis run https://<your-endpoint>/openapi.yaml --checks all --auth <API_KEY>
```

#### 2.1.3 MCP Inspectorテスト

スクリプト: [`scripts/run_inspector_test_suite.sh`](scripts/run_inspector_test_suite.sh:1)

```bash
./scripts/run_inspector_test_suite.sh --endpoint https://<your-endpoint> --api-key <API_KEY>
