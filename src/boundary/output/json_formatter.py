import json

from boundary.output.output_formatter import OutputFormatter


class JsonFormatter(OutputFormatter):
    def format(
        self, source_unit: str, source_value: float, results: dict[str, float]
    ) -> str:
        payload = {
            "source": {"unit": source_unit, "value": source_value},
            "results": results,
        }
        return json.dumps(payload)
