import sys
from pathlib import Path
from eda_tool.parser import DataParser
from eda_tool.stats import ColumnProfiler
from eda_tool.report import ReportGenerator


def main():
    # Looks for input argument or falls back to project 1's scraped CSV
    input_file = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path("C:/Users/Nabeel/web-scraper-etl-pipeline/data/processed/quotes.csv")
    )
    
    if not input_file.exists():
        print(f"Error: Dataset not found at {input_file}")
        return

    print(f"Parsing dataset: {input_file.name}...")
    dataset = DataParser.parse_csv(input_file)
    profiles = {}

    for col, col_type in dataset["types"].items():
        vals = dataset["data"][col]
        if col_type == "numeric":
            stats = ColumnProfiler.calculate_numeric_summary(vals)
        else:
            stats = ColumnProfiler.calculate_categorical_summary(vals)
        stats["type"] = col_type
        profiles[col] = stats

    output_report = Path("data/EDA_REPORT.md")
    ReportGenerator.generate_markdown(input_file.name, dataset, profiles, output_report)
    print(f"Report generated successfully: {output_report.resolve()}")


if __name__ == "__main__":
    main()