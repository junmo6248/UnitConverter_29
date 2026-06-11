class TextFormatter:
    def format(
        self, source_unit: str, source_value: float, results: dict[str, float]
    ) -> str:
        lines = [
            f"{source_value} {source_unit} = {value} {unit}"
            for unit, value in results.items()
        ]
        return "\n".join(lines)
