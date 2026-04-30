"""CLI orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from lillabo_calculator.ascii_render import render_ascii
from lillabo_calculator.dedup import canonical_layout_code, unique_solutions
from lillabo_calculator.geometry import default_physical_spec, default_topology_spec
from lillabo_calculator.inventory import Inventory, validate_inventory
from lillabo_calculator.solver import enumerate_loops


@dataclass(frozen=True)
class RunConfig:
    inventory: Inventory
    max_solutions: int
    bridge_unit: float
    max_nodes: int = 5_000_000
    strict_golden: bool = False


@dataclass(frozen=True)
class RunResult:
    solutions_printed: int
    text: str


def run(cfg: RunConfig) -> RunResult:
    validate_inventory(cfg.inventory, strict_golden=cfg.strict_golden)
    if (cfg.inventory.l1 + cfg.inventory.l2 + cfg.inventory.s1 + cfg.inventory.b1 + cfg.inventory.cw + cfg.inventory.ccw) == 0:
        return RunResult(solutions_printed=0, text="")
    topo = default_topology_spec(bridge_unit=cfg.bridge_unit)
    phys = default_physical_spec()
    raw_cap = max(10_000, cfg.max_solutions * 200)
    raw = enumerate_loops(
        cfg.inventory,
        topo,
        max_solutions=raw_cap,
        max_nodes=cfg.max_nodes,
    )
    uniq = unique_solutions(raw)
    uniq.sort(key=canonical_layout_code)
    uniq = uniq[: cfg.max_solutions]
    lines: list[str] = []
    for i, sol in enumerate(uniq, start=1):
        code = canonical_layout_code(sol)
        lines.append(f"Solution {i}")
        lines.append(f"layout_code: {code}")
        lines.append(render_ascii(sol, phys))
        lines.append("")
    body = "\n".join(lines).rstrip() + ("\n" if lines else "")
    return RunResult(solutions_printed=len(uniq), text=body)
