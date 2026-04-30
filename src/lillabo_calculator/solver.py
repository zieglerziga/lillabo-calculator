"""Backtracking enumerator for closed loops using every piece once."""

from __future__ import annotations

from collections import Counter

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
            if is_closed(start, state):
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
