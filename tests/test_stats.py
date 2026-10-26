from eda_tool.stats import ColumnProfiler


def test_numeric_summary_mean_and_median():
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    summary = ColumnProfiler.calculate_numeric_summary(data)
    assert summary["mean"] == 30.0
    assert summary["median"] == 30.0
    assert summary["min"] == 10.0
    assert summary["max"] == 50.0


def test_outlier_detection():
    data = [10.0, 11.0, 12.0, 10.5, 11.5, 500.0]
    summary = ColumnProfiler.calculate_numeric_summary(data)
    assert summary["outlier_count"] >= 1