import os
import streamlit as st
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title="DineSafe Toronto Map", layout="wide")
st.title("DineSafe Toronto - Inspection Heatmap")

conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))


@st.cache_data
def load_data():
    query = """
        SELECT
            f.INSPECTION_DATE,
            f.INSPECTION_STATUS,
            f.INFRACTION_TYPE,
            f.INFRACTION_SEVERITY,
            f.AMOUNT_FINED,
            d.ESTABLISHMENT_ID,
            d.ESTABLISHMENT_NAME,
            d.ESTABLISHMENT_ADDRESS,
            d.LATITUDE,
            d.LONGITUDE
        FROM ANALYTICS_ZONE_DB.DINESAFE_MARTS.FACT_INSPECTIONS f
        JOIN ANALYTICS_ZONE_DB.DINESAFE_MARTS.DIM_ESTABLISHMENTS d
            ON f.ESTABLISHMENT_ID = d.ESTABLISHMENT_ID
        WHERE d.LATITUDE IS NOT NULL
          AND d.LONGITUDE IS NOT NULL
          AND d.LATITUDE != 0
          AND d.LONGITUDE != 0
    """
    return conn.query(query)


with st.spinner("Loading inspection data..."):
    df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

# Search bar
search = st.sidebar.text_input("Search establishment name")

# Inspection status filter
statuses = sorted(df["INSPECTION_STATUS"].dropna().unique())
selected_statuses = st.sidebar.multiselect(
    "Inspection Status", statuses, default=statuses
)

# Severity filter
severities = sorted(df["INFRACTION_SEVERITY"].dropna().unique())
selected_severities = st.sidebar.multiselect(
    "Infraction Severity", severities, default=severities
)

# Date range filter
min_date = pd.to_datetime(df["INSPECTION_DATE"]).min()
max_date = pd.to_datetime(df["INSPECTION_DATE"]).max()
date_range = st.sidebar.date_input(
    "Inspection Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Apply Filters
filtered = df.copy()
filtered["INSPECTION_DATE"] = pd.to_datetime(filtered["INSPECTION_DATE"])

if search:
    filtered = filtered[
        filtered["ESTABLISHMENT_NAME"].str.contains(search, case=False, na=False)
    ]

filtered = filtered[filtered["INSPECTION_STATUS"].isin(selected_statuses)]
filtered = filtered[
    filtered["INFRACTION_SEVERITY"].isin(selected_severities)
    | filtered["INFRACTION_SEVERITY"].isna()
]

if len(date_range) == 2:
    start, end = date_range
    filtered = filtered[
        (filtered["INSPECTION_DATE"] >= pd.Timestamp(start))
        & (filtered["INSPECTION_DATE"] <= pd.Timestamp(end))
    ]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Inspections", f"{len(filtered):,}")
col2.metric("Unique Establishments", f"{filtered['ESTABLISHMENT_ID'].nunique():,}")
col3.metric(
    "Conditional Passes",
    f"{len(filtered[filtered['INSPECTION_STATUS'] == 'Conditional Pass']):,}",
)
col4.metric("Total Fines", f"${filtered['AMOUNT_FINED'].sum():,.0f}")

# Map
st.subheader("Violation Heatmap")

if filtered.empty:
    st.warning("No data matches the current filters.")
else:
    map_data = filtered[["LATITUDE", "LONGITUDE", "INFRACTION_SEVERITY"]].dropna()
    # Weight: Crucial=3, Significant=2, Minor=1
    weight_map = {"C - Crucial": 3, "S - Significant": 2, "M - Minor": 1}
    map_data = map_data.copy()
    map_data["weight"] = map_data["INFRACTION_SEVERITY"].map(weight_map).fillna(0.5)

    layer = pdk.Layer(
        "HeatmapLayer",
        data=map_data,
        get_position=["LONGITUDE", "LATITUDE"],
        get_weight="weight",
        radius_pixels=30,
        intensity=1,
        threshold=0.1,
    )

    view_state = pdk.ViewState(
        latitude=43.7,
        longitude=-79.4,
        zoom=10.5,
        pitch=0,
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# Data Table
st.subheader("Inspection Details")
st.dataframe(
    filtered[
        [
            "ESTABLISHMENT_NAME",
            "ESTABLISHMENT_ADDRESS",
            "INSPECTION_DATE",
            "INSPECTION_STATUS",
            "INFRACTION_SEVERITY",
            "INFRACTION_TYPE",
            "AMOUNT_FINED",
        ]
    ]
    .sort_values("INSPECTION_DATE", ascending=False)
    .head(500),
    use_container_width=True,
)

# Refresh button
if st.sidebar.button("Refresh Data"):
    load_data.clear()
    st.rerun()
