import pytest

from domain.errors import ValidationError


def test_negative_value_returns_validation_failure(input_validator):
    # Test ID: T-LOGIC-003 | InputValidator | value < 0 → 검증 실패
    with pytest.raises(ValidationError):
        input_validator.validate("meter", "-1")


def test_unregistered_unit_inch_returns_validation_failure():
    # Test ID: T-LOGIC-004 | InputValidator | unit inch (미등록) → 검증 실패
    pytest.fail("RED skeleton T-LOGIC-004")


def test_invalid_number_abc_returns_validation_failure():
    # Test ID: T-LOGIC-006 | InputValidator | meter:abc → 숫자 변환 실패
    pytest.fail("RED skeleton T-LOGIC-006")
