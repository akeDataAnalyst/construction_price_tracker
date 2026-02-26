import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Construction Price Tracker",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme + white text
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .stSidebar { background-color: #161b22; }
    .stMarkdown, .stText, .stCaption, .stLabel, .stSelectbox > label, 
    .stSlider > label, .stCheckbox > label, .stTextInput > label {
        color: #e6edf3 !important;
    }
    .stMetric {
        background-color: #161b22;
        border-radius: 10px;
        padding: 16px;
        border: 1px solid #30363d;
        text-align: center;
    }
    .stMetric label { color: #8b949e !important; font-size: 0.95rem; }
    .stMetric .metric-value { color: #ffffff !important; font-size: 1.7rem; }
    .stTabs [data-baseweb="tab-list"] { background-color: #0d1117; border-bottom: 1px solid #30363d; }
    .stTabs [data-baseweb="tab"] { color: #c9d1d9 !important; }
    .stTabs [aria-selected="true"] { color: #58a6ff !important; border-bottom: 2px solid #58a6ff !important; }
    hr { background-color: #30363d; margin: 1.5rem 0; }
    </style>
""", unsafe_allow_html=True)

# Load data 
@st.cache_data
def load_data():
    DATA_DIR = Path("notebooks")
    patterns = ["master_prices_ml_flagged_20260218.csv", "master_prices_cleaned_20260218.csv"]
    candidates = []
    for pat in patterns:
        candidates.extend(DATA_DIR.glob(pat))
    if not candidates:
        return None, "No file found"
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    try:
        df = pd.read_csv(latest, parse_dates=['last_checked_dt', 'scraped_at'])
        return df, latest.name
    except:
        return None, "Loading error"

df, filename = load_data()

if df is None:
    st.error("Could not load data. Check notebooks/.")
    st.stop()

# Title
st.title("🏗️ Construction Materials Price Tracker")
st.caption(f"File: {filename} • {len(df)} records • Updated: {datetime.now().strftime('%Y-%m-%d %H:%M EAT')}")

# Sidebar Filters 
with st.sidebar:
    st.header("Filters")

    categories = ["All"] + sorted(df["category"].dropna().unique())
    selected_category = st.selectbox("Category", categories)

    pmin = float(df["price_etb"].min(skipna=True) or 0)
    pmax = float(df["price_etb"].max(skipna=True) or 100000)
    price_range = st.slider(
        "Price range (ETB)",
        min_value=pmin,
        max_value=pmax,
        value=(pmin, pmax),
        step=100.0
    )

    search_term = st.text_input("Search material", "").strip()

    outliers_only = st.checkbox("Show only outliers", value=False)

# Apply filters
fdf = df.copy()

if selected_category != "All":
    fdf = fdf[fdf["category"] == selected_category]

fdf = fdf[
    (fdf["price_etb"] >= price_range[0]) &
    (fdf["price_etb"] <= price_range[1])
]

if search_term:
    mask = (
        fdf["material"].str.contains(search_term, case=False, na=False) |
        fdf.get("material_clean", "").str.contains(search_term, case=False, na=False)
    )
    fdf = fdf[mask]

if outliers_only and "is_price_outlier" in fdf.columns:
    fdf = fdf[fdf["is_price_outlier"]]

# Metrics 
cols = st.columns(4)
cols[0].metric("Total Records", f"{len(df):,}")
cols[1].metric("Filtered Records", f"{len(fdf):,}")
cols[2].metric("Valid Prices", f"{df['price_etb_valid'].sum():,}")
if "is_price_outlier" in df.columns:
    out_count = df["is_price_outlier"].sum()
    out_pct = out_count / len(df) * 100
    cols[3].metric("Outliers", f"{out_count:,} ({out_pct:.1f}%)")
else:
    cols[3].metric("Outliers", "—")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📋 Data Table", "⚠️ Outliers"])

with tab1:
    colL, colR = st.columns(2)

    with colL:
        avg_df = df[df["price_etb_valid"]].groupby("category")["price_etb"].mean().reset_index()
        fig_bar = px.bar(
            avg_df.sort_values("price_etb", ascending=False),
            x="category",
            y="price_etb",
            title="Average Price by Category",
            height=480,
            template="plotly_dark"
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

    with colR:
        fig_scatter = px.scatter(
            df,
            x="days_since_update",
            y="price_etb",
            color="is_price_outlier" if "is_price_outlier" in df else None,
            hover_data=["material", "category", "unit_standard"],
            title="Price vs Data Age (Red = Outlier)",
            color_discrete_map={False: "#58a6ff", True: "#f85149"},
            height=480,
            template="plotly_dark"
        )
        fig_scatter.update_layout(yaxis_type="log")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader(f"Showing {len(fdf):,} filtered rows")

    def highlight_outliers(row):
        if row.get("is_price_outlier", False):
            return ["background-color: #3d1f1f; color: white"] * len(row)
        return ["background-color: #161b22; color: white"] * len(row)

    styled = fdf.style.format({
        "price_etb": "{:,.0f}",
        "last_checked_dt": "{:%Y-%m-%d}"
    }).apply(highlight_outliers, axis=1)

    st.dataframe(styled, use_container_width=True, hide_index=True)

    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data (CSV)",
        csv,
        f"filtered_prices_{datetime.now():%Y%m%d}.csv",
        "text/csv"
    )

with tab3:
    st.subheader("Detected Price Outliers")
    if "is_price_outlier" not in df.columns:
        st.info("No outlier flag available in this dataset.")
    else:
        out_df = df[df["is_price_outlier"]].copy()
        if out_df.empty:
            st.success("No outliers detected.")
        else:
            st.dataframe(
                out_df[["category", "material", "price_etb", "unit_standard", "last_checked_dt"]]
                .sort_values("price_etb", ascending=False)
                .style.format({"price_etb": "{:,.0f}"}),
                use_container_width=True
            )

# Footer
st.markdown("---")
st.caption("Developed by **Aklilu Abera** • Construction Materials Price Tracker Project")
