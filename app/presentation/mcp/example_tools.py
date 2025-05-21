"""
サンプルMCPツール

注意: このファイルは参照用です。
FastAPI MCP 0.3.3では、FastAPIのエンドポイントを自動的にMCPツールとして登録するため、
このファイルで定義されたツールは使用されません。

実際のMCPツールは、app/presentation/api/example_router.pyで定義されたAPIエンドポイントから
自動的に生成されます。
"""

# サンプルデータ (app/presentation/api/example_router.pyと同じデータ)
EXAMPLES = [
    {"id": 1, "name": "Example 1", "description": "This is example 1"},
    {"id": 2, "name": "Example 2", "description": "This is example 2"},
    {"id": 3, "name": "Example 3", "description": "This is example 3"},
]

# 以下のコードは参照用です。実際には使用されません。
# FastAPI MCP 0.3.3では、MCPTool、MCPToolInput、MCPToolOutputクラスは提供されていません。
# 代わりに、FastAPIのエンドポイントを自動的にMCPツールとして登録します。

# get_examples_toolとget_example_toolは、app/main.pyで参照されていますが、
# 実際には使用されません。app/main.pyでは、これらのツールが存在するかどうかを
# 確認してから登録しようとしていますが、FastApiMCPクラスにはadd_toolメソッドが
# 存在しないため、この部分は実行されません。

# 以下は、FastAPI MCPの古いバージョンで使用されていたコードの例です。
# 現在のバージョンでは、このコードは機能しません。

"""
from typing import Dict, List, Optional
from pydantic import BaseModel

class GetExamplesInput(BaseModel):
    pass

class GetExamplesOutput(BaseModel):
    examples: List[Dict]

class GetExampleInput(BaseModel):
    example_id: int

class GetExampleOutput(BaseModel):
    example: Optional[Dict] = None
    error: Optional[str] = None

async def get_examples_tool(input: GetExamplesInput) -> GetExamplesOutput:
    return GetExamplesOutput(examples=EXAMPLES)

async def get_example_tool(input: GetExampleInput) -> GetExampleOutput:
    for example in EXAMPLES:
        if example["id"] == input.example_id:
            return GetExampleOutput(example=example)
    return GetExampleOutput(error=f"Example with ID {input.example_id} not found")
"""

# 以下は、app/main.pyでの参照用に空の関数を定義しています。
# これらの関数は実際には使用されませんが、app/main.pyでのインポートエラーを防ぐために定義しています。
get_examples_tool = None
get_example_tool = None
