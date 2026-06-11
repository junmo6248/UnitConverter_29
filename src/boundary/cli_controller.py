from boundary.input.commands import ConvertCommand, RegisterCommand
from boundary.input.command_parser import InputCommandParser
from boundary.output.output_format_factory import OutputFormatterFactory

from application.convert_length_use_case import ConvertRequest
from application.register_unit_use_case import RegisterRequest


class CliController:
    def __init__(
        self,
        command_parser: InputCommandParser,
        use_case,
        register_use_case,
        format_factory: OutputFormatterFactory | None = None,
    ) -> None:
        self._command_parser = command_parser
        self._use_case = use_case
        self._register_use_case = register_use_case
        self._format_factory = format_factory or OutputFormatterFactory()

    def run_once(self, raw_input: str) -> str:
        command = self._command_parser.parse(raw_input)

        if isinstance(command, RegisterCommand):
            response = self._register_use_case.execute(
                RegisterRequest(
                    unit=command.unit,
                    to_meter_factor=command.to_meter_factor,
                )
            )
            return response.error or response.message or ""

        response = self._use_case.execute(
            ConvertRequest(unit=command.unit, value_str=command.value_str)
        )

        if response.error:
            return response.error

        formatter = self._format_factory.create(command.format)
        return formatter.format(
            response.source_unit, response.source_value, response.results
        )
