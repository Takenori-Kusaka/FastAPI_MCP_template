"""
サンプルAPIエンドポイントのユニットテスト
"""

from fastapi.testclient import TestClient


def test_get_examples(test_client: TestClient) -> None:
    """
    サンプル一覧取得エンドポイントのテスト
    """
    response = test_client.get("/api/examples/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "description" in data[0]


def test_get_example(test_client: TestClient) -> None:
    """
    サンプル取得エンドポイントのテスト
    """
    # 存在するIDでテスト
    response = test_client.get("/api/examples/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "description" in data

    # 存在しないIDでテスト
    response = test_client.get("/api/examples/999")
    assert response.status_code == 404
    assert "detail" in response.json()
