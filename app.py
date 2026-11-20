import streamlit as st
import pandas as pd
from queries import (
    cost_per_model,
    cost_per_day,
    average_cost_per_call,
    calls_per_day,
    average_latency_per_day,
    success_vs_error_count,
)

st.title("Observability Dashboard")

st.subheader("Cost per Model")
cost_model_data = cost_per_model()
cost_model_df = pd.DataFrame(cost_model_data, columns=["Model", "Total Cost"])
st.dataframe(cost_model_df)

st.subheader("Cost per Day")
cost_day_data = cost_per_day()
cost_day_df = pd.DataFrame(cost_day_data, columns=["Day", "Total Cost"])
cost_day_df = cost_day_df.set_index("Day")
st.line_chart(cost_day_df)

st.subheader("Average Cost per Call")
average_cost = average_cost_per_call()
st.write(f"${average_cost:.6f}")

st.header("Call Volume")

st.subheader("Calls per Day")
calls_day_data = calls_per_day()
calls_day_df = pd.DataFrame(calls_day_data, columns=["Day", "Total Calls"])
calls_day_df = calls_day_df.set_index("Day")
st.bar_chart(calls_day_df)

st.subheader("Average Latency per Day")
latency_day_data = average_latency_per_day()
latency_day_df = pd.DataFrame(
    latency_day_data, columns=["Day", "Average Latency (ms)"]
)
latency_day_df = latency_day_df.set_index("Day")
st.line_chart(latency_day_df)

latency_threshold_ms = 15_000
high_latency_days = latency_day_df[
    latency_day_df["Average Latency (ms)"] > latency_threshold_ms
]

if not high_latency_days.empty:
    high_latency_details = ", ".join(
        f"{day}: {latency:,.0f} ms"
        for day, latency in high_latency_days["Average Latency (ms)"].items()
    )
    st.error(
        f"High latency detected (above {latency_threshold_ms:,} ms): "
        f"{high_latency_details}"
    )
else:
    st.success(f"All average latencies are below {latency_threshold_ms:,} ms.")

st.subheader("Success vs Error Count")
status_count_data = success_vs_error_count()
status_count_df = pd.DataFrame(status_count_data, columns=["Status", "Total Calls"])
st.dataframe(status_count_df)
