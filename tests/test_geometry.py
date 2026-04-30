import math

from lillabo_calculator.geometry import (
    L2_CM,
    default_physical_spec,
    default_topology_spec,
    physical_length_cm,
)
from lillabo_calculator.inventory import PieceToken


def test_l2_is_unit_topology() -> None:
    topo = default_topology_spec()
    assert topo.l2 == 1.0
    assert abs(topo.l1 - 24.0 / L2_CM) < 1e-9


def test_bridge_topology_not_physical_sum() -> None:
    topo = default_topology_spec(bridge_unit=2.0)
    assert topo.b1 == 2.0
    assert abs(topo.b1 - (24.0 + 20.5) / L2_CM) > 0.1


def test_curve_chord_matches_jgc() -> None:
    topo = default_topology_spec()
    expected = 2.0 * math.sin(math.pi / 8)
    assert abs(topo.curve_chord - expected) < 1e-9


def test_forward_for_tokens() -> None:
    topo = default_topology_spec()
    assert topo.forward_for(PieceToken.L2) == 1.0
    assert topo.forward_for(PieceToken.B1) == 2.0
    assert topo.forward_for(PieceToken.CW) == topo.curve_chord
    assert topo.forward_for(PieceToken.CCW) == topo.curve_chord


def test_physical_spec_x1_is_modeled_explicitly() -> None:
    phys = default_physical_spec()
    assert phys.x1.length_cm == 14.0
    assert phys.x1.width_cm == 10.8
    assert phys.x1.width_cm > phys.s1.width_cm
    assert phys.x1.length_cm < phys.s1.length_cm


def test_physical_length_mapping_for_solver_tokens() -> None:
    phys = default_physical_spec()
    assert physical_length_cm(PieceToken.L1, phys) == phys.l1.length_cm
    assert physical_length_cm(PieceToken.L2, phys) == phys.l2.length_cm
    assert physical_length_cm(PieceToken.S1, phys) == phys.s1.length_cm
    assert physical_length_cm(PieceToken.B1, phys) == phys.b1.length_cm
    assert physical_length_cm(PieceToken.CW, phys) == phys.l2.length_cm
    assert physical_length_cm(PieceToken.CCW, phys) == phys.l2.length_cm
