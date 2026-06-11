import pytest

from _approval import (
    assert_matches_golden,
    format_convert_all_golden,
    format_registered_golden,
    format_single_unit_golden,
)
from domain.conversion_registry import ConversionRegistry
from domain.length_converter import LengthConverter


def test_meter_is_registered(conversion_registry):
    # Test ID: T-LOGIC-011 | ConversionRegistry | meter 등록 확인
    assert conversion_registry.is_registered("meter") is True

    assert_matches_golden(
        "T-LOGIC-011", format_registered_golden("meter", True)
    )


def test_register_cubit_enables_conversion(conversion_registry):
    # Test ID: T-LOGIC-005 | ConversionRegistry | register("cubit", 0.4572) → cubit 변환 가능
    conversion_registry.register("cubit", 0.4572)
    converter = LengthConverter(conversion_registry)

    results = converter.convert_all(1, "cubit")

    assert results["meter"] == pytest.approx(0.4572)

    assert_matches_golden(
        "T-LOGIC-005", format_single_unit_golden("meter", results["meter"])
    )
    # Test ID: T-LOGIC-012 | ConversionRegistry | register 후 is_registered
    conversion_registry.register("cubit", 0.4572)

    assert conversion_registry.is_registered("cubit") is True

    assert_matches_golden(
        "T-LOGIC-012", format_registered_golden("cubit", True)
    )
