import pytest

from lillabo_calculator.inventory import golden_two_set_inventory
from lillabo_calculator.runner import RunConfig, run


@pytest.mark.slow
def test_two_set_smoke_is_deterministic_and_well_formed() -> None:
    """Large search space: enforce deterministic bounded behavior."""
    cfg = RunConfig(
        inventory=golden_two_set_inventory(12, 12),
        max_solutions=5,
        bridge_unit=2.0,
        max_nodes=50_000,
    )
    first = run(cfg)
    second = run(cfg)
    assert first == second
    assert 0 <= first.solutions_printed <= cfg.max_solutions

    lines = first.text.splitlines()
    solution_headers = [line for line in lines if line.startswith("Solution ")]
    layout_lines = [line for line in lines if line.startswith("layout_code: ")]

    assert solution_headers == [f"Solution {i}" for i in range(1, first.solutions_printed + 1)]
    assert len(layout_lines) == first.solutions_printed
    assert len(layout_lines) == len(set(layout_lines))

    codes = [line.removeprefix("layout_code: ") for line in layout_lines]
    assert codes == sorted(codes)

    allowed = {"L1", "L2", "S1", "B1", "CW", "CCW"}
    for code in codes:
        assert all(token in allowed for token in code.split(" "))

    if first.solutions_printed == 0:
        assert first.text == ""
    else:
        assert first.text.endswith("\n")
