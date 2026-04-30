"""Canonical deduplication: rotation, reflection, cyclic shift (layout code min)."""

from __future__ import annotations

import math
from typing import Iterable

from lillabo_calculator.layout_code import layout_code_from_vertices
from lillabo_calculator.solution import Solution


def _rot(x: float, y: float, k: int) -> tuple[float, float]:
    th = k * math.pi / 4
    c, s = math.cos(th), math.sin(th)
    return (c * x - s * y, s * x + c * y)


def _verts(sol: Solution) -> list[tuple[float, float]]:
    n = len(sol.tokens)
    return [(sol.states[i].x, sol.states[i].y) for i in range(n)]


def canonical_layout_code(sol: Solution) -> str:
    toks = list(sol.tokens)
    verts = _verts(sol)
    best: str | None = None
    for k in range(8):
        for flip in (False, True):
            pv: list[tuple[float, float]] = []
            for x, y in verts:
                xr, yr = _rot(x, y, k)
                if flip:
                    yr = -yr
                pv.append((xr, yr))
            tt = list(reversed(toks)) if flip else list(toks)
            cand = layout_code_from_vertices(pv, tt)
            if best is None or cand < best:
                best = cand
    assert best is not None
    return best


def unique_solutions(solutions: Iterable[Solution]) -> list[Solution]:
    seen: dict[str, Solution] = {}
    for sol in solutions:
        key = canonical_layout_code(sol)
        seen.setdefault(key, sol)
    return list(seen.values())
