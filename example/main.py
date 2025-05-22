"""
FastAPI MCP サンプルアプリケーション

このサンプルアプリケーションは、FastAPI MCPテンプレートを使用して
シンプルなAPIを実装する方法を示します。
"""
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

app = FastAPI(
    title="FastAPI MCP サンプルアプリケーション",
    description="FastAPI MCPテンプレートを使用したシンプルなAPIサンプル",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# サンプルデータ
EXAMPLES = [
    {"id": 1, "name": "Example 1", "description": "This is example 1"},
    {"id": 2, "name": "Example 2", "description": "This is example 2"},
    {"id": 3, "name": "Example 3", "description": "This is example 3"},
]

# モデル定義
class ExampleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class CommentCreate(BaseModel):
    content: str

# ルート定義
@app.get("/")
def read_root():
    return {
        "message": "FastAPI MCP サンプルアプリケーション",
        "endpoints": [
            {"path": "/api/examples", "description": "サンプル一覧を取得"},
            {"path": "/api/examples/{example_id}", "description": "サンプル詳細を取得"},
            {"path": "/api/examples", "method": "POST", "description": "サンプルを作成"},
            {"path": "/api/examples/{example_id}", "method": "PUT", "description": "サンプルを更新"},
            {"path": "/api/examples/{example_id}", "method": "DELETE", "description": "サンプルを削除"},
            {"path": "/api/examples/{example_id}/comments", "method": "POST", "description": "コメントを追加"},
            {"path": "/api/examples/{example_id}/comments", "description": "コメント一覧を取得"},
        ]
    }

# サンプルデータ関連のエンドポイント
@app.get("/api/examples")
def get_examples():
    """サンプル一覧を取得"""
    return EXAMPLES

@app.get("/api/examples/{example_id}")
def get_example(example_id: int):
    """サンプル詳細を取得"""
    for example in EXAMPLES:
        if example["id"] == example_id:
            return example
    raise HTTPException(status_code=404, detail=f"サンプルID {example_id} が見つかりません")

@app.post("/api/examples", status_code=201)
def create_example(example: ExampleCreate):
    """サンプルを作成"""
    # 新しいIDを生成（実際のアプリケーションではデータベースで自動生成される）
    new_id = max([example["id"] for example in EXAMPLES]) + 1 if EXAMPLES else 1
    
    new_example = {
        "id": new_id,
        "name": example.name,
        "description": example.description or f"This is example {new_id}"
    }
    
    # サンプルデータに追加（実際のアプリケーションではデータベースに保存）
    EXAMPLES.append(new_example)
    
    return new_example

@app.put("/api/examples/{example_id}")
def update_example(example_id: int, example: ExampleUpdate):
    """サンプルを更新"""
    for i, existing_example in enumerate(EXAMPLES):
        if existing_example["id"] == example_id:
            # 更新するフィールドのみ変更
            if example.name is not None:
                EXAMPLES[i]["name"] = example.name
            if example.description is not None:
                EXAMPLES[i]["description"] = example.description
            return EXAMPLES[i]
    
    raise HTTPException(status_code=404, detail=f"サンプルID {example_id} が見つかりません")

@app.delete("/api/examples/{example_id}")
def delete_example(example_id: int):
    """サンプルを削除"""
    for i, example in enumerate(EXAMPLES):
        if example["id"] == example_id:
            # サンプルデータから削除（実際のアプリケーションではデータベースから削除）
            deleted = EXAMPLES.pop(i)
            return {"message": f"サンプルID {example_id} を削除しました", "deleted": deleted}
    
    raise HTTPException(status_code=404, detail=f"サンプルID {example_id} が見つかりません")

# コメント関連のエンドポイント（インメモリで実装）
COMMENTS = {}  # example_id をキーとしたコメントのリスト

@app.post("/api/examples/{example_id}/comments", status_code=201)
def add_comment(example_id: int, comment: CommentCreate):
    """サンプルにコメントを追加"""
    # サンプルが存在するか確認
    example_exists = False
    for example in EXAMPLES:
        if example["id"] == example_id:
            example_exists = True
            break
    
    if not example_exists:
        raise HTTPException(status_code=404, detail=f"サンプルID {example_id} が見つかりません")
    
    # コメントを追加
    if example_id not in COMMENTS:
        COMMENTS[example_id] = []
    
    comment_id = len(COMMENTS[example_id]) + 1
    timestamp = datetime.now().isoformat()
    
    new_comment = {
        "id": comment_id,
        "content": comment.content,
        "created_at": timestamp
    }
    
    COMMENTS[example_id].append(new_comment)
    
    return new_comment

@app.get("/api/examples/{example_id}/comments")
def get_comments(example_id: int):
    """サンプルのコメント一覧を取得"""
    # サンプルが存在するか確認
    example_exists = False
    for example in EXAMPLES:
        if example["id"] == example_id:
            example_exists = True
            break
    
    if not example_exists:
        raise HTTPException(status_code=404, detail=f"サンプルID {example_id} が見つかりません")
    
    # コメントを取得
    return COMMENTS.get(example_id, [])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
