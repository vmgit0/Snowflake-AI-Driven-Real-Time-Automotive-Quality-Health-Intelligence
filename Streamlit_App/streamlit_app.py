import streamlit as st
from snowflake.snowpark.context import get_active_session


# Snowflake Session

session = get_active_session()

st.set_page_config(
    page_title="AI-Driven EV Health & Failure Intelligence",
    layout="wide"
)


# Title

st.title("🚗 AI-Driven Real-Time EV Health & Failure Intelligence")
st.markdown("**Predict • Detect • Explain • Prevent**")


# Sidebar Filters

st.sidebar.header("🔎 Filters")

risk_level = st.sidebar.selectbox(
    "Failure Risk Level",
    ["ALL", "HIGH_RISK_NEXT_30_DAYS", "MEDIUM_RISK"]
)

anomaly_type = st.sidebar.selectbox(
    "Anomaly Type",
    ["ALL", "BATTERY_DEGRADATION", "MOTOR_OVERSTRESS", "USAGE_OVERLOAD"]
)


# Executive Summary

st.header("📊 Executive Quality Summary")

summary_df = session.sql("""
    SELECT
        TOTAL_EVENTS,
        TOTAL_ANOMALIES,
        AVG_FAILURE_PROBABILITY,
        HIGH_RISK_VEHICLES
    FROM EV_EXECUTIVE_QUALITY_SUMMARY
""").to_pandas()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Telemetry Events", int(summary_df.TOTAL_EVENTS[0]))
col2.metric("Detected Anomalies", int(summary_df.TOTAL_ANOMALIES[0]))
col3.metric("Avg Failure Risk", round(summary_df.AVG_FAILURE_PROBABILITY[0], 2))
col4.metric("High-Risk Vehicles (30 Days)", int(summary_df.HIGH_RISK_VEHICLES[0]))


# Failure Risk Forecast Table

st.header("⚠️ Failure Risk Forecast (Next 30 Days)")

risk_query = """
    SELECT
        EVENT_TIMESTAMP,
        FAILURE_RISK_LEVEL,
        RUL,
        FAILURE_PROBABILITY
    FROM EV_FAILURE_FORECAST_30D
"""

if risk_level != "ALL":
    risk_query += f" WHERE FAILURE_RISK_LEVEL = '{risk_level}'"

risk_query += " ORDER BY FAILURE_PROBABILITY DESC LIMIT 100"

risk_df = session.sql(risk_query).to_pandas()
st.dataframe(risk_df, use_container_width=True)

# Failure Risk Distribution Chart
st.header("📊 Failure Risk Distribution")

risk_chart_df = session.sql("""
    SELECT FAILURE_RISK_LEVEL, COUNT(*) AS CNT
    FROM EV_FAILURE_FORECAST_30D
    GROUP BY FAILURE_RISK_LEVEL
""").to_pandas()

st.bar_chart(risk_chart_df.set_index("FAILURE_RISK_LEVEL"))

# Anomaly Distribution Chart

st.header("📈 Anomaly Distribution")

anomaly_chart_df = session.sql("""
    SELECT ANOMALY_TYPE, COUNT(*) AS CNT
    FROM EV_ANOMALIES
    WHERE IS_ANOMALY = 1
    GROUP BY ANOMALY_TYPE
""").to_pandas()

st.bar_chart(anomaly_chart_df.set_index("ANOMALY_TYPE"))

# AI Predictive Maintenance Agent

st.header("🛠️ AI Predictive Maintenance Recommendations")

maint_df = session.sql("""
    SELECT
        EVENT_TIMESTAMP,
        FAILURE_RISK_LEVEL,
        MAINTENANCE_RECOMMENDATION
    FROM EV_PREDICTIVE_MAINTENANCE_AGENT
    LIMIT 10
""").to_pandas()

for _, row in maint_df.iterrows():
    st.markdown(f"""
    **🕒 {row.EVENT_TIMESTAMP}**  
    **Risk Level:** {row.FAILURE_RISK_LEVEL}  
    🧠 *{row.MAINTENANCE_RECOMMENDATION}*
    ---
    """)


# AI Quality Monitoring Agent

st.header("🧪 AI Quality Monitoring Insights")

quality_query = """
    SELECT
        EVENT_TIMESTAMP,
        ANOMALY_TYPE,
        AI_QUALITY_INSIGHT
    FROM EV_QUALITY_MONITORING_AGENT
"""

if anomaly_type != "ALL":
    quality_query += f" WHERE ANOMALY_TYPE = '{anomaly_type}'"

quality_query += " LIMIT 10"

quality_df = session.sql(quality_query).to_pandas()

for _, row in quality_df.iterrows():
    st.markdown(f"""
    **🕒 {row.EVENT_TIMESTAMP}**  
    **Anomaly:** {row.ANOMALY_TYPE}  
    🧠 *{row.AI_QUALITY_INSIGHT}*
    ---
    """)


# AI Root Cause Analysis Agent

st.header("🔍 AI Root Cause Analysis")

rca_query = """
    SELECT
        EVENT_TIMESTAMP,
        ANOMALY_TYPE,
        ROOT_CAUSE_ANALYSIS
    FROM EV_ROOT_CAUSE_AGENT
"""

if anomaly_type != "ALL":
    rca_query += f" WHERE ANOMALY_TYPE = '{anomaly_type}'"

rca_query += " LIMIT 5"

rca_df = session.sql(rca_query).to_pandas()

for _, row in rca_df.iterrows():
    st.markdown(f"""
    **🕒 {row.EVENT_TIMESTAMP}**  
    **Anomaly:** {row.ANOMALY_TYPE}  
    🧠 *{row.ROOT_CAUSE_ANALYSIS}*
    ---
    """)


# Footer

st.markdown("---")
st.markdown("🚀 **Built on Snowflake using SQL & Cortex AI**")
