from application.convert_length_use_case import ConvertRequest, ConvertResponse
from boundary.input_parser import InputParser


class CliController:
    def __init__(self, parser: InputParser, use_case, formatter) -> None:
        self._parser = parser
        self._use_case = use_case
        self._formatter = formatter

    def run_once(self, raw_input: str) -> str:
        unit, value_str = self._parser.parse(raw_input)
        response = self._use_case.execute(
            ConvertRequest(unit=unit, value=float(value_str))
        )

        if response.error:
            return response.error

        return self._formatter.format(
            response.source_unit, response.source_value, response.results
        )
