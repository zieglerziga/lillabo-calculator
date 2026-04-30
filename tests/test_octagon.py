import math

from lillabo_calculator.dedup import canonical_layout_code, unique_solutions
from lillabo_calculator.geometry import default_topology_spec
from lillabo_calculator.inventory import Inventory, PieceToken
from lillabo_calculator.solution import Solution
from lillabo_calculator.solver import _has_self_intersection, enumerate_loops
from lillabo_calculator.state import TurtleState


def _solution_from_vertices(
    vertices: list[tuple[float, float]],
    tokens: tuple[PieceToken, ...],
) -> Solution:
    states = [TurtleState(float(x), float(y), 0.0) for x, y in vertices]
    states.append(states[0])
    return Solution(tokens=tokens, states=tuple(states))


def _mixed_fixture_solution() -> Solution:
    vertices = [
        (0.0, 0.0),
        (2.0, 0.0),
        (3.0, 1.0),
        (3.0, 3.0),
        (2.0, 4.0),
        (0.0, 4.0),
        (-1.0, 3.0),
        (-1.0, 1.0),
    ]
    tokens = (
        PieceToken.L1,
        PieceToken.L2,
        PieceToken.S1,
        PieceToken.B1,
        PieceToken.CW,
        PieceToken.CCW,
        PieceToken.L2,
        PieceToken.B1,
    )
    return _solution_from_vertices(vertices, tokens)


def _cyclic_shift(sol: Solution, shift: int) -> Solution:
    n = len(sol.tokens)
    vertices = [(s.x, s.y) for s in sol.states[:n]]
    shifted_vertices = vertices[shift:] + vertices[:shift]
    shifted_tokens = sol.tokens[shift:] + sol.tokens[:shift]
    return _solution_from_vertices(shifted_vertices, shifted_tokens)


def _rotate(sol: Solution, radians: float) -> Solution:
    c = math.cos(radians)
    s = math.sin(radians)
    n = len(sol.tokens)
    vertices = [(st.x, st.y) for st in sol.states[:n]]
    rotated = [(c * x - s * y, s * x + c * y) for x, y in vertices]
    return _solution_from_vertices(rotated, sol.tokens)


def _reflect_with_reversed_traversal(sol: Solution) -> Solution:
    n = len(sol.tokens)
    vertices = [(st.x, st.y) for st in sol.states[:n]]
    reflected = [(x, -y) for x, y in vertices]
    return _solution_from_vertices(reflected, tuple(reversed(sol.tokens)))


def test_eight_ccw_octagon_unique() -> None:
    inv = Inventory(0, 0, 0, 0, 0, 8)
    topo = default_topology_spec()
    raw = enumerate_loops(inv, topo, max_solutions=50)
    assert len(raw) == 1
    assert len(unique_solutions(raw)) == 1
    assert canonical_layout_code(raw[0]) == " ".join(["CCW"] * 8)


def test_eight_cw_octagon_unique() -> None:
    inv = Inventory(0, 0, 0, 0, 8, 0)
    raw = enumerate_loops(inv, default_topology_spec(), max_solutions=50)
    assert len(raw) == 1
    assert canonical_layout_code(raw[0]) == " ".join(["CW"] * 8)


def test_cw_and_ccw_octagons_remain_distinct() -> None:
    ccw = enumerate_loops(Inventory(0, 0, 0, 0, 0, 8), default_topology_spec(), max_solutions=1)[0]
    cw = enumerate_loops(Inventory(0, 0, 0, 0, 8, 0), default_topology_spec(), max_solutions=1)[0]
    assert canonical_layout_code(ccw) != canonical_layout_code(cw)


def test_canonical_code_invariant_over_transform_orbit() -> None:
    base = _mixed_fixture_solution()
    variants = [
        base,
        _cyclic_shift(base, 3),
        _rotate(base, math.pi / 2),
        _reflect_with_reversed_traversal(base),
    ]
    codes = {canonical_layout_code(sol) for sol in variants}
    assert len(codes) == 1
    assert len(unique_solutions(variants)) == 1


def test_solver_returns_simple_loops_only() -> None:
    inv = Inventory(0, 0, 0, 0, 8, 8)
    raw = enumerate_loops(inv, default_topology_spec(), max_solutions=16, max_nodes=200_000)
    assert all(not _has_self_intersection(list(sol.states)) for sol in raw)
