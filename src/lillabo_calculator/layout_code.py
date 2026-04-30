"""Layout code: CW from above, start at lexicographically smallest corner."""

from __future__ import annotations

from typing import Sequence

from lillabo_calculator.inventory import PieceToken
from lillabo_calculator.solution import Solution

ROUND = 6


def _vertex_key(p: tuple[float, float]) -> tuple[float, float]:
    return (round(p[0], ROUND), round(p[1], ROUND))


def _signed_area(pts: Sequence[tuple[float, float]]) -> float:
    n = len(pts)
    s = 0.0
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return 0.5 * s


def layout_code_from_vertices(
    verts: Sequence[tuple[float, float]],
    tokens: Sequence[PieceToken],
) -> str:
    """ verts[i] -> verts[i+1] uses tokens[i]; verts[n] should equal verts[0] implicitly (len n cycle). """
    n = len(tokens)
    if len(verts) != n:
        msg = "verts and tokens length mismatch"
        raise ValueError(msg)
    if n == 0:
        return ""
    area = _signed_area(verts)
    toks = list(tokens)
    if area > 0:
        cw_seq = [toks[(n - 1 - j) % n] for j in range(n)]
    elif area < 0:
        cw_seq = list(toks)
    else:
        cw_seq = list(toks)
    keys = [_vertex_key(verts[i]) for i in range(n)]
    k = min(range(n), key=lambda i: keys[i])
    if area > 0:
        start_idx = (n - k) % n
        rotated = [cw_seq[(start_idx + j) % n] for j in range(n)]
    else:
        rotated = [cw_seq[(k + j) % n] for j in range(n)]
    return " ".join(t.name for t in rotated)


def layout_code(solution: Solution) -> str:
    n = len(solution.tokens)
    verts = [(solution.states[i].x, solution.states[i].y) for i in range(n)]
    return layout_code_from_vertices(verts, solution.tokens)


def token_names(tokens: Sequence[PieceToken]) -> str:
    return " ".join(t.name for t in tokens)
