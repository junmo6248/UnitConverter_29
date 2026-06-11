from unittest.mock import Mock

import pytest

from _approval import assert_matches_golden, format_cli_flow_golden
from application.convert_length_use_case import ConvertRequest, ConvertResponse
from boundary.cli_controller import CliController
from boundary.input.commands import ConvertCommand


def test_cli_controller_invokes_use_case_flow():
    # Test ID: T-UI-005 | CliController | Mock Use Case → 입력→출력 흐름
    command_parser = Mock()
    use_case = Mock()
    register_use_case = Mock()
    format_factory = Mock()
    formatter = Mock()

    command_parser.parse.return_value = ConvertCommand(unit="meter", value_str="2.5")
    use_case.execute.return_value = ConvertResponse(
        source_unit="meter",
        source_value=2.5,
        results={"meter": 2.5, "feet": 8.2021},
    )
    format_factory.create.return_value = formatter
    formatter.format.return_value = "formatted output"

    controller = CliController(
        command_parser, use_case, register_use_case, format_factory
    )
    result = controller.run_once("meter:2.5")

    command_parser.parse.assert_called_once_with("meter:2.5")
    use_case.execute.assert_called_once_with(
        ConvertRequest(unit="meter", value_str="2.5")
    )
    register_use_case.execute.assert_not_called()
    format_factory.create.assert_called_once_with("text")
    formatter.format.assert_called_once_with(
        "meter", 2.5, {"meter": 2.5, "feet": 8.2021}
    )
    assert result == "formatted output"

    assert_matches_golden("T-UI-005", format_cli_flow_golden(result))
