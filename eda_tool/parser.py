import csv
from pathlib import Path
from typing import Dict, List, Any


class DataParser:
    @staticmethod
    def parse_csv(file_path: Path) -> Dict[str, Any]:
        """Reads a CSV file and profiles column types dynamically."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)

        column_data: Dict[str, List[Any]] = {h: [] for h in headers}
        for row in rows:
            for h in headers:
                column_data[h].append(row.get(h, ""))

        # Type inference: Attempt converting to float, otherwise keep as string
        inferred_types = {}
        processed_data: Dict[str, List[Any]] = {}

        for h, raw_vals in column_data.items():
            numeric_vals = []
            is_numeric = True
            
            for v in raw_vals:
                if v == "" or v is None:
                    continue
                try:
                    numeric_vals.append(float(v))
                except ValueError:
                    is_numeric = False
                    break

            if is_numeric and numeric_vals:
                inferred_types[h] = "numeric"
                processed_data[h] = numeric_vals
            else:
                inferred_types[h] = "categorical"
                processed_data[h] = [str(v) for v in raw_vals if v]

        return {
            "row_count": len(rows),
            "column_count": len(headers),
            "types": inferred_types,
            "data": processed_data
        }