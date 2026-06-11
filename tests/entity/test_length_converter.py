import pytest


def test_meter_2_5_converts_to_all_units_accurately(length_converter):
    # Test ID: T-LOGIC-001 | LengthConverter | meter:2.5 → 3단위 변환값 정확
    results = length_converter.convert_all(2.5, "meter")

    assert results["meter"] == pytest.approx(2.5)
    assert results["feet"] == pytest.approx(8.2021, rel=1e-3)
    assert results["yard"] == pytest.approx(2.734025, rel=1e-3)


def test_feet_10_converts_to_meter_accurately():
    # Test ID: T-LOGIC-002 | LengthConverter | feet:10 → meter 3.048…
    pytest.fail("RED skeleton T-LOGIC-002")
