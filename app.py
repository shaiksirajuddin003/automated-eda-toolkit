import streamlit as st
import pandas as pd
from pathlib import Path
from eda_tool.stats import ColumnProfiler

st.set_page_config(
    page_title="DataPulse | Automated EDA & Statistical Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .hero-container {
        background: radial-gradient(circle at top left, #1e1e38 0%, #0e1117 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(120deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        line-height: 1.5;
    }

    .badge-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 4px 10px;
        border-radius: 20px;
        margin-bottom: 0.6rem;
    }

    .tag-numeric {
        background: rgba(96, 165, 250, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(96, 165, 250, 0.3);
    }

    .tag-cat {
        background: rgba(244, 114, 182, 0.15);
        color: #f472b6;
        border: 1px solid rgba(244, 114, 182, 0.3);
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }

    div[data-testid="stExpander"] {
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        margin-bottom: 1rem !important;
        background: rgba(255, 255, 255, 0.015);
    }
</style>
""", unsafe_allow_html=True)

# Top Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">DataPulse Studio</div>
    <div class="hero-subtitle">
        Automated exploratory data analysis, dynamic schema inference, Tukey's outlier fences, and pure-Python distribution modeling.
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Design
st.sidebar.markdown("### 🎛️ Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload CSV Dataset", type=["csv"], help="Upload any structured tabular CSV.")
use_sample = st.sidebar.toggle("Use Sample Dataset", value=(uploaded_file is None))

df = None
file_name = ""

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    file_name = uploaded_file.name
elif use_sample:
    sample_path = Path("C:/Users/Nabeel/web-scraper-etl-pipeline/data/processed/quotes.csv")
    if sample_path.exists():
        df = pd.read_csv(sample_path)
        file_name = "quotes.csv"
    else:
        df = pd.DataFrame({
            "record_id": list(range(1, 13)),
            "category": ["Technology", "Finance", "Technology", "Healthcare", "Finance", "Technology", "Retail", "Finance", "Retail", "Healthcare", "Tech", "Finance"],
            "word_count": [14, 22, 19, 18, 25, 12, 145, 20, 16, 21, 19, 23],  # 145 is an outlier
            "char_count": [85, 130, 110, 95, 145, 75, 870, 115, 90, 120, 105, 135]
        })
        file_name = "benchmark_quotes.csv"

if df is not None:
    # High-level Statistics row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Records", f"{df.shape[0]:,}")
    with c2:
        st.metric("Total Features", df.shape[1])
    with c3:
        missing_count = int(df.isna().sum().sum())
        st.metric("Missing Values", missing_count)
    with c4:
        kb_size = round(df.memory_usage().sum() / 1024, 2)
        st.metric("Memory Ingested", f"{kb_size} KB")

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Inspection Filter
    with st.expander("🔍 Interactive Data Inspection", expanded=False):
        filter_col, search_col = st.columns([1, 3])
        with filter_col:
            selected_col = st.selectbox("Search Target", ["All Columns"] + list(df.columns))
        with search_col:
            query = st.text_input("Filter Records", placeholder="Type keywords, numbers, or tags...")

        if query:
            if selected_col == "All Columns":
                filtered = df[df.astype(str).apply(lambda r: r.str.contains(query, case=False).any(), axis=1)]
            else:
                filtered = df[df[selected_col].astype(str).str.contains(query, case=False, na=False)]
            st.dataframe(filtered, use_container_width=True)
        else:
            st.dataframe(df.head(20), use_container_width=True)

    st.markdown("### 📊 Statistical Profiling & Anomaly Detection")

    report_lines = [
        f"# Automated EDA Report: `{file_name}`",
        f"- **Total Rows:** {df.shape[0]}",
        f"- **Total Columns:** {df.shape[1]}",
        f"- **Missing Cells:** {missing_count}",
        "",
        "## Feature Analysis",
        ""
    ]

    for col in df.columns:
        series = df[col].dropna()

        is_numeric = False
        try:
            numeric_vals = [float(x) for x in series]
            is_numeric = True
        except ValueError:
            is_numeric = False

        if is_numeric and len(numeric_vals) > 0:
            stats = ColumnProfiler.calculate_numeric_summary(numeric_vals)

            with st.expander(f"📈  {col}", expanded=True):
                st.markdown('<span class="badge-tag tag-numeric">Continuous Numerical</span>', unsafe_allow_html=True)

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Mean", stats["mean"])
                k2.metric("Median", stats["median"])
                k3.metric("Std Deviation", stats["std_dev"])
                k4.metric("Outliers Flagged", stats["outlier_count"])

                left, right = st.columns([1, 1.4])
                with left:
                    summary_df = pd.DataFrame({
                        "Metric": ["Count", "Min", "Max", "Variance", "IQR", "Outlier Count"],
                        "Value": [
                            stats["count"], stats["min"], stats["max"],
                            stats["variance"], stats["iqr"], stats["outlier_count"]
                        ]
                    })
                    st.dataframe(summary_df, use_container_width=True, hide_index=True)

                with right:
                    st.caption("Distribution Profile")
                    st.area_chart(series.reset_index(drop=True), color="#60a5fa")

            report_lines.append(f"### Column: `{col}` (NUMERIC)")
            for k, v in stats.items():
                report_lines.append(f"- **{k.capitalize()}:** {v}")
            report_lines.append("")

        else:
            cat_vals = [str(x) for x in series]
            stats = ColumnProfiler.calculate_categorical_summary(cat_vals)

            with st.expander(f"🗂️  {col}", expanded=False):
                st.markdown('<span class="badge-tag tag-cat">Categorical String</span>', unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)
                c1.metric("Total Count", stats.get("count", 0))
                c2.metric("Unique Classes", stats.get("unique_values", 0))
                c3.metric("Mode (Frequent)", str(stats.get("mode", "N/A")))

                top_freq = stats.get("top_3_frequencies", [])
                if top_freq:
                    st.caption("Frequency Breakdown")
                    freq_df = pd.DataFrame(top_freq, columns=["Category", "Occurrences"])

                    chart_col, table_col = st.columns([1.5, 1])
                    with chart_col:
                        st.bar_chart(freq_df.set_index("Category"), color="#f472b6")
                    with table_col:
                        st.dataframe(freq_df, use_container_width=True, hide_index=True)

            report_lines.append(f"### Column: `{col}` (CATEGORICAL)")
            report_lines.append(f"- **Count:** {stats.get('count', 0)}")
            report_lines.append(f"- **Unique Cardinality:** {stats.get('unique_values', 0)}")
            report_lines.append(f"- **Mode:** {stats.get('mode', 'N/A')}")
            report_lines.append("")

    st.markdown("---")
    st.markdown("### 📥 Deliverables & Export")
    d1, d2 = st.columns(2)

    with d1:
        st.download_button(
            label="📄 Download Statistical Audit (.md)",
            data="\n".join(report_lines),
            file_name=f"{file_name}_EDA_AUDIT.md",
            mime="text/markdown",
            use_container_width=True
        )

    with d2:
        st.download_button(
            label="📊 Download Clean Dataset (.csv)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"cleaned_{file_name}",
            mime="text/csv",
            use_container_width=True
        )