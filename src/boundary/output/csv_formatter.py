from boundary.output.output_formatter import OutputFormatter


class CsvFormatter(OutputFormatter):
    def format(
        self, source_unit: str, source_value: float, results: dict[str, float]
    ) -> str:
        lines = ["source_unit,source_value,result_unit,result_value"]
        for unit in sorted(results.keys()):
            value = results[unit]
            lines.append(f"{source_unit},{source_value},{unit},{value}")
        return "\n".join(lines)
