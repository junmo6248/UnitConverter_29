from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from application.convert_length_use_case import ConvertResponse
from boundary.cli_controller import CliController


def test_cli_controller_invokes_use_case_flow():
    # Test ID: T-UI-005 | CliController | Mock Use Case → 입력→출력 흐름
    parser = Mock()
    use_case = Mock()
    formatter = Mock()

    parser.parse.return_value = ("meter", "2.5")
    use_case.execute.return_value = ConvertResponse(
        source_unit="meter",
        source_value=2.5,
        results={"meter": 2.5, "feet": 8.2021},
    )
    formatter.format.return_value = "formatted output"

    controller = CliController(parser, use_case, formatter)
    result = controller.run_once("meter:2.5")

    parser.parse.assert_called_once_with("meter:2.5")
    use_case.execute.assert_called_once()
    formatter.format.assert_called_once_with(
        "meter", 2.5, {"meter": 2.5, "feet": 8.2021}
    )
    assert result == "formatted output"
