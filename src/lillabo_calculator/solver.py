"""Backtracking enumerator for closed loops using every piece once."""

from __future__ import annotations

from collections import Counter

from lillabo_calculator._debug_log import emit_debug_log
from lillabo_calculator.geometry import TopologySpec
from lillabo_calculator.inventory import Inventory, PieceToken
from lillabo_calculator.solution import Solution
from lillabo_calculator.state import TurtleState, is_closed


def _branch_tokens(counter: Counter[PieceToken]) -> list[PieceToken]:
    order = (
        PieceToken.L1,
        PieceToken.L2,
        PieceToken.S1,
        PieceToken.B1,
        PieceToken.CCW,
        PieceToken.CW,
    )
    return [t for t in order if counter[t] > 0]


def _orientation(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    *,
    eps: float,
) -> int:
    cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if abs(cross) <= eps:
        return 0
    return 1 if cross > 0 else -1


def _on_segment(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    *,
    eps: float,
) -> bool:
    return (
        min(a[0], b[0]) - eps <= c[0] <= max(a[0], b[0]) + eps
        and min(a[1], b[1]) - eps <= c[1] <= max(a[1], b[1]) + eps
    )


def _segments_intersect(
    a: tuple[float, float],
    b: tuple[float, float],
    c: tuple[float, float],
    d: tuple[float, float],
    *,
    eps: float,
) -> bool:
    o1 = _orientation(a, b, c, eps=eps)
    o2 = _orientation(a, b, d, eps=eps)
    o3 = _orientation(c, d, a, eps=eps)
    o4 = _orientation(c, d, b, eps=eps)
    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and _on_segment(a, b, c, eps=eps):
        return True
    if o2 == 0 and _on_segment(a, b, d, eps=eps):
        return True
    if o3 == 0 and _on_segment(c, d, a, eps=eps):
        return True
    if o4 == 0 and _on_segment(c, d, b, eps=eps):
        return True
    return False


def _has_self_intersection(states: list[TurtleState], *, eps: float = 1e-9) -> bool:
    if len(states) <= 3:
        return False
    pts = [(s.x, s.y) for s in states]
    seg_count = len(pts) - 1
    for i in range(seg_count):
        a, b = pts[i], pts[i + 1]
        for j in range(i + 1, seg_count):
            if abs(i - j) <= 1:
                continue
            if i == 0 and j == seg_count - 1:
                continue
            c, d = pts[j], pts[j + 1]
            if _segments_intersect(a, b, c, d, eps=eps):
                return True
    return False


def enumerate_loops(
    inv: Inventory,
    topo: TopologySpec,
    *,
    max_solutions: int,
    max_nodes: int = 5_000_000,
) -> list[Solution]:
    start = TurtleState(0.0, 0.0, 0.0)
    counter: Counter[PieceToken] = Counter(
        {
            PieceToken.L1: inv.l1,
            PieceToken.L2: inv.l2,
            PieceToken.S1: inv.s1,
            PieceToken.B1: inv.b1,
            PieceToken.CW: inv.cw,
            PieceToken.CCW: inv.ccw,
        }
    )

    out: list[Solution] = []
    nodes = 0

    def backtrack(
        state: TurtleState,
        ctr: Counter[PieceToken],
        path: list[PieceToken],
        states: list[TurtleState],
    ) -> None:
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes:
            return
        if len(out) >= max_solutions:
            return
        if sum(ctr.values()) == 0:
            closed = is_closed(start, state)
            self_intersects = _has_self_intersection(states) if path else False
            # region agent log
            emit_debug_log(
                hypothesis_id="H1_H2",
                location="solver.py:backtrack_leaf",
                message="leaf_candidate_evaluated",
                data={
                    "token_count": len(path),
                    "is_closed": closed,
                    "self_intersects": self_intersects,
                    "accepted": closed,
                },
            )
            # endregion
            accepted = bool(path) and closed and not self_intersects
            if accepted:
                # region agent log
                emit_debug_log(
                    hypothesis_id="H2",
                    location="solver.py:backtrack_leaf",
                    message="leaf_candidate_appended",
                    data={"token_count": len(path), "self_intersects": self_intersects},
                )
                # endregion
                out.append(Solution(tokens=tuple(path), states=tuple(states)))
            return
        for tok in _branch_tokens(ctr):
            nxt = state.apply(tok, topo)
            ctr[tok] -= 1
            path.append(tok)
            states.append(nxt)
            backtrack(nxt, ctr, path, states)
            states.pop()
            path.pop()
            ctr[tok] += 1
            if len(out) >= max_solutions or nodes > max_nodes:
                return

    backtrack(start, counter, [], [start])
    return out
