from domain.conversion_registry import ConversionRegistry


class LengthConverter:
    def __init__(self, registry: ConversionRegistry) -> None:
        self._registry = registry

    def convert_all(self, value: float, from_unit: str) -> dict[str, float]:
        base_meters = value * self._registry.get_to_meter_factor(from_unit)
        return {
            unit: base_meters / self._registry.get_to_meter_factor(unit)
            for unit in self._registry.all_units()
        }
