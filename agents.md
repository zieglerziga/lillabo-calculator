# Agent Guide

## Project overview

`lillabo-calculator` is a Python 3.13 proof-of-concept CLI that enumerates simple,
closed planar LILLABO-style track loops. It uses each inventory piece exactly
once. The solver uses unitless topology lengths; the ASCII renderer uses the
physical centimetre dimensions.

The package uses a `src/` layout:

- `src/lillabo_calculator/cli.py` — `lillabo` argparse entry point.
- `runner.py` — validates input, runs enumeration, deduplicates and formats output.
- `inventory.py` — piece tokens, inventory validation and golden inventory helpers.
- `geometry.py` — topology and physical specifications and piece lengths.
- `state.py` — turtle-state transitions and closure checks.
- `solver.py` — bounded backtracking enumeration and self-intersection rejection.
- `dedup.py` / `layout_code.py` — canonical layout codes and transform-invariant deduplication.
- `ascii_render.py` — MVP polyline preview.
- `tests/` — unit, CLI, canonicalization and smoke tests.

## Setup

Use Python 3.13 or newer. A local editable development install is:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

There are no runtime dependencies. The `dev` extra provides pytest.

## Verification

Run the normal test suite with:

```bash
pytest
```

The expensive golden-inventory smoke test can be excluded with:

```bash
pytest -m "not slow"
```

The CLI package entry point is `lillabo`:

```bash
lillabo --l1 0 --l2 0 --s1 0 --b1 0 --cw 8 --ccw 0 --max-solutions 10
```

## CLI and domain constraints

- Default CLI mode enables `--strict-golden`, requiring `l1=1`, `l2=2`, `s1=2`, `b1=4`, and `cw+ccw=24`; all-zero input is also valid.
- Use `--no-strict-golden` for exploratory inventories.
- `--max-solutions` limits distinct results after canonical deduplication.
- `--max-nodes` bounds backtracking work; increase it deliberately for deeper searches.
- `--bridge-unit` changes the topology-layer bridge length and is not a physical centimetre sum.
- `X1` exists in the physical model but is intentionally excluded from v1 enumeration.

## Development conventions

- Keep the topology and physical geometry layers separate.
- Preserve deterministic token ordering, canonical layout codes, and stable output; tests rely on them.
- Validate inventory changes through both unit tests and CLI behavior.
- Avoid weakening self-intersection checks or search bounds without adding targeted tests.
- Keep public behavior and the documented CLI contract synchronized with `README.md` and `pyproject.toml`.
- Do not hand-edit `.codegraph/`; regenerate it with `codegraph init` when the indexed project needs refreshing.

## Technical priorities

- Readability is the highest priority. Prefer clear names, small functions, straightforward control flow, and explicit domain logic.
- Keep implementations as simple as possible. Avoid abstractions, dependencies, clever optimizations, and premature generalization unless they clearly improve correctness or maintainability.
- Performance is not the focus. Optimize only when a measured bottleneck prevents a documented use case, and preserve the simplest readable implementation otherwise.
- Add comments for domain reasoning and non-obvious invariants, not for code that is already self-explanatory.
- Use modern, well-supported Python features while respecting the project’s Python 3.13 requirement.

## CodeGraph and token efficiency

- Use CodeGraph first when locating code, tracing behavior, or understanding relationships. Prefer `codegraph explore "<focused question>"` over broad file dumps, grep-heavy exploration, or reading unrelated files.
- Ask focused questions that name the relevant symbol, module, behavior, or test. Start with the smallest context that can answer the question and expand only when needed.
- Use CodeGraph’s blast-radius and related-test information before editing public behavior or shared domain logic.
- Keep prompts and tool output narrow: avoid repeating source already examined, exclude unrelated directories, and summarize stable findings instead of carrying large verbatim excerpts forward.
- If the repository’s `.codegraph/` index is stale after structural changes, refresh it with `codegraph init` before relying on relationship results.
- Do not initialize or index unrelated parent directories; CodeGraph should remain scoped to this repository.

## Commit messages

Use a modern open-source style based on Conventional Commits:

```text
<type>(<optional scope>): <imperative summary>
```

Prefer focused commits with a short imperative subject (usually no more than 72 characters), followed by a body only when context is needed. Use types such as `feat`, `fix`, `refactor`, `test`, `docs`, `build`, `ci`, and `chore`. Explain user-visible impact or important rationale in the body; do not put implementation trivia in the subject.

## Change checklist

Before handing off a change:

1. Run the focused tests for the affected module.
2. Run `pytest -m "not slow"`.
3. Run `pytest` when solver, canonicalization, or output behavior changes.
4. Update `README.md` when CLI flags, inventory rules, or workflows change.
