# Automated EDA & Statistical Profiling Toolkit

An automated command-line toolkit for Exploratory Data Analysis (EDA) built in pure Python. It parses structured tabular datasets, dynamically infers schema types, computes rigorous descriptive statistical distributions without external heavy mathematical libraries, and generates Markdown reporting summaries.

## Features
- **Dynamic Type Inference:** Distinguishes between categorical and continuous numerical distributions.
- **Pure-Python Statistics:** Computes five-number summaries, standard deviation, interquartile range (IQR), and Tukey's fence outlier diagnostics.
- **Reporting:** Generates production-ready Markdown summaries with frequency charts.

## Setup & Running
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run profiling tool on any CSV file:
python -m eda_tool path/to/your/data.csv

# Run tests:
pytest