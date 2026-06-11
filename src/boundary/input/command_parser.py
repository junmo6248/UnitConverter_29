import re

from boundary.input.commands import ConvertCommand, RegisterCommand
from boundary.input.errors import ParseError
from boundary.input.input_parser import InputParser

_REGISTER_PREFIX = re.compile(
    r"^1\s+(?P<unit>\S+)\s*=\s*(?P<factor>[\d.]+)\s+meter\s*$",
    re.IGNORECASE,
)
_OUTPUT_FORMATS = frozenset({"json", "csv", "text"})


class InputCommandParser:
    def __init__(self, convert_parser: InputParser | None = None) -> None:
        self._convert_parser = convert_parser or InputParser()

    def parse(self, raw: str) -> ConvertCommand | RegisterCommand:
        stripped = raw.strip()

        if stripped.startswith("register:"):
            return self._parse_register_colon(stripped)

        natural = _REGISTER_PREFIX.match(stripped)
        if natural:
            return RegisterCommand(
                unit=natural.group("unit"),
                to_meter_factor=float(natural.group("factor")),
            )

        format_prefix = self._parse_format_prefix(stripped)
        if format_prefix is not None:
            output_format, unit, value_str = format_prefix
            return ConvertCommand(
                unit=unit, value_str=value_str, format=output_format
            )

        unit, value_str = self._convert_parser.parse(stripped)
        return ConvertCommand(unit=unit, value_str=value_str)

    def _parse_format_prefix(
        self, raw: str
    ) -> tuple[str, str, str] | None:
        parts = raw.split(":", 2)
        if len(parts) != 3:
            return None

        output_format, unit, value_str = parts
        if output_format not in _OUTPUT_FORMATS or not unit or not value_str:
            return None

        return output_format, unit, value_str

    def _parse_register_colon(self, raw: str) -> RegisterCommand:
        parts = raw.split(":", 2)
        if len(parts) != 3 or not parts[1] or not parts[2]:
            raise ParseError(
                "Invalid register format. Use register:unit:factor "
                "(ex: register:cubit:0.4572)"
            )

        _, unit, factor_str = parts
        try:
            factor = float(factor_str)
        except ValueError as exc:
            raise ParseError(f"Invalid number: {factor_str}") from exc

        return RegisterCommand(unit=unit, to_meter_factor=factor)
