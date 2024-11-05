import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Dimension, Metric
from datetime import datetime, timedelta

# Load Google Analytics property ID and JSON credentials from secrets
PROPERTY_ID = st.secrets["general"]["PROPERTY_ID"]  # Ensure this is defined in your secrets.toml
JSON_FILE = st.secrets["GOOGLE_CREDENTIALS"]  # Assuming you've stored your JSON credentials here

# Authentication
credentials = service_account.Credentials.from_service_account_info(JSON_FILE)
client = BetaAnalyticsDataClient(credentials=credentials)

# Function to get real-time active users and country data
def get_realtime_active_users():
    request = RunRealtimeReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
    )
    response = client.run_realtime_report(request)

    user_data = []
    for row in response.rows:
        country = row.dimension_values[0].value
        active_users = int(row.metric_values[0].value)
        user_data.append({"Country": country, "Active Users": active_users, "Timestamp": datetime.now()})

    return user_data

# Embed Google Analytics tracking code
GA_TRACKING_ID = st.secrets["GA_TRACKING_ID"]  # Add this to your secrets.toml
st.markdown(f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_TRACKING_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA_TRACKING_ID}');
</script>
""", unsafe_allow_html=True)

# Store data history for the last 30 minutes
data_history = []

st.title("Real-Time Active Users by Country")

# Refresh data manually
if st.button("Refresh Data"):
    # Fetch new data
    new_data = get_realtime_active_users()

    # Append new data to history
    data_history.extend(new_data)

    # Filter history to only keep data from the last 30 minutes
    cutoff = datetime.now() - timedelta(minutes=30)
    data_history = [entry for entry in data_history if entry["Timestamp"] >= cutoff]

    # Convert history to DataFrame
    df = pd.DataFrame(data_history)

    if not df.empty:
        # Main Graph: Bar chart showing active users per country in the last 30 minutes
        fig_bar = px.bar(df, x="Country", y="Active Users", color="Country",
                         title="Active Users by Country Over the Last 30 Minutes",
                         labels={"Active Users": "Active Users"}, height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Secondary Graph: Histogram for active users in the last 5 minutes
        cutoff_5min = datetime.now() - timedelta(minutes=5)
        recent_data = df[df["Timestamp"] >= cutoff_5min]
        if not recent_data.empty:
            fig_hist = px.histogram(recent_data, x="Country", y="Active Users",
                                    color="Country", title="Active Users in the Last 5 Minutes by Country",
                                    labels={"Active Users": "Active Users"}, height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.write("No active users data in the last 5 minutes.")
    else:
        st.write("No active user data available for the last 30 minutes.")

# Add a metric for the total number of unique active users throughout the day
if data_history:
    df_day = pd.DataFrame(data_history)
    total_users = df_day["Active Users"].sum()  # Summing all active users over the day
    st.metric("Total Active Users Today", total_users)
