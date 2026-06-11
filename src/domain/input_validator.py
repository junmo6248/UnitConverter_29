from domain.conversion_registry import ConversionRegistry
from domain.errors import ValidationError


class InputValidator:
    def __init__(self, registry: ConversionRegistry) -> None:
        self._registry = registry

    def validate(self, unit: str, value_str: str) -> None:
        if not self._registry.is_registered(unit):
            raise ValidationError(f"Unknown unit: {unit}")

        try:
            value = float(value_str)
        except ValueError:
            raise ValidationError(f"Invalid number: {value_str}") from None

        if value < 0:
            raise ValidationError("Negative value not allowed")
