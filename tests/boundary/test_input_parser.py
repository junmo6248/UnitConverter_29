import pytest

from _approval import assert_matches_golden, format_parse_error_golden, format_parse_ok_golden
from boundary.input.errors import ParseError


def test_valid_meter_colon_value_parses_unit_and_value(input_parser):
    # Test ID: T-UI-001 | InputParser | "meter:2.5" → ("meter", "2.5")
    assert input_parser.parse("meter:2.5") == ("meter", "2.5")

    assert_matches_golden(
        "T-UI-001", format_parse_ok_golden("meter", "2.5")
    )


def test_invalid_format_without_colon_parse_fails(input_parser):
    # Test ID: T-UI-002 | InputParser | "invalid" → 파싱 실패
    with pytest.raises(ParseError):
        input_parser.parse("invalid")

    assert_matches_golden("T-UI-002", format_parse_error_golden("invalid"))


def test_meter_colon_empty_value_parses(input_parser):
    # Test ID: T-UI-006 | InputParser | "meter:" → ("meter", "")
    assert input_parser.parse("meter:") == ("meter", "")

    assert_matches_golden("T-UI-006", format_parse_ok_golden("meter", ""))


def test_colon_only_value_parses_empty_unit(input_parser):
    # Test ID: T-UI-007 | InputParser | ":2.5" → ("", "2.5")
    assert input_parser.parse(":2.5") == ("", "2.5")

    assert_matches_golden("T-UI-007", format_parse_ok_golden("", "2.5"))


def test_empty_string_parse_fails(input_parser):
    # Test ID: T-UI-008 | InputParser | "" → 파싱 실패
    with pytest.raises(ParseError):
        input_parser.parse("")

    assert_matches_golden("T-UI-008", format_parse_error_golden(""))


def test_multiple_colons_splits_on_first_only(input_parser):
    # Test ID: T-UI-009 | InputParser | "meter:2.5:extra" → ("meter", "2.5:extra")
    assert input_parser.parse("meter:2.5:extra") == ("meter", "2.5:extra")

    assert_matches_golden(
        "T-UI-009", format_parse_ok_golden("meter", "2.5:extra")
    )
