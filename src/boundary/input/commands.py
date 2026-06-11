from dataclasses import dataclass


@dataclass(frozen=True)
class ConvertCommand:
    unit: str
    value_str: str
    format: str = "text"


@dataclass(frozen=True)
class RegisterCommand:
    unit: str
    to_meter_factor: float
