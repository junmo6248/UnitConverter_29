from infrastructure.config_loader import ConfigLoader


class ConversionRegistry:
    def __init__(
        self,
        units_to_meter: dict[str, float] | None = None,
        config_loader: ConfigLoader | None = None,
    ) -> None:
        if units_to_meter is not None:
            self._to_meter = dict(units_to_meter)
        else:
            loader = config_loader or ConfigLoader()
            self._to_meter = loader.load_units_to_meter()

    def is_registered(self, unit: str) -> bool:
        return unit in self._to_meter

    def all_units(self) -> list[str]:
        return list(self._to_meter.keys())

    def get_to_meter_factor(self, unit: str) -> float:
        return self._to_meter[unit]

    def register(self, unit: str, to_meter_factor: float) -> None:
        self._to_meter[unit] = to_meter_factor
