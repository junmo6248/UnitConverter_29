import pytest

from boundary.text_formatter import TextFormatter


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


def test_json_formatter_valid_json():
    # Test ID: T-UI-004 | JsonFormatter | 변환 결과 dict → 유효한 JSON
    pytest.fail("RED skeleton T-UI-004")
