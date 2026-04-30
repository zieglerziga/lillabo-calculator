# lillabo-calculator

PoC CLI (Python 3.13) that searches for **simple closed planar loops** using a fixed LILLABO-style inventory **exactly once** per piece. Topology follows the turtle model from [John Graham-Cumming’s LILLABO post](https://blog.jgc.org/2010/01/more-fun-with-toys-ikea-lillabo-train.html): straights/bridge translate along the chord direction; curves use a **45°** heading change and a chord length derived from a nominal straight unit.

## Install (local)

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

Entry point: `lillabo` (see `pyproject.toml`).

```bash
lillabo --l1 0 --l2 0 --s1 0 --b1 0 --cw 8 --ccw 0 --max-solutions 10
```

Flags:

- `--l1`, `--l2`, `--s1`, `--b1`: straight/bridge counts.
- `--cw`, `--ccw`: how many of the pooled curve pieces are placed with CW vs CCW bend (same 45° family; orientation only).
- `--strict-golden` / `--no-strict-golden` (default `--strict-golden`): require the golden two-set inventory `l1=1,l2=2,s1=2,b1=4,cw+ccw=24`, while still allowing all-zero no-op input.
- `--max-solutions` (default **100**): cap on **distinct** solutions after canonical deduplication.
- `--max-nodes` (default **5_000_000**): backtracking step budget (search aborts when exceeded).
- `--bridge-unit` (default **2.0**): topology length of B1 in multiples of the L2 straight unit (closure layer), **not** L1+L2 cm.

## Golden two-set inventory (tests + docs)

| Count | ID | Description |
|------:|----|----------------|
| 1 | L1 | Long straight |
| 2 | L2 | Standard long |
| 2 | S1 | Short / crossing straight |
| 4 | B1 | Bridge |
| 24 | curves | One physical curve type; split via `--cw` + `--ccw` (must sum to 24) |

**X1** (car crossing) is documented in code (`PhysicalSpec.x1`) but **not** enumerated in v1 (SoW).

Example matching the golden multiset:

```bash
lillabo --l1 1 --l2 2 --s1 2 --b1 4 --cw 12 --ccw 12 --max-solutions 5 --max-nodes 200000
```

For exploratory non-golden runs:

```bash
lillabo --no-strict-golden --cw 8 --max-solutions 5
```

The full two-set search space is large; raise `--max-nodes` (and time) for deeper exploration.

## Topology vs physical (dual layer)

- **Topology** (`TopologySpec`): unitless lengths for closure search. L2 = **1.0**; L1/S1 scale from measured cm ratios; B1 uses `bridge_unit × L2`.
- **Physical** (`PhysicalSpec`): cm lengths/widths for ASCII preview (MVP polyline raster).

## Layout code

Space-separated tokens: `L1`, `L2`, `S1`, `B1`, `CW`, `CCW`. Output is **canonical**: clockwise walk from above, starting at the **lexicographically smallest** corner (rounded coordinates), then minimized over **rotation by 45°**, **reflection**, and **cyclic shift** (see `layout_code.py` / `dedup.py`).

## Tests

```bash
pytest
# exclude expensive smoke:
pytest -m "not slow"
```

## GitHub Actions

The repository includes four workflows:

- `CI` (`.github/workflows/ci.yml`): Ruff linting, fast pytest run (`-m "not slow"`), CLI smoke check, and package build verification.
- `Secret Scan (TruffleHog)` (`.github/workflows/secrets-trufflehog.yml`): PR/push secret scanning plus weekly full-history scan.
- `SonarCloud` (`.github/workflows/sonarcloud.yml`): pytest coverage + SonarCloud scan with quality gate wait.
- `Slow Test Suite` (`.github/workflows/nightly-slow-tests.yml`): weekly/manual full pytest run.

SonarCloud workflow prerequisites:

- Repository secret: `SONAR_TOKEN`
- Repository variables: `SONAR_ORGANIZATION`, `SONAR_PROJECT_KEY`

## License

See [LICENSE](LICENSE).
