from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from lillabo_calculator._debug_log import emit_debug_log


class PieceToken(Enum):
    """Placed piece tokens for v1 (X1 excluded from enumeration)."""

    L1 = auto()
    L2 = auto()
    S1 = auto()
    B1 = auto()
    CW = auto()
    CCW = auto()


@dataclass(frozen=True)
class Inventory:
    """Multiset of pieces to use exactly once in a closed layout."""

    l1: int
    l2: int
    s1: int
    b1: int
    cw: int
    ccw: int

    def __post_init__(self) -> None:
        for name, v in (
            ("l1", self.l1),
            ("l2", self.l2),
            ("s1", self.s1),
            ("b1", self.b1),
            ("cw", self.cw),
            ("ccw", self.ccw),
        ):
            if v < 0:
                msg = f"{name} must be non-negative, got {v}"
                raise ValueError(msg)

    @property
    def total_curves(self) -> int:
        return self.cw + self.ccw

    def remaining_tokens(self) -> list[PieceToken]:
        out: list[PieceToken] = []
        out.extend([PieceToken.L1] * self.l1)
        out.extend([PieceToken.L2] * self.l2)
        out.extend([PieceToken.S1] * self.s1)
        out.extend([PieceToken.B1] * self.b1)
        out.extend([PieceToken.CW] * self.cw)
        out.extend([PieceToken.CCW] * self.ccw)
        order = (
            PieceToken.L1,
            PieceToken.L2,
            PieceToken.S1,
            PieceToken.B1,
            PieceToken.CCW,
            PieceToken.CW,
        )
        key = {p: i for i, p in enumerate(order)}
        out.sort(key=lambda t: key[t])
        return out


def _is_zero_inventory(inv: Inventory) -> bool:
    return (inv.l1 + inv.l2 + inv.s1 + inv.b1 + inv.cw + inv.ccw) == 0


def _matches_strict_golden_inventory(inv: Inventory) -> bool:
    return (
        inv.l1 == GOLDEN_TWO_SET_L1
        and inv.l2 == GOLDEN_TWO_SET_L2
        and inv.s1 == GOLDEN_TWO_SET_S1
        and inv.b1 == GOLDEN_TWO_SET_B1
        and inv.total_curves == GOLDEN_TWO_SET_CURVES
    )


def validate_inventory(inv: Inventory, *, strict_golden: bool = False) -> None:
    # region agent log
    emit_debug_log(
        hypothesis_id="H3",
        location="inventory.py:validate_inventory",
        message="inventory_validation_called",
        data={
            "l1": inv.l1,
            "l2": inv.l2,
            "s1": inv.s1,
            "b1": inv.b1,
            "cw": inv.cw,
            "ccw": inv.ccw,
        },
    )
    # endregion
    if inv.total_curves == 0 and any(x > 0 for x in (inv.l1, inv.l2, inv.s1, inv.b1)):
        msg = "curve counts are zero but straights/bridge are present"
        raise ValueError(msg)
    if not strict_golden:
        return
    if _is_zero_inventory(inv):
        # region agent log
        emit_debug_log(
            hypothesis_id="H3",
            location="inventory.py:validate_inventory",
            message="strict_golden_zero_inventory_allowed",
            data={"strict_golden": strict_golden},
        )
        # endregion
        return
    if _matches_strict_golden_inventory(inv):
        # region agent log
        emit_debug_log(
            hypothesis_id="H3",
            location="inventory.py:validate_inventory",
            message="strict_golden_inventory_matched",
            data={"strict_golden": strict_golden},
        )
        # endregion
        return
    # region agent log
    emit_debug_log(
        hypothesis_id="H3",
        location="inventory.py:validate_inventory",
        message="strict_golden_inventory_rejected",
        data={"strict_golden": strict_golden},
    )
    # endregion
    msg = (
        "strict golden inventory requires l1=1, l2=2, s1=2, b1=4 and cw+ccw=24 "
        "(or all-zero no-op inventory)"
    )
    raise ValueError(msg)


GOLDEN_TWO_SET_L1 = 1
GOLDEN_TWO_SET_L2 = 2
GOLDEN_TWO_SET_S1 = 2
GOLDEN_TWO_SET_B1 = 4
GOLDEN_TWO_SET_CURVES = 24


def golden_two_set_inventory(cw: int = 12, ccw: int = 12) -> Inventory:
    if cw + ccw != GOLDEN_TWO_SET_CURVES:
        msg = f"cw+ccw must equal {GOLDEN_TWO_SET_CURVES}, got {cw}+{ccw}"
        raise ValueError(msg)
    return Inventory(
        l1=GOLDEN_TWO_SET_L1,
        l2=GOLDEN_TWO_SET_L2,
        s1=GOLDEN_TWO_SET_S1,
        b1=GOLDEN_TWO_SET_B1,
        cw=cw,
        ccw=ccw,
    )
