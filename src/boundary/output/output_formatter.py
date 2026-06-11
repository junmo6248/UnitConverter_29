from abc import ABC, abstractmethod


class OutputFormatter(ABC):
    @abstractmethod
    def format(
        self, source_unit: str, source_value: float, results: dict[str, float]
    ) -> str:
        pass
