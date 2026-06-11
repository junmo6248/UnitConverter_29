from dataclasses import dataclass

from domain.errors import ValidationError
from domain.input_validator import InputValidator
from domain.length_converter import LengthConverter


@dataclass
class ConvertRequest:
    unit: str
    value_str: str


@dataclass
class ConvertResponse:
    source_unit: str
    source_value: float
    results: dict[str, float]
    error: str | None = None


class ConvertLengthUseCase:
    def __init__(
        self,
        validator: InputValidator,
        converter: LengthConverter,
    ) -> None:
        self._validator = validator
        self._converter = converter

    def execute(self, request: ConvertRequest) -> ConvertResponse:
        try:
            self._validator.validate(request.unit, request.value_str)
        except ValidationError as exc:
            return ConvertResponse(
                source_unit=request.unit,
                source_value=0.0,
                results={},
                error=str(exc),
            )

        value = float(request.value_str)
        results = self._converter.convert_all(value, request.unit)
        return ConvertResponse(
            source_unit=request.unit,
            source_value=value,
            results=results,
        )
