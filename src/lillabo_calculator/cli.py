"""argparse entry point."""

from __future__ import annotations

import argparse
import sys

from lillabo_calculator.inventory import Inventory
from lillabo_calculator.runner import RunConfig, run


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lillabo", description="Enumerate closed LILLABO loops (PoC).")
    p.add_argument("--l1", type=int, default=0)
    p.add_argument("--l2", type=int, default=0)
    p.add_argument("--s1", type=int, default=0)
    p.add_argument("--b1", type=int, default=0)
    p.add_argument("--cw", type=int, default=0)
    p.add_argument("--ccw", type=int, default=0)
    p.add_argument("--max-solutions", type=int, default=100)
    p.add_argument("--max-nodes", type=int, default=5_000_000, help="Backtracking step budget (aborts search when exceeded).")
    p.add_argument("--bridge-unit", type=float, default=2.0)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        inv = Inventory(l1=args.l1, l2=args.l2, s1=args.s1, b1=args.b1, cw=args.cw, ccw=args.ccw)
        cfg = RunConfig(
            inventory=inv,
            max_solutions=max(1, args.max_solutions),
            bridge_unit=float(args.bridge_unit),
            max_nodes=max(1, args.max_nodes),
        )
        res = run(cfg)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(res.text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
