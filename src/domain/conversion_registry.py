class ConversionRegistry:
    def __init__(self) -> None:
        self._units = {"meter", "feet", "yard"}

    def is_registered(self, unit: str) -> bool:
        return unit in self._units
