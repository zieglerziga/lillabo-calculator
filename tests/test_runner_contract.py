from lillabo_calculator.inventory import Inventory
from lillabo_calculator.runner import RunConfig, run


def test_runner_sorts_and_prints_unique_canonical_codes() -> None:
    cfg = RunConfig(
        inventory=Inventory(l1=0, l2=0, s1=2, b1=0, cw=0, ccw=8),
        max_solutions=10,
        bridge_unit=2.0,
        max_nodes=300_000,
    )
    res = run(cfg)
    assert res.solutions_printed == 2

    layout_lines = [line for line in res.text.splitlines() if line.startswith("layout_code: ")]
    codes = [line.removeprefix("layout_code: ") for line in layout_lines]

    assert len(codes) == res.solutions_printed
    assert len(codes) == len(set(codes))
    assert codes == sorted(codes)
