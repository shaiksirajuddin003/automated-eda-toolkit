from pathlib import Path
from typing import Dict, Any


class ReportGenerator:
    @staticmethod
    def generate_markdown(file_name: str, meta: Dict[str, Any], profiles: Dict[str, Any], output_path: Path) -> None:
        lines = [
            f"# Automated EDA Report: `{file_name}`",
            "",
            "## Dataset Overview",
            f"- **Total Rows Analyzed:** {meta['row_count']}",
            f"- **Total Columns:** {meta['column_count']}",
            "",
            "## Statistical Profiling",
            ""
        ]

        for col, stats in profiles.items():
            lines.append(f"### Column: `{col}` ({stats.get('type', 'unknown').upper()})")
            if stats["type"] == "numeric":
                lines.append("| Metric | Value |")
                lines.append("| --- | --- |")
                for k, v in stats.items():
                    if k != "type":
                        lines.append(f"| {k.replace('_', ' ').capitalize()} | {v} |")
            else:
                lines.append(f"- **Valid Count:** {stats.get('count', 0)}")
                lines.append(f"- **Unique Cardinality:** {stats.get('unique_values', 0)}")
                lines.append(f"- **Mode (Most Common):** {stats.get('mode', 'N/A')}")
                lines.append("- **Top Frequencies:**")
                for val, cnt in stats.get("top_3_frequencies", []):
                    lines.append(f"  - `{val}`: {cnt} occurrences")
            lines.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))