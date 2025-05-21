#!/usr/bin/env python
"""
テスト実行スクリプト
"""

import argparse
import os
import subprocess
import sys
from typing import List, Optional


def main() -> int:
    """
    テスト実行スクリプトのメインエントリーポイント

    Returns:
        int: 終了コード（0: 成功、1: 失敗）
    """
    parser = argparse.ArgumentParser(description="テスト実行スクリプト")
    parser.add_argument(
        "--unit", action="store_true", help="ユニットテストのみ実行"
    )
    parser.add_argument(
        "--integration", action="store_true", help="結合テストのみ実行"
    )
    parser.add_argument(
        "--e2e", action="store_true", help="E2Eテストのみ実行"
    )
    parser.add_argument(
        "--all", action="store_true", help="すべてのテストを実行"
    )
    parser.add_argument(
        "--coverage", action="store_true", help="カバレッジレポートを生成"
    )
    parser.add_argument(
        "--html", action="store_true", help="HTMLカバレッジレポートを生成"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="詳細なログを出力"
    )
    parser.add_argument(
        "pytest_args", nargs="*", help="pytestに渡す追加の引数"
    )

    args = parser.parse_args()

    # デフォルトですべてのテストを実行
    if not (args.unit or args.integration or args.e2e or args.all):
        args.all = True

    pytest_args: List[str] = []

    # テストの種類に応じた引数を追加
    if args.all:
        pytest_args.append("tests")
    else:
        if args.unit:
            pytest_args.append("tests/unit")
        if args.integration:
            pytest_args.append("tests/integration")
        if args.e2e:
            pytest_args.append("tests/e2e")

    # カバレッジレポートの設定
    if args.coverage:
        pytest_args.append("--cov=app")
        if args.html:
            pytest_args.append("--cov-report=html")
        else:
            pytest_args.append("--cov-report=term")

    # 詳細なログ出力
    if args.verbose:
        pytest_args.append("-v")

    # 追加の引数
    pytest_args.extend(args.pytest_args)

    # コマンドの表示
    print(f"実行コマンド: pytest {' '.join(pytest_args)}")

    # pytestの実行
    result = subprocess.run(["pytest"] + pytest_args)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
