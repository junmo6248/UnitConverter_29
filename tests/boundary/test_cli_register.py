import pytest

from _approval import assert_matches_golden, format_cli_flow_golden
from application.app_factory import create_app


def test_cli_controller_register_command_flow():
    # Test ID: T-UI-013 | CliController | register → Registry 반영
    app = create_app()

    result = app.controller.run_once("1 cubit = 0.4572 meter")

    assert result == "Registered: 1 cubit = 0.4572 meter"
    assert app.registry.is_registered("cubit")

    results = app.convert_use_case._converter.convert_all(1, "cubit")
    assert results["meter"] == pytest.approx(0.4572)

    assert_matches_golden("T-UI-013", format_cli_flow_golden(result))
