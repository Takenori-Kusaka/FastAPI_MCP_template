"""
サンプルAPIエンドポイント
"""

from typing import Dict, List

from fastapi import APIRouter, HTTPException

# ルーターの作成
router = APIRouter(
    prefix="/api/examples",
    tags=["examples"],
    responses={404: {"description": "Not found"}},
)

# サンプルデータ
EXAMPLES = [
    {"id": 1, "name": "Example 1", "description": "This is example 1"},
    {"id": 2, "name": "Example 2", "description": "This is example 2"},
    {"id": 3, "name": "Example 3", "description": "This is example 3"},
]


@router.get("/", response_model=List[Dict], operation_id="get_examples")
async def get_examples() -> List[Dict]:
    """
    サンプル一覧を取得するエンドポイント

    Returns:
        サンプル一覧
    """
    return EXAMPLES


@router.get("/{example_id}", response_model=Dict, operation_id="get_example")
async def get_example(example_id: int) -> Dict:
    """
    サンプル情報を取得するエンドポイント

    Args:
        example_id: サンプルID

    Returns:
        サンプル情報
    """
    for example in EXAMPLES:
        if example["id"] == example_id:
            return example
    raise HTTPException(status_code=404, detail=f"Example with ID {example_id} not found")
