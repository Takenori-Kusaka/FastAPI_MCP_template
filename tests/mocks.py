"""
テスト用のモックモジュール
"""

from typing import Any, Dict, List, Optional, Union
from unittest.mock import Mock


class MockExampleService:
    """
    モックのサンプルサービス
    """

    def __init__(self, **kwargs) -> None:
        """
        初期化
        """
        pass

    def get_examples(self) -> List[Dict[str, Any]]:
        """
        サンプル一覧を取得

        Returns:
            サンプル一覧
        """
        return [
            {"id": 1, "name": "Example 1", "description": "This is example 1"},
            {"id": 2, "name": "Example 2", "description": "This is example 2"},
            {"id": 3, "name": "Example 3", "description": "This is example 3"},
        ]

    def get_example(self, example_id: int) -> Optional[Dict[str, Any]]:
        """
        サンプルを取得

        Args:
            example_id: サンプルID

        Returns:
            サンプル情報
        """
        examples = {
            1: {"id": 1, "name": "Example 1", "description": "This is example 1"},
            2: {"id": 2, "name": "Example 2", "description": "This is example 2"},
            3: {"id": 3, "name": "Example 3", "description": "This is example 3"},
        }
        return examples.get(example_id)

    def create_example(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        サンプルを作成

        Args:
            name: サンプル名
            description: 説明

        Returns:
            作成されたサンプル情報
        """
        return {
            "id": 4,
            "name": name,
            "description": description or f"This is {name}"
        }

    def update_example(self, example_id: int, name: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        サンプルを更新

        Args:
            example_id: サンプルID
            name: サンプル名
            description: 説明

        Returns:
            更新されたサンプル情報
        """
        example = self.get_example(example_id)
        if not example:
            return None
        
        updated = example.copy()
        if name is not None:
            updated["name"] = name
        if description is not None:
            updated["description"] = description
        
        return updated

    def delete_example(self, example_id: int) -> bool:
        """
        サンプルを削除

        Args:
            example_id: サンプルID

        Returns:
            削除に成功した場合はTrue
        """
        example = self.get_example(example_id)
        return example is not None


class MockCommentService:
    """
    モックのコメントサービス
    """

    def __init__(self) -> None:
        """
        初期化
        """
        self.comments = {}  # example_id をキーとしたコメントのリスト

    def add_comment(self, example_id: int, content: str) -> Dict[str, Any]:
        """
        サンプルにコメントを追加

        Args:
            example_id: サンプルID
            content: コメント内容

        Returns:
            追加されたコメント情報
        """
        if example_id not in self.comments:
            self.comments[example_id] = []
        
        comment_id = len(self.comments[example_id]) + 1
        comment = {
            "id": comment_id,
            "content": content,
            "example_id": example_id
        }
        
        self.comments[example_id].append(comment)
        return comment

    def get_comments(self, example_id: int) -> List[Dict[str, Any]]:
        """
        サンプルのコメント一覧を取得

        Args:
            example_id: サンプルID

        Returns:
            コメント一覧
        """
        return self.comments.get(example_id, [])
