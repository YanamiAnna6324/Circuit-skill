#!/usr/bin/env python3
"""Compare expected and actual scalar values with explicit unit conversion."""

from __future__ import annotations

import argparse
import math

PREFIX = {"": 1.0, "p": 1e-12, "n": 1e-9, "u": 1e-6, "m": 1e-3,
          "k": 1e3, "M": 1e6, "G": 1e9}


def scale(unit: str) -> tuple[float, str]:
    unit = unit.strip().replace("μ", "u").replace("Ω", "Ohm")
    for base in ("Ohm", "Hz", "F", "H", "W", "V", "A", "s"):
        if unit == base:
            return 1.0, base
        if unit.endswith(base) and unit[:-len(base)] in PREFIX:
            prefix = unit[:-len(base)]
            return PREFIX[prefix], base
    raise ValueError(f"Unsupported unit: {unit}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected", type=float, required=True)
    parser.add_argument("--expected-unit", required=True)
    parser.add_argument("--actual", type=float, required=True)
    parser.add_argument("--actual-unit", required=True)
    parser.add_argument("--rel-tol", type=float, default=1e-6)
    parser.add_argument("--abs-tol", type=float, default=0.0)
    args = parser.parse_args()
    try:
        expected_scale, expected_base = scale(args.expected_unit)
        actual_scale, actual_base = scale(args.actual_unit)
    except ValueError as exc:
        parser.error(str(exc))
    if expected_base != actual_base:
        parser.error(f"Incompatible units: {expected_base} and {actual_base}")
    expected = args.expected * expected_scale
    actual = args.actual * actual_scale
    difference = actual - expected
    passed = math.isclose(actual, expected, rel_tol=args.rel_tol, abs_tol=args.abs_tol)
    print(f"expected={expected:g} {expected_base}")
    print(f"actual={actual:g} {actual_base}")
    print(f"difference={difference:g} {expected_base}")
    print("comparison=" + ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
