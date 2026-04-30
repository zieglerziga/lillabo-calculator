"""ASCII preview from physical cm lengths (MVP polyline raster)."""

from __future__ import annotations

from lillabo_calculator.geometry import CURVE_PIECE_ANGLE, PhysicalSpec, TopologySpec, physical_length_cm
from lillabo_calculator.inventory import PieceToken
from lillabo_calculator.solution import Solution
from lillabo_calculator.state import move_cursor


def _hand(token: PieceToken) -> int:
    return TopologySpec.curve_hand(token)


def _phys_length(token: PieceToken, phys: PhysicalSpec) -> float:
    return physical_length_cm(token, phys)


def render_ascii(solution: Solution, phys: PhysicalSpec, *, width: int = 72, height: int = 28) -> str:
    x, y, ang = 0.0, 0.0, 0.0
    pts: list[tuple[float, float]] = [(x, y)]
    for tok in solution.tokens:
        length = _phys_length(tok, phys)
        h = _hand(tok)
        pa = CURVE_PIECE_ANGLE if h != 0 else 0.0
        x, y, ang = move_cursor(x, y, ang, length, pa, h)
        pts.append((x, y))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    pad = 1.0
    minx -= pad
    maxx += pad
    miny -= pad
    maxy += pad
    w = max(maxx - minx, 1e-6)
    hgt = max(maxy - miny, 1e-6)

    grid = [[" " for _ in range(width)] for _ in range(height)]

    def plot(ix: int, iy: int, ch: str) -> None:
        if 0 <= ix < width and 0 <= iy < height:
            if grid[iy][ix] == " ":
                grid[iy][ix] = ch

    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        steps = int(max(abs(x1 - x0), abs(y1 - y0)) / (w / width) * 2) + 5
        for s in range(steps + 1):
            t = s / steps
            px = x0 + (x1 - x0) * t
            py = y0 + (y1 - y0) * t
            ix = int((px - minx) / w * (width - 1))
            iy = int((maxy - py) / hgt * (height - 1))
            plot(ix, iy, "#")

    return "\n".join("".join(row) for row in grid)
