"""
FastAPI MCP Template - メインアプリケーション
"""

import os

try:
    from dotenv import load_dotenv
    # 環境変数の読み込み
    load_dotenv()
    print("[DEBUG] .env ファイルを読み込みました")
except ImportError:
    print("[DEBUG] python-dotenv がインストールされていないため、.env ファイルを読み込めません")
    # Lambda環境では.envファイルは使用しないので、エラーを無視する

from fastapi import FastAPI, Request, HTTPException, Response
from typing import Callable
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN
from fastapi_mcp import FastApiMCP  # type: ignore

from app.core.config import settings
from mangum import Mangum

# ルーターとMCPツールのインポート
from app.presentation.api.example_router import router as example_router
from app.presentation.mcp.example_tools import get_examples_tool, get_example_tool

# FastAPIアプリケーションの作成
app = FastAPI(
    title="FastAPI MCP Template",
    description="FastAPIとModel Context Protocol (MCP)を使用したAPIテンプレート",
    version="0.1.0",
    openapi_version="3.0.3",
)
from fastapi.openapi.utils import get_openapi

def custom_openapi_schema():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"  # OpenAPIのバージョンを3.0.3に設定
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi_schema

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read-only mode middleware
@app.middleware("http")
async def read_only_middleware(request: Request, call_next: Callable) -> Response:
    if settings.READ_ONLY_MODE and request.method in ("POST", "PUT", "DELETE", "PATCH"):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Application is in read-only mode. Write operations are disabled.",
        )
    response: Response = await call_next(request)
    return response

# APIルーターの登録
app.include_router(example_router)

# MCPサーバーの作成
print("[DEBUG] MCPサーバー作成開始")
mcp_server = FastApiMCP(
    fastapi=app,
    name="FastAPI-MCP-Template",
    description="FastAPIとModel Context Protocol (MCP)を使用したAPIテンプレート",
)
print("[DEBUG] MCPサーバー作成完了")

# MCPサーバーの設定
# FastApiMCP 0.3.3では、FastAPIのエンドポイントを自動的にMCPツールとして登録するため、
# カスタムツールのインポートは不要ですが、明示的に登録することもできます。
print("[DEBUG] MCPサーバー設定開始")

# MCPサーバーの設定を更新
mcp_server.setup_server()

# カスタムMCPツールを明示的に登録
if hasattr(mcp_server, "add_tool") and callable(mcp_server.add_tool):
    mcp_server.add_tool(get_examples_tool)
    mcp_server.add_tool(get_example_tool)
    print(f"[DEBUG] 明示的にツールを登録: get_examples_tool, get_example_tool")


print("[DEBUG] MCPサーバー設定完了")

# 登録されたツールの一覧を表示
print("[DEBUG] 登録されたMCPツール一覧:")
try:
    # FastApiMCP 0.3.3では、toolsプロパティを使用してツール一覧を取得
    if hasattr(mcp_server, "tools"):
        for tool in mcp_server.tools:
            print(f"[DEBUG] - ツール名: {tool.name}")
    else:
        print("[DEBUG] - ツール一覧を取得できません")
except Exception as e:
    print(f"[DEBUG] - ツール一覧取得エラー: {str(e)}")

# MCPサーバーをマウント
print("[DEBUG] MCPサーバーマウント開始")
mcp_server.mount(mount_path="/mcp")
print("[DEBUG] MCPサーバーマウント完了")


# グローバル例外ハンドラー
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    グローバル例外ハンドラー

    Args:
        request: リクエスト
        exc: 例外

    Returns:
        JSONResponse: エラーレスポンス
    """
    import traceback
    error_traceback = traceback.format_exc()
    print(f"[ERROR] 例外が発生しました: {str(exc)}")
    print(f"[ERROR] トレースバック: {error_traceback}")
    print(f"[ERROR] リクエストパス: {request.url.path}")
    print(f"[ERROR] リクエストメソッド: {request.method}")
    print(f"[ERROR] リクエストヘッダー: {request.headers}")
    
    try:
        body = await request.body()
        print(f"[ERROR] リクエストボディ: {body.decode('utf-8')}")
    except Exception as e:
        print(f"[ERROR] リクエストボディの取得に失敗しました: {str(e)}")
    
    import datetime
    return JSONResponse(
        status_code=500, 
        content={
            "error": "Internal Server Error", 
            "message": str(exc),
            "path": request.url.path,
            "method": request.method,
            "timestamp": str(datetime.datetime.now())
        }
    )


# Hello Worldエンドポイント
@app.get("/hello")
async def hello_world() -> dict:
    """
    Hello Worldエンドポイント

    Returns:
        dict: Hello Worldメッセージ
    """
    return {"message": "Hello World from FastAPI MCP Template!"}

# ルートエンドポイント
@app.get("/")
async def root() -> dict:
    """
    ルートエンドポイント

    Returns:
        dict: ウェルカムメッセージ
    """
    return {"message": "Welcome to FastAPI MCP Template", "docs": "/docs", "mcp": "/mcp", "hello": "/hello"}


# AWS Lambda用ハンドラー
handler = Mangum(app)


# 開発サーバー起動用関数
def start() -> None:
    """
    開発サーバーを起動
    """
    import uvicorn

    # 開発環境では0.0.0.0を使用し、本番環境では特定のインターフェースを使用する
    # セキュリティ上の理由から、デフォルトではlocalhostを使用
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run(
        "app.main:app", host=host, port=int(os.getenv("PORT", "8000")), reload=True
    )


# スクリプトとして実行された場合
if __name__ == "__main__":
    start()
