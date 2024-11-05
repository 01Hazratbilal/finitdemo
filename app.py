import os
import json
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient
import streamlit as st
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Dimension, Metric
from datetime import datetime

PROPERTY_ID = "465906322"

# Load credentials from environment variable
@st.cache_resource
def load_credentials():
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if credentials_json is None:
        st.error("Google credentials are not set in the environment variables.")
        return None
    try:
        credentials_info = json.loads(credentials_json)
        return service_account.Credentials.from_service_account_info(credentials_info)
    except json.JSONDecodeError:
        st.error("Failed to decode Google credentials JSON.")
        return None

# Authentication
credentials = load_credentials()
if credentials:
    client = BetaAnalyticsDataClient(credentials=credentials)
else:
    st.error("Failed to load credentials. Check your configuration.")

# Function to get real-time active users
def get_realtime_active_users():
    if 'client' not in locals():
        st.error("Client not initialized. Check credentials.")
        return []
    
    request = RunRealtimeReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
    )
    
    try:
        response = client.run_realtime_report(request)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

    user_data = []
    for row in response.rows:
        country = row.dimension_values[0].value
        active_users = int(row.metric_values[0].value)
        user_data.append({"Country": country, "Active Users": active_users, "Timestamp": datetime.now()})

    return user_data

# Streamlit app layout
st.title("Real-Time Active Users by Country")
if st.button("Refresh Data"):
    new_data = get_realtime_active_users()
    st.write(new_data)
