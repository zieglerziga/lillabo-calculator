from lillabo_calculator.cli import build_parser, main


def test_parser_defaults_match_cli_contract() -> None:
    args = build_parser().parse_args([])
    assert args.l1 == 0
    assert args.l2 == 0
    assert args.s1 == 0
    assert args.b1 == 0
    assert args.cw == 0
    assert args.ccw == 0
    assert args.max_solutions == 100
    assert args.max_nodes == 5_000_000
    assert args.bridge_unit == 2.0


def test_cli_negative_inventory_reports_error_to_stderr(capsys) -> None:
    rc = main(["--l1", "-1"])
    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""
    assert captured.err.startswith("error: l1 must be non-negative")


def test_cli_prints_solution_block_for_simple_octagon(capsys) -> None:
    rc = main(["--cw", "8", "--max-solutions", "1", "--max-nodes", "100000"])
    captured = capsys.readouterr()
    assert rc == 0
    assert captured.err == ""
    lines = captured.out.splitlines()
    assert lines[0] == "Solution 1"
    assert lines[1] == "layout_code: CW CW CW CW CW CW CW CW"
    assert any("#" in line for line in lines[2:])
