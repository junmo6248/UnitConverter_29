import pytest

from application.register_unit_use_case import RegisterRequest, RegisterUnitUseCase


def test_register_unit_adds_to_registry(conversion_registry):
    use_case = RegisterUnitUseCase(conversion_registry)

    response = use_case.execute(
        RegisterRequest(unit="cubit", to_meter_factor=0.4572)
    )

    assert response.error is None
    assert response.message == "Registered: 1 cubit = 0.4572 meter"
    assert conversion_registry.is_registered("cubit")


def test_register_then_convert_cubit(conversion_registry):
    use_case = RegisterUnitUseCase(conversion_registry)
    use_case.execute(RegisterRequest(unit="cubit", to_meter_factor=0.4572))

    from domain.length_converter import LengthConverter

    results = LengthConverter(conversion_registry).convert_all(1, "cubit")
    assert results["meter"] == pytest.approx(0.4572)
