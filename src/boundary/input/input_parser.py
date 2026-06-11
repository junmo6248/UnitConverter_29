from boundary.input.errors import ParseError


class InputParser:
    def parse(self, raw: str) -> tuple[str, str]:
        if ":" not in raw:
            raise ParseError("Invalid format. Use unit:value (ex: meter:2.5)")

        unit, value_str = raw.split(":", 1)
        return unit, value_str
