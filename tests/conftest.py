import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

TESTS = Path(__file__).resolve().parent
if str(TESTS) not in sys.path:
    sys.path.insert(0, str(TESTS))


@pytest.fixture
def config_loader():
    from infrastructure.config_loader import ConfigLoader

    return ConfigLoader()


@pytest.fixture
def conversion_registry(config_loader):
    from domain.conversion_registry import ConversionRegistry

    return ConversionRegistry(config_loader=config_loader)


@pytest.fixture
def input_validator(conversion_registry):
    from domain.input_validator import InputValidator

    return InputValidator(conversion_registry)


@pytest.fixture
def length_converter(conversion_registry):
    from domain.length_converter import LengthConverter

    return LengthConverter(conversion_registry)


@pytest.fixture
def input_parser():
    from boundary.input.input_parser import InputParser

    return InputParser()
