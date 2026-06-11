from boundary.output.csv_formatter import CsvFormatter
from boundary.output.json_formatter import JsonFormatter
from boundary.output.output_formatter import OutputFormatter
from boundary.output.text_formatter import TextFormatter

_FORMATTERS: dict[str, type[OutputFormatter]] = {
    "json": JsonFormatter,
    "csv": CsvFormatter,
    "text": TextFormatter,
}


class OutputFormatterFactory:
    def create(self, format_name: str) -> OutputFormatter:
        formatter_cls = _FORMATTERS.get(format_name)
        if formatter_cls is None:
            raise ValueError(f"Unsupported output format: {format_name}")
        return formatter_cls()
