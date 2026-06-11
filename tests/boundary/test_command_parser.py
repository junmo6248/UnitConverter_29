import pytest

from boundary.input.command_parser import InputCommandParser
from boundary.input.commands import ConvertCommand, RegisterCommand
from boundary.input.errors import ParseError


@pytest.fixture
def command_parser():
    return InputCommandParser()


def test_register_colon_format_parses_register_command(command_parser):
    # Test ID: T-UI-011 | InputCommandParser | register:cubit:0.4572
    command = command_parser.parse("register:cubit:0.4572")

    assert isinstance(command, RegisterCommand)
    assert command.unit == "cubit"
    assert command.to_meter_factor == pytest.approx(0.4572)


def test_natural_register_format_parses_register_command(command_parser):
    # Test ID: T-UI-012 | InputCommandParser | 1 cubit = 0.4572 meter
    command = command_parser.parse("1 cubit = 0.4572 meter")

    assert isinstance(command, RegisterCommand)
    assert command.unit == "cubit"
    assert command.to_meter_factor == pytest.approx(0.4572)


def test_convert_format_still_parses_convert_command(command_parser):
    command = command_parser.parse("meter:2.5")

    assert isinstance(command, ConvertCommand)
    assert command.unit == "meter"
    assert command.value_str == "2.5"
    assert command.format == "text"


def test_invalid_register_colon_raises_parse_error(command_parser):
    with pytest.raises(ParseError):
        command_parser.parse("register:cubit")
