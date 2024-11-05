import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Dimension, Metric
from datetime import datetime, timedelta
import json

# Google Analytics setup
PROPERTY_ID = "465906322"

# Authentication using secrets
google_credentials = GOOGLE_CREDENTIALS = """
{
  "type": "service_account",
  "project_id": "new1-440719",
  "private_key_id": "cffbdff96fe6932e6900bbaf40b1641ede593575",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDJcsu1n0R0D1yU\n9trjOYaJOL82pgbcpS/5P4z3iHCkYtTqWM9Dlu8YgSGt8lBxrD+e9w0h+bIXMLpt\noyX4p/ajYvmjxvX0SsM2U1QvDI8HOLHN5gL/7/Phmd97Nb/1kjNoMRzVDnDUBjws\nH5vgrEK3BaxwKV1NxA+diIVn/I/u6RicnBw0v4tf1Zmyq6Q1Xj0kd9syJuDYzgN/\nEPPMYGHHqgJ32rvzBV4lv/QKawtg78V+jKwB3zKSznPTaoNgaa/Cp7PkWnbGV0Z4\nCki56riKiMyPfaZ3XnwNBbgGus9m8Mr366n48NkfpdRX317q5o8pAWMeT5bWCHO3\noWYKfiz7AgMBAAECggEAMCJlaX7mYOMAyLlZYPzwWB5+lgTC0/sGhQR53vWzkJvq\n6xoQYEKS2+STExi4vwic5RN8CFe9BYyHp0XZ/1nG9ZBjPQ5/24D3tyXfEiTqkhuq\nZJvmsJf5yri1LSARP5DRBr7heEksjYT14McmvF78y/Wnl99SY5AK+SXTVp8DF18f\nTZV4udisZBPobm/dNcBzq6XcUznBtXIf33GIfSteinntygceWjLnNO8RS8sVCTT7\nQxVolo+r3TgT9SvGdFSvS8CSC5I5fRJm8sI18+hc7fYmsK0rDExYwYXg8Z34RU64\nE1Dc/gCDJAaF0ny19XFCgYwHlDeWiiC4Wq8jJEgP6QKBgQDzx/iJKmmKZZJ+7hTz\nYmvOEUfBBC9kXimoDVuXCAQFD4ncpYjElA12cDRrus0qp3CVq8rWEj19WF6yOLjj\nEc9gqRz57X7djjpn2IjZEy98nO+mQaHWjV4L1PDcABh9/X980BAvgrmJ/3Wq8NsR\nm9SNVuYQXKcjRLUSZhQIYrI8GQKBgQDTi6Qd8X0g7wKHuq9l7q/PLKpkqMEnsg5T\nyLjBc1GA9Pb80EUggVod31eXZwM2jfZKO3RcM68KdbkhhYLm3vw00lD24/7/uU/i\nB2sgP2IIz6Ou8VcJ+3zN3KuDndQ8+PPtTU2fYKcxGilIIM1RExYYTWCk/ZYx3r7A\n49VZN+RUMwKBgAt3zcZOG3bqPlEATDYC3EVuZKy80KntEBKaxkM9mkrOp1Kc6uks\nedGnh5/Fwt8Nz2sLENivNPtPi+zgZDoyXUoTyowrUvuDNFYsRovHrkUzcMamccGR\nFuqBku8WhhBvO28Yrpo9kRLf1J49BGE4rnATtXDxmt863TXHXYvjcLUJAoGAJjzJ\nb3glC/zn0izWY3Bfau1B52vxbgFrQY24h48Wnl6o/k2PES8QYPHr3TwLgqLqb8SL\nZdcZvqRE0GBXpu+LWujhJZ9UiliurcZ1gKC0Ua9mgMqy1uUUTAmlHuc6Y8MEJFKi\nwzovPlriN11mf08Z4U6rN2d27JC8nhUQjU3jAa0CgYEAgwUd4ECGNxnliEUFOc93\nL3mlXEaSv+k773U8NMqX61WCbODiCQwq+zR9JEXFYBoci6W6s5qtKXKe3SwHAMKV\nshXfxeJXlIv0C+iL1WJh1k2nO63gRg5BR6fNwuv7MG7h6CZSe8wkf86EN3a5TevT\nXp+zWeRVszYlGqk24jbqUl0=\n-----END PRIVATE KEY-----\n",
  "client_email": "demo-303@new1-440719.iam.gserviceaccount.com",
  "client_id": "111570280622118416726",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/demo-303%40new1-440719.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""
credentials_info = json.loads(google_credentials)  # Parse the JSON string
credentials = service_account.Credentials.from_service_account_info(credentials_info)
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




st.write(st.secrets)
