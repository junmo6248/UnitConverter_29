from domain.constants import FEET_TO_METER, YARD_TO_METER


class ConversionRegistry:
    def __init__(self) -> None:
        self._to_meter = {
            "meter": 1.0,
            "feet": FEET_TO_METER,
            "yard": YARD_TO_METER,
        }

    def is_registered(self, unit: str) -> bool:
        return unit in self._to_meter

    def all_units(self) -> list[str]:
        return list(self._to_meter.keys())

    def get_to_meter_factor(self, unit: str) -> float:
        return self._to_meter[unit]
