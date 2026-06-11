import pytest

from domain.conversion_registry import ConversionRegistry
from domain.length_converter import LengthConverter


def test_meter_is_registered(conversion_registry):
    # Test ID: T-LOGIC-011 | ConversionRegistry | meter 등록 확인
    assert conversion_registry.is_registered("meter") is True


def test_register_cubit_enables_conversion():
    # Test ID: T-LOGIC-005 | ConversionRegistry | register("cubit", 0.4572) → cubit 변환 가능
    pytest.fail("RED skeleton T-LOGIC-005")


def test_register_cubit_makes_unit_registered(conversion_registry):
    # Test ID: T-LOGIC-012 | ConversionRegistry | register 후 is_registered
    conversion_registry.register("cubit", 0.4572)

    assert conversion_registry.is_registered("cubit") is True
