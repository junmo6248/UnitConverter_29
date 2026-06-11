import pytest

from boundary.errors import ParseError


def test_invalid_format_without_colon_parse_fails(input_parser):
    # Test ID: T-UI-002 | InputParser | "invalid" → 파싱 실패
    with pytest.raises(ParseError):
        input_parser.parse("invalid")
