"""
Export formats for CacheKaro scan results.

Supports text, JSON, CSV, and HTML output formats.
"""

from cachekaro.exporters.base import Exporter, ExportFormat
from cachekaro.exporters.text import TextExporter
from cachekaro.exporters.json_export import JsonExporter
from cachekaro.exporters.csv_export import CsvExporter
from cachekaro.exporters.html_export import HtmlExporter

__all__ = [
    "Exporter",
    "ExportFormat",
    "TextExporter",
    "JsonExporter",
    "CsvExporter",
    "HtmlExporter",
]


def get_exporter(format: str) -> Exporter:
    """
    Get an exporter instance by format name.

    Args:
        format: Format name (text, json, csv, html)

    Returns:
        Exporter instance

    Raises:
        ValueError: If format is not supported
    """
    exporters = {
        "text": TextExporter,
        "json": JsonExporter,
        "csv": CsvExporter,
        "html": HtmlExporter,
    }

    format_lower = format.lower()
    if format_lower not in exporters:
        raise ValueError(
            f"Unsupported format: {format}. "
            f"Supported formats: {', '.join(exporters.keys())}"
        )

    return exporters[format_lower]()
