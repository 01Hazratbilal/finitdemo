import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Dimension, Metric
from datetime import datetime, timedelta

# Google Analytics setup
PROPERTY_ID = "465906322"

# JSON data embedded directly (replace with your actual JSON credentials)
SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "new1-440719",
    "private_key_id": "8d97355e183af1da3c4a2053eb85c8206d5ca3b2",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDnujz6+hgQvpwI\n/7zHj3+dnYCx4gNmupmGeDi4S+Mcsh2UBWoJnmlzeTYZsD6ov3PhFMKYG5SQgjTT\nWnZ3zTvFYI8gML2YHbRIZkvUeZvRHC5cvAm5I/gCm8lSTXda9JgcUNnwQw9wsi+P\nYOgtBx52+qKAQFWgFWkE9bHiDOFRSQu7l/Ye1cFBW6FJ8aSmPCiTMkwXUB3DwS1G\n+73HxMpnRRbM7eGhVBTa+gCOfu/P3Rt8XO1IDY+k3Wrqt1O9BfQ0W9k/C6YDe10R\nhXZ+WMy8QTbbWW08uF/GkGbRs/LlI+IZ7Fvx1yF3tRcJZtE4E+l88b2AhvA8uIMF\nSljhrDt5AgMBAAECggEABLOAT7YvB/iZ/qETlyKH5q5z691Hj41lwSGOGF0VGoyu\n3Bp/rs9w2RJ34MMKLmRonoPMOTJGtrzRg1/bNe3VvS4gO+QJQKgKSOARwJnb/vzO\nSvwsn/3aZvvP9Im/oWUuHdWdFPUDVUMO2HQ77vKX8WF/K6YX0UjbPyoYkFsNtNdX\nj3dRdhvClX6cdniZw2gVp1Eb+TAYCKhMPPxRE+fXAKb1Wpa/5XqTrbfjuRTJEaLT\ne2U72/iQM1OaiqrI+uKNP8+AIEJKUP4pexbBTNCY1F39iZ4tW8JtQQgPfphDzfi9\nBK6MfM0svmEA5faEMKHwPTU9jr/IU6Z939a4xfoElQKBgQD+b9FDoW6fMxmMNQCl\noePhKuV0Z9RwttRtI30lcmZy1RNT+QSz6ZRW96e/h7kkkcf0tm8VsZAgPCJtLAXh\nY0jhLg4hOc2vdVj1t6En/iI+w82RE+s2GIW4QuKtkX9hISwpiErOjYCAG5mZPQ6a\nae2hpO+uiQ6FMSgU8GrclekZ/QKBgQDpJrQExHCsx+1GqVSflEROpY7YLH5ouucG\nx2akvd7I8o2JuuierfuPTN570kmTY3S1pPqc97jp3uRx8JALY2hcvxRON5Nfc64d\nHDN2bHcf3BYnqNbZqJyMseiCCq1P83P12DNesobzFVU3bkW7lQUsEtVajqmMvKAB\nS88dLKByLQKBgQDvFQcgc7rM4WlqNAvNl9fXp0VBIqee2k212BkqbNsToGCvEVl3\n7U60gbYg5Vn1oP6xVhP/4H+7qoX2690CsxaycWJZmkVKUAwtqEVInSZ0r+ykHIFy\nrYxJXqA91HBLRq6GwEj62kAbINQuCA+GzW67645FBQid41j0hA0GBd+pyQKBgQCQ\njc+FOSpG5foGGox+GFY1kM4813FUi7UbbdwE/je3zTLWFw2M/IAAu/8hNCMr/7jn\nui8rzSdX0TtALY+RkAOvpUT4rdpwju9/2vFJVjyRg0o1Mqhq8PCHBvMKVYZZEK9v\n2KkY6IVlB2/7WyJfCCjZx5+CcvtKZ9SomREDnJypzQKBgQDV9pArksoKSdXD58BI\n2zdsd/SuC9cRlHyQhpVBY/vYqjqxT1AUmbyfT7qh1hRg9k83TSro6wcMAm/T9yxt\n84Q1CqkeMjJW97etqYB9d7ZcDgC4uiKRNrNZ5G+hIZqo4rOQu03wl4X9usgNUnPK\nXWGr7k/bUdaWR5qpCxZ+nWMHOg==\n-----END PRIVATE KEY-----\n",
    "client_email": "once-92@new1-440719.iam.gserviceaccount.com",
    "client_id": "118139536468258384459",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/once-92%40new1-440719.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }
  

# Authentication using embedded JSON data and specifying scopes
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=["https://www.googleapis.com/auth/analytics.readonly"]
)
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
