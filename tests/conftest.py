"""
pytest用の共通フィクスチャ
"""

import os
import signal
import socket
import subprocess
import time
from typing import Dict, Generator, List, Optional, Union
from unittest.mock import Mock

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.main import app

# .envファイルを読み込む
load_dotenv()


@pytest.fixture
def test_client() -> TestClient:
    """
    FastAPIのテストクライアント

    Returns:
        TestClient: FastAPIのテストクライアント
    """
    return TestClient(app)


@pytest.fixture(scope="session")
def mcp_server_url() -> str:
    """
    テスト用のMCPサーバーURLを返すフィクスチャ
    
    環境変数 TEST_SERVER_URL でサーバーのURLを指定できます（デフォルト: http://localhost:8001）

    Returns:
        str: MCPサーバーのURL
    """
    # サーバーのURLを取得
    server_url = os.getenv("TEST_SERVER_URL", "http://localhost:8001")
    print(f"テスト用サーバーURL: {server_url}")
    return server_url


@pytest.fixture(scope="session")
def env_vars() -> Dict[str, Optional[str]]:
    """
    環境変数を読み込むフィクスチャ

    Returns:
        Dict[str, Optional[str]]: 環境変数の辞書
    """
    return {
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
        "read_only_mode": os.getenv("READ_ONLY_MODE"),
    }
