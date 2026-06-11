import json
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path: Path | None = None) -> None:
        self._config_path = config_path or self.default_config_path()

    @staticmethod
    def default_config_path() -> Path:
        return Path(__file__).resolve().parent.parent.parent / "config" / "units.json"

    def load_units_to_meter(self) -> dict[str, float]:
        data = json.loads(self._config_path.read_text(encoding="utf-8"))
        units = data["units_to_meter"]
        return {unit: float(factor) for unit, factor in units.items()}
