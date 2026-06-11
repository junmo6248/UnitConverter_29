import json

import pytest

from _approval import (
    assert_matches_golden,
    format_convert_command_golden,
    format_json_output_golden,
    format_text_output_golden,
)
from application.app_factory import create_app
from boundary.input.command_parser import InputCommandParser
from boundary.input.commands import ConvertCommand


@pytest.fixture
def command_parser():
    return InputCommandParser()


def test_convert_command_with_json_prefix_parses_format_and_unit_value(
    command_parser,
):
    # Test ID: T-UI-018 | InputCommandParser | "json:meter:2.5" → format=json, unit=meter, value=2.5
    command = command_parser.parse("json:meter:2.5")

    assert isinstance(command, ConvertCommand)
    assert command.format == "json"
    assert command.unit == "meter"
    assert command.value_str == "2.5"
    assert_matches_golden(
        "T-UI-018",
        format_convert_command_golden("json", "meter", "2.5"),
    )


def test_convert_command_default_format_is_text_when_no_prefix(command_parser):
    # Test ID: T-UI-019 | InputCommandParser | "meter:2.5" → format=text (기본값)
    command = command_parser.parse("meter:2.5")

    assert isinstance(command, ConvertCommand)
    assert command.format == "text"
    assert command.unit == "meter"
    assert command.value_str == "2.5"
    assert_matches_golden(
        "T-UI-019",
        format_convert_command_golden("text", "meter", "2.5"),
    )


def test_cli_controller_json_format_outputs_valid_json():
    # Test ID: T-UI-020 | CliController | json:meter:2.5 → JSON 출력
    app = create_app()

    result = app.controller.run_once("json:meter:2.5")
    parsed = json.loads(result)

    assert parsed["source"] == {"unit": "meter", "value": 2.5}
    assert parsed["results"]["meter"] == pytest.approx(2.5)
    assert parsed["results"]["feet"] == pytest.approx(8.2021, rel=1e-3)
    assert_matches_golden("T-UI-020", format_json_output_golden(parsed))


def test_cli_controller_csv_format_outputs_csv_header():
    # Test ID: T-UI-021 | CliController | csv:meter:2.5 → CSV 출력
    app = create_app()

    result = app.controller.run_once("csv:meter:2.5")

    assert result.startswith(
        "source_unit,source_value,result_unit,result_value"
    )
    assert "meter,2.5,feet," in result
    assert_matches_golden("T-UI-021", format_text_output_golden(result))


def test_cli_controller_text_format_outputs_line_table():
    # Test ID: T-UI-022 | CliController | text:meter:2.5 → 표 형태 줄 출력 (기존 TextFormatter)
    app = create_app()

    result = app.controller.run_once("text:meter:2.5")

    assert "2.5 meter = 2.5 meter" in result
    assert "2.5 meter =" in result
    assert "feet" in result
    assert "yard" in result
    assert_matches_golden("T-UI-022", format_text_output_golden(result))
