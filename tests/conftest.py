import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture
def conversion_registry():
    from domain.conversion_registry import ConversionRegistry

    return ConversionRegistry()


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
    from boundary.input_parser import InputParser

    return InputParser()
