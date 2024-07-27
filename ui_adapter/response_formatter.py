import json
from typing import Dict, Any

class ResponseFormatter:
    @staticmethod
    def format_json(data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=2)

    @staticmethod
    def format_html(data: Dict[str, Any]) -> str:
        html = "<ul>"
        for key, value in data.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        html += "</ul>"
        return html

    @staticmethod
    def format_plain_text(data: Dict[str, Any]) -> str:
        return "\n".join([f"{key}: {value}" for key, value in data.items()])

    @staticmethod
    def format_response(data: Dict[str, Any], format_type: str = "json") -> str:
        if format_type == "json":
            return ResponseFormatter.format_json(data)
        elif format_type == "html":
            return ResponseFormatter.format_html(data)
        elif format_type == "plain":
            return ResponseFormatter.format_plain_text(data)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")