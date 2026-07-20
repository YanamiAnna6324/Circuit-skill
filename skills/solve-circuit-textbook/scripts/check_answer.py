#!/usr/bin/env python3
"""Check that a circuit solution contains every required answer section."""

import argparse
from pathlib import Path

REQUIRED = ("题意与约定", "教材依据", "解题思路", "计算过程", "结果自检",
            "知识点", "规律总结", "考试要点", "易错点", "快速自检")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("answer", type=Path)
    args = parser.parse_args()
    text = args.answer.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED if f"## {heading}" not in text]
    if missing:
        print("Missing sections: " + ", ".join(missing))
        return 1
    print("Answer structure: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
