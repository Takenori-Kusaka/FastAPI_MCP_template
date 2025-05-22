# FastAPI_MCP_Template CDKデプロイガイド

このガイドでは、AWS CDKを使用したFastAPI_MCP_Templateのデプロイ手法を説明します。Dry Runの実行方法、実際のデプロイ方法、ログ確認、トラブルシューティングを解説します。

## 前提条件

- AWS CLIがインストールされていること  
- AWS CDKがインストールされていること  
- Node.jsがインストールされていること  
- Python (3.x)がインストールされていること  
- AWSアカウントおよび適切な権限  

## 環境変数の設定

デプロイに必要な環境変数を `.env` ファイルに設定します:

```bash
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_SESSION_TOKEN=your_session_token  # 必要な場合
AWS_DEFAULT_REGION=your_region
```

## CDKのDry Run

プロジェクトルートで以下のコマンドを実行します:

```bash
./scripts/dry-run-cdk.sh
```

このスクリプトは以下を実行します:
1. `.env` 読み込みとAWS認証確認  
2. CDK環境変数設定  
3. CDKビルド (`cdk` ディレクトリ内で `npm run build`)  
4. `cdk.out` ディレクトリのクリーンアップ  
5. `npx cdk synth` および Dry Run  

ログは `logs/cdk_dry_run_YYYYMMDD_HHMMSS.log` に出力されます。

## CDKのデプロイ

プロジェクトルートで以下のコマンドを実行します:

```bash
./scripts/deploy-cdk.sh
```

このスクリプトは以下を実行します:
1. `.env` 読み込みとAWS認証確認  
2. CDKビルド  
3. `npx cdk deploy --all` によるデプロイ  

ログは `logs/cdk_deploy_YYYYMMDD_HHMMSS.log` に出力されます。

## ログの確認

- Dry Runログ: `logs/cdk_dry_run_*.log`  
- デプロイログ: `logs/cdk_deploy_*.log`  

```bash
grep "Error" logs/cdk_*.log
grep -A 10 "Stack ARN" logs/cdk_*.log
```

## トラブルシューティング

### AWS認証エラー

- `The security token included in the request is invalid` など  
- `aws configure list` および `.env` の設定を確認

### CDKブートストラップエラー

```bash
cd cdk && npx cdk bootstrap
```

### 依存関係エラー

```bash
cd cdk && npm install
```

### ファイルパス長エラー

- `ENAMETOOLONG` エラーが発生した場合:

```bash
rm -rf cdk/cdk.out
```

### その他

- AWS CloudFormationコンソールでスタックイベントを確認

## 参考

- AWS CDK公式ドキュメント: https://docs.aws.amazon.com/cdk/latest/guide/home.html
