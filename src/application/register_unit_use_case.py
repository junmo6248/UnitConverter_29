from dataclasses import dataclass

from domain.conversion_registry import ConversionRegistry


@dataclass
class RegisterRequest:
    unit: str
    to_meter_factor: float


@dataclass
class RegisterResponse:
    unit: str
    to_meter_factor: float
    message: str | None = None
    error: str | None = None


class RegisterUnitUseCase:
    def __init__(self, registry: ConversionRegistry) -> None:
        self._registry = registry

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        if not request.unit:
            return RegisterResponse(
                unit=request.unit,
                to_meter_factor=request.to_meter_factor,
                error="Unknown unit: ",
            )

        if request.to_meter_factor <= 0:
            return RegisterResponse(
                unit=request.unit,
                to_meter_factor=request.to_meter_factor,
                error="Invalid factor: must be positive",
            )

        self._registry.register(request.unit, request.to_meter_factor)
        return RegisterResponse(
            unit=request.unit,
            to_meter_factor=request.to_meter_factor,
            message=(
                f"Registered: 1 {request.unit} = {request.to_meter_factor} meter"
            ),
        )
