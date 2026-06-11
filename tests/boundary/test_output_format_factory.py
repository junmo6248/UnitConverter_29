import pytest

from _approval import (
    assert_matches_golden,
    format_factory_ok_golden,
    format_format_error_golden,
)
from boundary.output.csv_formatter import CsvFormatter
from boundary.output.json_formatter import JsonFormatter
from boundary.output.output_format_factory import OutputFormatterFactory
from boundary.output.text_formatter import TextFormatter


def test_format_factory_json_returns_json_formatter():
    # Test ID: T-UI-014 | OutputFormatterFactory | "json" → JsonFormatter
    factory = OutputFormatterFactory()

    formatter = factory.create("json")

    assert isinstance(formatter, JsonFormatter)
    assert_matches_golden(
        "T-UI-014",
        format_factory_ok_golden("json", type(formatter).__name__),
    )


def test_format_factory_csv_returns_csv_formatter():
    # Test ID: T-UI-015 | OutputFormatterFactory | "csv" → CsvFormatter
    factory = OutputFormatterFactory()

    formatter = factory.create("csv")

    assert isinstance(formatter, CsvFormatter)
    assert_matches_golden(
        "T-UI-015",
        format_factory_ok_golden("csv", type(formatter).__name__),
    )


def test_format_factory_text_returns_text_formatter():
    # Test ID: T-UI-016 | OutputFormatterFactory | "text" → TextFormatter (표 형태)
    factory = OutputFormatterFactory()

    formatter = factory.create("text")

    assert isinstance(formatter, TextFormatter)
    assert_matches_golden(
        "T-UI-016",
        format_factory_ok_golden("text", type(formatter).__name__),
    )


def test_format_factory_unknown_format_raises_error():
    # Test ID: T-UI-017 | OutputFormatterFactory | "xml" → 지원하지 않는 포맷 오류
    factory = OutputFormatterFactory()

    with pytest.raises(ValueError, match="Unsupported output format"):
        factory.create("xml")

    assert_matches_golden("T-UI-017", format_format_error_golden("xml"))
