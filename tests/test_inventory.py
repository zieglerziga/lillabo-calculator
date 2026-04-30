import pytest

from lillabo_calculator.inventory import (
    Inventory,
    PieceToken,
    golden_two_set_inventory,
    validate_inventory,
)


def test_golden_two_set_sums() -> None:
    inv = golden_two_set_inventory(12, 12)
    assert inv.l1 == 1 and inv.l2 == 2 and inv.s1 == 2 and inv.b1 == 4
    assert inv.cw + inv.ccw == 24


def test_golden_invalid_sum() -> None:
    with pytest.raises(ValueError):
        golden_two_set_inventory(10, 10)


@pytest.mark.parametrize("field", ["l1", "l2", "s1", "b1", "cw", "ccw"])
def test_inventory_rejects_negative_counts(field: str) -> None:
    payload = {"l1": 0, "l2": 0, "s1": 0, "b1": 0, "cw": 0, "ccw": 0}
    payload[field] = -1
    with pytest.raises(ValueError, match=field):
        Inventory(**payload)


def test_validate_inventory_rejects_straights_without_curves() -> None:
    with pytest.raises(ValueError, match="curve counts are zero"):
        validate_inventory(Inventory(l1=1, l2=0, s1=0, b1=0, cw=0, ccw=0))


def test_validate_inventory_accepts_curves_only() -> None:
    validate_inventory(Inventory(l1=0, l2=0, s1=0, b1=0, cw=8, ccw=0))


def test_remaining_tokens_are_deterministically_ordered() -> None:
    inv = Inventory(l1=1, l2=1, s1=1, b1=1, cw=1, ccw=1)
    assert inv.remaining_tokens() == [
        PieceToken.L1,
        PieceToken.L2,
        PieceToken.S1,
        PieceToken.B1,
        PieceToken.CCW,
        PieceToken.CW,
    ]
