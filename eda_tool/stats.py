import math
from typing import List, Dict, Any


class ColumnProfiler:
    @staticmethod
    def calculate_numeric_summary(values: List[float]) -> Dict[str, Any]:
        """Calculates mean, median, variance, std dev, IQR, and identifies outliers."""
        n = len(values)
        if n == 0:
            return {}

        sorted_vals = sorted(values)
        total = sum(sorted_vals)
        mean = total / n

        # Variance & Standard Deviation
        variance = sum((x - mean) ** 2 for x in sorted_vals) / n if n > 1 else 0.0
        std_dev = math.sqrt(variance)

        # Median & Quartiles
        def get_percentile(data: List[float], p: float) -> float:
            idx = int(p * (len(data) - 1))
            return data[idx]

        q1 = get_percentile(sorted_vals, 0.25)
        median = get_percentile(sorted_vals, 0.50)
        q3 = get_percentile(sorted_vals, 0.75)
        iqr = q3 - q1

        # Outlier Detection (Tukey's Fences)
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = [x for x in sorted_vals if x < lower_bound or x > upper_bound]

        return {
            "count": n,
            "min": round(sorted_vals[0], 2),
            "max": round(sorted_vals[-1], 2),
            "mean": round(mean, 2),
            "median": round(median, 2),
            "variance": round(variance, 2),
            "std_dev": round(std_dev, 2),
            "iqr": round(iqr, 2),
            "outlier_count": len(outliers)
        }

    @staticmethod
    def calculate_categorical_summary(values: List[str]) -> Dict[str, Any]:
        """Calculates frequency distributions and cardinality."""
        n = len(values)
        if n == 0:
            return {}

        freq_map: Dict[str, int] = {}
        for val in values:
            freq_map[val] = freq_map.get(val, 0) + 1

        sorted_freq = sorted(freq_map.items(), key=lambda x: x[1], reverse=True)
        mode = sorted_freq[0][0] if sorted_freq else None

        return {
            "count": n,
            "unique_values": len(freq_map),
            "mode": mode,
            "top_3_frequencies": sorted_freq[:3]
        }