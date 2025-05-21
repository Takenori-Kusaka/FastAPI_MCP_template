"""
APIエンドポイントの結合テスト
"""

import pytest
from fastapi.testclient import TestClient


class TestAPIIntegration:
    """
    APIエンドポイントの結合テスト
    """

    def test_root_endpoint(self, test_client: TestClient) -> None:
        """
        ルートエンドポイントのテスト
        """
        response = test_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "mcp" in data
        assert "hello" in data

    def test_hello_endpoint(self, test_client: TestClient) -> None:
        """
        Hello Worldエンドポイントのテスト
        """
        response = test_client.get("/hello")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Hello World" in data["message"]

    def test_api_documentation(self, test_client: TestClient) -> None:
        """
        APIドキュメントのテスト
        """
        # OpenAPI JSONのテスト
        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        openapi_schema = response.json()
        assert "openapi" in openapi_schema
        assert openapi_schema["openapi"] == "3.0.3"
        assert "paths" in openapi_schema
        assert "/api/examples/" in openapi_schema["paths"]
        assert "/api/examples/{example_id}" in openapi_schema["paths"]

        # Swagger UIのテスト
        response = test_client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # ReDocのテスト
        response = test_client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_example_api_flow(self, test_client: TestClient) -> None:
        """
        サンプルAPIの一連のフローをテスト
        """
        # 1. サンプル一覧を取得
        response = test_client.get("/api/examples/")
        assert response.status_code == 200
        examples = response.json()
        assert len(examples) > 0
        
        # 2. 最初のサンプルのIDを取得
        first_example_id = examples[0]["id"]
        
        # 3. 特定のサンプルを取得
        response = test_client.get(f"/api/examples/{first_example_id}")
        assert response.status_code == 200
        example = response.json()
        assert example["id"] == first_example_id
        assert example["name"] == examples[0]["name"]
        assert example["description"] == examples[0]["description"]
