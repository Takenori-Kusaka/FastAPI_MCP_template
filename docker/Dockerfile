# ビルドステージ - 依存関係のインストールのみを行う
FROM python:3.12-slim AS builder

WORKDIR /build

# 必要な依存関係のみをインストール
RUN pip install --no-cache-dir --target=/build/deps \
    fastapi==0.115.12 \
    uvicorn[standard]==0.34.2 \
    pydantic==2.11.3 \
    httpx==0.28.1 \
    python-dotenv==1.1.0 \
    fastapi-mcp==0.3.3 \
    mangum==0.19.0 \
    requests

# uvicornをグローバルにインストール（コマンドラインから実行できるように）
RUN pip install --no-cache-dir uvicorn[standard]==0.34.2

# 実行環境ステージ - 必要最小限のイメージを作成
FROM python:3.12-slim AS runtime

WORKDIR /app

# ヘルスチェック用のcurlとuvicornをインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir uvicorn[standard]==0.34.2

# ビルドステージから依存関係をコピー
COPY --from=builder /build/deps /usr/local/lib/python3.12/site-packages/

# アプリケーションコードのみをコピー
COPY app/ ./app/

# 環境変数の設定
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# ポートの公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# uvicornを使用してサーバーを起動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
