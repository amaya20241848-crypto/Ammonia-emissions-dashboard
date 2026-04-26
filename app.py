import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Ammonia Emissions Dashboard", layout="wide")

st.title("🌍 Ammonia Emissions from Agriculture")
st.markdown("Analyze emissions across countries and years")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Amonia_emission_from_agriculture.csv")
df.columns = df.columns.str.strip()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

country = st.sidebar.selectbox("Select Country", sorted(df["Country"].unique()))

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

# =========================
# FILTERED DATA
# =========================
filtered_df = df[
    (df["Country"] == country) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# =========================
# INSIGHT TAGS (KPIs)
# =========================
st.subheader("📊 Key Insights")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Selected Country", country)
c2.metric("Year Range", f"{year_range[0]} - {year_range[1]}")
c3.metric("Max Emissions", round(df["Value"].max(), 2))
c4.metric("Avg Emissions", round(df["Value"].mean(), 2))

# Simple interpretive insights
if filtered_df["Value"].mean() > df["Value"].mean():
    st.error("⚠ Emissions in selected range are ABOVE global average")
else:
    st.success("✔ Emissions in selected range are BELOW global average")

st.markdown("---")

# =========================
# MAIN VISUALIZATIONS
# =========================
col1, col2 = st.columns(2)

# Trend
with col1:
    st.subheader(f"Trend for {country}")
    st.line_chart(filtered_df.set_index("Year")["Value"])

# Top countries
with col2:
    st.subheader("Top 10 Countries (Latest Year)")
    latest_year = df["Year"].max()
    top_df = df[df["Year"] == latest_year].sort_values(by="Value", ascending=False).head(10)
    st.bar_chart(top_df.set_index("Country")["Value"])

# =========================
# COUNTRY COMPARISON
# =========================
st.subheader("🌍 Country Comparison")

selected_countries = st.multiselect(
    "Select countries to compare",
    df["Country"].unique(),
    default=[country]
)

compare_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

st.line_chart(compare_df.pivot(index="Year", columns="Country", values="Value"))

st.markdown("---")


# =========================
# DATA PREVIEW
# =========================
with st.expander("🔍 View Data"):
    st.dataframe(filtered_df)

# =========================
# FOOTER INSIGHTS
# =========================
st.success("Higher emissions are concentrated in top-ranked countries.")
st.warning("Emissions vary significantly across regions and years.")
st.info("Use filters to explore specific time periods and countries.")
