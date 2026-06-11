from dataclasses import dataclass

from application.convert_length_use_case import ConvertLengthUseCase
from application.register_unit_use_case import RegisterUnitUseCase
from boundary.cli_controller import CliController
from boundary.input.command_parser import InputCommandParser
from boundary.output.output_format_factory import OutputFormatterFactory
from domain.conversion_registry import ConversionRegistry
from domain.input_validator import InputValidator
from domain.length_converter import LengthConverter
from infrastructure.config_loader import ConfigLoader


@dataclass
class AppServices:
    registry: ConversionRegistry
    convert_use_case: ConvertLengthUseCase
    register_use_case: RegisterUnitUseCase
    controller: CliController


def create_app(config_loader: ConfigLoader | None = None) -> AppServices:
    loader = config_loader or ConfigLoader()
    registry = ConversionRegistry(config_loader=loader)
    convert_use_case = ConvertLengthUseCase(
        InputValidator(registry),
        LengthConverter(registry),
    )
    register_use_case = RegisterUnitUseCase(registry)
    controller = CliController(
        InputCommandParser(),
        convert_use_case,
        register_use_case,
        OutputFormatterFactory(),
    )
    return AppServices(
        registry=registry,
        convert_use_case=convert_use_case,
        register_use_case=register_use_case,
        controller=controller,
    )


def create_default_use_case() -> ConvertLengthUseCase:
    return create_app().convert_use_case
