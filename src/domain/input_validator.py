from domain.errors import ValidationError


class InputValidator:
    def validate(self, unit: str, value_str: str) -> None:
        value = float(value_str)
        if value < 0:
            raise ValidationError("Negative value not allowed")
