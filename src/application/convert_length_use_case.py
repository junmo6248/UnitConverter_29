from dataclasses import dataclass


@dataclass
class ConvertRequest:
    unit: str
    value: float


@dataclass
class ConvertResponse:
    source_unit: str
    source_value: float
    results: dict[str, float]
    error: str | None = None
