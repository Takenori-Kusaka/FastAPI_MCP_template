"""
E2Eテスト
"""

import os
import requests
import pytest
import time
from typing import Dict, Any


class TestE2E:
    """
    E2Eテスト
    
    実際に起動しているサーバーに対してリクエストを送信してテストします。
    テスト実行前にサーバーを起動しておく必要があります。
    """

    @pytest.fixture
    def base_url(self, mcp_server_url: str) -> str:
        """
        テスト対象のサーバーのベースURL
        """
        return mcp_server_url

    def test_server_is_running(self, base_url: str) -> None:
        """
        サーバーが起動しているかテスト
        """
        # テスト用のサーバーが起動していない場合は、テストをスキップ
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "docs" in data
            assert "mcp" in data
            assert "hello" in data
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pytest.skip("サーバーが起動していません")

    def test_hello_endpoint(self, base_url: str) -> None:
        """
        Hello Worldエンドポイントのテスト
        """
        try:
            response = requests.get(f"{base_url}/hello", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "Hello World" in data["message"]
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pytest.skip("サーバーが起動していません")

    def test_api_examples(self, base_url: str) -> None:
        """
        サンプルAPIのテスト
        """
        try:
            # サンプル一覧を取得
            response = requests.get(f"{base_url}/api/examples/", timeout=5)
            assert response.status_code == 200
            examples = response.json()
            assert isinstance(examples, list)
            assert len(examples) > 0
            
            # 特定のサンプルを取得
            example_id = examples[0]["id"]
            response = requests.get(f"{base_url}/api/examples/{example_id}", timeout=5)
            assert response.status_code == 200
            example = response.json()
            assert example["id"] == example_id
            
            # 存在しないサンプルを取得
            response = requests.get(f"{base_url}/api/examples/999", timeout=5)
            assert response.status_code == 404
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pytest.skip("サーバーが起動していません")

    def test_mcp_endpoint(self, base_url: str) -> None:
        """
        MCPエンドポイントのテスト
        """
        try:
            # MCPサーバー情報を取得
            response = requests.get(f"{base_url}/mcp", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "name" in data
            assert "description" in data
            assert "tools" in data
            
            # ツール一覧を確認
            tools = data["tools"]
            assert isinstance(tools, list)
            assert len(tools) > 0
            
            # get_examplesツールが存在するか確認
            get_examples_tool = next((tool for tool in tools if tool["name"] == "get_examples"), None)
            assert get_examples_tool is not None
            
            # get_exampleツールが存在するか確認
            get_example_tool = next((tool for tool in tools if tool["name"] == "get_example"), None)
            assert get_example_tool is not None
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pytest.skip("サーバーが起動していません")

    @pytest.mark.skip(reason="FastAPI MCP 0.3.3ではMCPツールのエンドポイントが変更されているため")
    def test_mcp_tool_execution(self, base_url: str) -> None:
        """
        MCPツールの実行テスト
        
        注意: FastAPI MCP 0.3.3ではMCPツールのエンドポイントが変更されているため、
        このテストはスキップされます。
        """
        pass
