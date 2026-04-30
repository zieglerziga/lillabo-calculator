"""Turtle state: JGC move_cursor semantics."""

from __future__ import annotations

import math
from dataclasses import dataclass

from lillabo_calculator.geometry import CURVE_PIECE_ANGLE, TopologySpec
from lillabo_calculator.inventory import PieceToken


@dataclass(frozen=True)
class TurtleState:
    x: float
    y: float
    angle: float

    def apply(self, token: PieceToken, topo: TopologySpec) -> TurtleState:
        length = topo.forward_for(token)
        h = TopologySpec.curve_hand(token)
        pa = CURVE_PIECE_ANGLE if h != 0 else 0.0
        x, y, ang = move_cursor(self.x, self.y, self.angle, length, pa, h)
        return TurtleState(x, y, ang)


def move_cursor(
    x: float,
    y: float,
    angle: float,
    length: float,
    piece_angle: float,
    h: int,
) -> tuple[float, float, float]:
    dx = length * math.cos(angle + h * piece_angle)
    dy = length * math.sin(angle + h * piece_angle)
    x2 = x + dx
    y2 = y + dy
    if h == 0:
        return x2, y2, angle
    return x2, y2, angle + 2 * h * piece_angle


def is_closed(
    start: TurtleState,
    end: TurtleState,
    *,
    pos_tol: float = 1e-4,
    ang_tol: float = 1e-4,
) -> bool:
    if math.hypot(end.x - start.x, end.y - start.y) > pos_tol:
        return False
    d = (end.angle - start.angle) % (2 * math.pi)
    if d > math.pi:
        d -= 2 * math.pi
    return abs(d) < ang_tol
