import pytest

from boundary.output.csv_formatter import CsvFormatter
from boundary.output.json_formatter import JsonFormatter
from boundary.output.output_format_factory import OutputFormatterFactory
from boundary.output.text_formatter import TextFormatter


def test_format_factory_json_returns_json_formatter():
    # Test ID: T-UI-014 | OutputFormatterFactory | "json" → JsonFormatter
    factory = OutputFormatterFactory()

    formatter = factory.create("json")

    assert isinstance(formatter, JsonFormatter)


def test_format_factory_csv_returns_csv_formatter():
    # Test ID: T-UI-015 | OutputFormatterFactory | "csv" → CsvFormatter
    factory = OutputFormatterFactory()

    formatter = factory.create("csv")

    assert isinstance(formatter, CsvFormatter)


def test_format_factory_text_returns_text_formatter():
    # Test ID: T-UI-016 | OutputFormatterFactory | "text" → TextFormatter (표 형태)
    factory = OutputFormatterFactory()

    formatter = factory.create("text")

    assert isinstance(formatter, TextFormatter)


def test_format_factory_unknown_format_raises_error():
    # Test ID: T-UI-017 | OutputFormatterFactory | "xml" → 지원하지 않는 포맷 오류
    factory = OutputFormatterFactory()

    with pytest.raises(ValueError, match="Unsupported output format"):
        factory.create("xml")
