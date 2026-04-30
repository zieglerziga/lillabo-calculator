"""Recorded closed-loop solution."""

from __future__ import annotations

from dataclasses import dataclass

from lillabo_calculator.inventory import PieceToken
from lillabo_calculator.state import TurtleState


@dataclass(frozen=True)
class Solution:
    tokens: tuple[PieceToken, ...]
    states: tuple[TurtleState, ...]
