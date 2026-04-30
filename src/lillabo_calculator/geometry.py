"""Dual-layer geometry: topology (closure search) vs physical cm (rendering)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lillabo_calculator.inventory import PieceToken

L2_CM = 20.5
L1_CM = 24.0
S1_CM = 14.5
B1_CM = 43.5
X1_L_CM = 14.0
X1_W_CM = 10.8
STRAIGHT_W_CM = 4.0

_CURVE_RAD = math.pi / 4
CURVE_PIECE_ANGLE = math.pi / 8


@dataclass(frozen=True)
class PhysicalRow:
    length_cm: float
    width_cm: float


@dataclass(frozen=True)
class TopologySpec:
    l1: float
    l2: float
    s1: float
    b1: float
    curve_chord: float
    bridge_unit: float

    def forward_for(self, token: PieceToken) -> float:
        from lillabo_calculator.inventory import PieceToken as T

        if token is T.L1:
            return self.l1
        if token is T.L2:
            return self.l2
        if token is T.S1:
            return self.s1
        if token is T.B1:
            return self.bridge_unit * self.l2
        if token in (T.CW, T.CCW):
            return self.curve_chord
        raise TypeError(token)

    @staticmethod
    def curve_hand(token: PieceToken) -> int:
        from lillabo_calculator.inventory import PieceToken as T

        if token is T.CCW:
            return 1
        if token is T.CW:
            return -1
        return 0


@dataclass(frozen=True)
class PhysicalSpec:
    l1: PhysicalRow
    l2: PhysicalRow
    s1: PhysicalRow
    b1: PhysicalRow
    x1: PhysicalRow


def default_topology_spec(*, bridge_unit: float = 2.0) -> TopologySpec:
    l2 = 1.0
    l1 = L1_CM / L2_CM * l2
    s1 = S1_CM / L2_CM * l2
    chord = 2.0 * l2 * math.sin(_CURVE_RAD / 2)
    return TopologySpec(
        l1=l1,
        l2=l2,
        s1=s1,
        b1=bridge_unit * l2,
        curve_chord=chord,
        bridge_unit=bridge_unit,
    )


def default_physical_spec() -> PhysicalSpec:
    w = STRAIGHT_W_CM
    return PhysicalSpec(
        l1=PhysicalRow(L1_CM, w),
        l2=PhysicalRow(L2_CM, w),
        s1=PhysicalRow(S1_CM, w),
        b1=PhysicalRow(B1_CM, w),
        x1=PhysicalRow(X1_L_CM, X1_W_CM),
    )


def physical_length_cm(token: PieceToken, phys: PhysicalSpec) -> float:
    from lillabo_calculator.inventory import PieceToken as T

    if token is T.L1:
        return phys.l1.length_cm
    if token is T.L2:
        return phys.l2.length_cm
    if token is T.S1:
        return phys.s1.length_cm
    if token is T.B1:
        return phys.b1.length_cm
    if token in (T.CW, T.CCW):
        return phys.l2.length_cm
    raise TypeError(token)
