import json
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).parent / "golden"
GOLDEN_DECIMALS = 4


def assert_matches_golden(test_id: str, actual: str) -> None:
    slug = test_id.lower().replace("_", "-")
    path = GOLDEN_DIR / f"{slug}.approved.txt"
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    expected = path.read_text(encoding="utf-8")
    assert actual == expected, (
        f"golden mismatch: {path}\n--- expected ---\n{expected}\n--- actual ---\n{actual}"
    )


def _lines(status: str, pairs: dict[str, str]) -> str:
    lines = [status]
    for key in sorted(pairs.keys()):
        lines.append(f"{key}={pairs[key]}")
    return "\n".join(lines)


def format_convert_all_golden(results: dict[str, float]) -> str:
    pairs = {key: f"{value:.{GOLDEN_DECIMALS}f}" for key, value in results.items()}
    return _lines("ok", pairs)


def format_single_unit_golden(unit: str, value: float) -> str:
    return _lines("ok", {unit: f"{value:.{GOLDEN_DECIMALS}f}"})


def format_validation_error_golden(code: str, unit: str, value_str: str) -> str:
    return _lines("validation_error", {"code": code, "unit": unit, "value_str": value_str})


def format_validation_ok_golden(unit: str, value_str: str) -> str:
    return _lines("ok", {"unit": unit, "value_str": value_str})


def format_registered_golden(unit: str, registered: bool) -> str:
    return _lines("ok", {"registered": str(registered).lower(), "unit": unit})


def format_parse_ok_golden(unit: str, value_str: str) -> str:
    return _lines("ok", {"unit": unit, "value_str": value_str})


def format_parse_error_golden(input_str: str) -> str:
    return _lines("parse_error", {"input": input_str})


def format_text_output_golden(output: str) -> str:
    return "ok\n" + output


def format_json_output_golden(payload: dict) -> str:
    return _lines("ok", {"json": json.dumps(payload, sort_keys=True)})


def format_cli_flow_golden(result: str) -> str:
    return _lines("ok", {"result": result})


def format_factory_ok_golden(format_name: str, formatter_type: str) -> str:
    return _lines("ok", {"format": format_name, "formatter_type": formatter_type})


def format_format_error_golden(format_name: str) -> str:
    return _lines(
        "validation_error", {"code": "unsupported_format", "format": format_name}
    )


def format_convert_command_golden(
    output_format: str, unit: str, value_str: str
) -> str:
    return _lines(
        "ok", {"format": output_format, "unit": unit, "value_str": value_str}
    )
