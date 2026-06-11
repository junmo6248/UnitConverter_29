import pytest

from _approval import (
    assert_matches_golden,
    format_convert_all_golden,
    format_registered_golden,
    format_validation_error_golden,
    format_validation_ok_golden,
)
from domain.conversion_registry import ConversionRegistry
from domain.errors import ValidationError
from domain.length_converter import LengthConverter


def test_negative_value_returns_validation_failure(input_validator):
    # Test ID: T-LOGIC-003 | InputValidator | value < 0 → 검증 실패
    with pytest.raises(ValidationError):
        input_validator.validate("meter", "-1")

    assert_matches_golden(
        "T-LOGIC-003",
        format_validation_error_golden("negative_value", "meter", "-1"),
    )


def test_unregistered_unit_inch_returns_validation_failure(input_validator):
    # Test ID: T-LOGIC-004 | InputValidator | unit inch (미등록) → 검증 실패
    with pytest.raises(ValidationError):
        input_validator.validate("inch", "5")

    assert_matches_golden(
        "T-LOGIC-004",
        format_validation_error_golden("unknown_unit", "inch", "5"),
    )


def test_invalid_number_abc_returns_validation_failure(input_validator):
    # Test ID: T-LOGIC-006 | InputValidator | meter:abc → 숫자 변환 실패
    with pytest.raises(ValidationError):
        input_validator.validate("meter", "abc")

    assert_matches_golden(
        "T-LOGIC-006",
        format_validation_error_golden("invalid_number", "meter", "abc"),
    )


def test_zero_value_passes_validation(input_validator):
    # Test ID: T-LOGIC-007 | InputValidator | value 0 → 검증 통과
    input_validator.validate("meter", "0")

    assert_matches_golden(
        "T-LOGIC-007", format_validation_ok_golden("meter", "0")
    )


def test_empty_value_returns_validation_failure(input_validator):
    # Test ID: T-LOGIC-008 | InputValidator | meter: (빈 값) → 검증 실패
    with pytest.raises(ValidationError):
        input_validator.validate("meter", "")

    assert_matches_golden(
        "T-LOGIC-008",
        format_validation_error_golden("invalid_number", "meter", ""),
    )


def test_empty_unit_returns_validation_failure(input_validator):
    # Test ID: T-LOGIC-009 | InputValidator | :2.5 (빈 단위) → 검증 실패
    with pytest.raises(ValidationError):
        input_validator.validate("", "2.5")

    assert_matches_golden(
        "T-LOGIC-009",
        format_validation_error_golden("unknown_unit", "", "2.5"),
    )


def test_valid_input_passes_validation(input_validator):
    # Test ID: T-LOGIC-010 | InputValidator | meter, 2.5 → 검증 통과
    input_validator.validate("meter", "2.5")

    assert_matches_golden(
        "T-LOGIC-010", format_validation_ok_golden("meter", "2.5")
    )
