#!/usr/bin/env python3
"""Validate the required structure and verdict of a circuit diagnosis report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = (
    "诊断范围", "教材与正确基线", "候选答案复现", "根因假设", "第一个实质错误",
    "错误传播", "修正解答", "独立复验", "最终判定", "知识点", "规律总结",
    "考试要点", "易错点", "快速自检",
)
VERDICTS = {"通过", "修正后通过", "无法判定"}


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def read_stdin() -> str:
    data = sys.stdin.buffer.read()
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16")
    if data.startswith(b"\xef\xbb\xbf"):
        return data.decode("utf-8-sig")
    if data.count(b"\x00") > len(data) // 4:
        return data.decode("utf-16-le")
    return data.decode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", help="UTF-8 Markdown report path, or - to read standard input")
    args = parser.parse_args()
    text = read_stdin() if args.report == "-" else Path(args.report).read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED if not section(text, heading)]
    errors: list[str] = []
    if missing:
        errors.append("Missing or empty sections: " + ", ".join(missing))
    verdict_text = section(text, "最终判定")
    verdict_line = verdict_text.splitlines()[0].strip().strip("`*_ ") if verdict_text else ""
    if verdict_line not in VERDICTS:
        errors.append("The first final-verdict line must be exactly one of: " + ", ".join(sorted(VERDICTS)))
    if len(section(text, "独立复验")) < 20:
        errors.append("Independent verification is too short to show an actual check")
    if errors:
        print("\n".join(errors))
        return 1
    print("Diagnosis structure: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
