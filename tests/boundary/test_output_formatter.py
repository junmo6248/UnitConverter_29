import json

import pytest

from _approval import assert_matches_golden, format_json_output_golden, format_text_output_golden
from boundary.output.csv_formatter import CsvFormatter
from boundary.output.json_formatter import JsonFormatter
from boundary.output.text_formatter import TextFormatter


def test_text_formatter_line_output():
    # Test ID: T-UI-003 | TextFormatter | 변환 결과 dict → 줄 단위 텍스트
    formatter = TextFormatter()
    results = {"meter": 2.5, "feet": 8.2021, "yard": 2.734025}

    output = formatter.format("meter", 2.5, results)

    assert output == (
        "2.5 meter = 2.5 meter\n"
        "2.5 meter = 8.2021 feet\n"
        "2.5 meter = 2.734025 yard"
    )

    assert_matches_golden("T-UI-003", format_text_output_golden(output))


def test_json_formatter_valid_json():
    # Test ID: T-UI-004 | JsonFormatter | 변환 결과 dict → 유효한 JSON
    formatter = JsonFormatter()
    results = {"meter": 2.5, "feet": 8.2021}

    output = formatter.format("meter", 2.5, results)
    parsed = json.loads(output)

    assert parsed["source"] == {"unit": "meter", "value": 2.5}
    assert parsed["results"] == results

    assert_matches_golden("T-UI-004", format_json_output_golden(parsed))


def test_csv_formatter_csv_output():
    # Test ID: T-UI-010 | CsvFormatter | 변환 결과 dict → CSV
    formatter = CsvFormatter()
    results = {"meter": 2.5, "feet": 8.2021, "yard": 2.734025}

    output = formatter.format("meter", 2.5, results)

    assert output == (
        "source_unit,source_value,result_unit,result_value\n"
        "meter,2.5,feet,8.2021\n"
        "meter,2.5,meter,2.5\n"
        "meter,2.5,yard,2.734025"
    )

    assert_matches_golden("T-UI-010", format_text_output_golden(output))
