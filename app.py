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
    "private_key_id": "c256b416f66b8624cc7e437bd11e80cda9da812a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC+zehOu7oERM2I\n5W3XIrGxCUP9I3s57nKaRZ0bOaQU9r/aGn9spQmpBJPS1Xz73MSTBXX8d4risefR\nLsQRLyl4dC7ufd1JUylMpJCF0xuX+LM2s2jwmi+pO3v6AVDzFH1NJADjOfEuBaDX\nDLI0gnrF6/mjFX30+mmwrK9iZnjIzdzPjuz9dXJCQIEdSEnW1bZyZjxFRpGHSfMr\nD3LJkNXdk+hM9ZiddlM4pkb+GsLtUFE2VQhSLRJwJtrBuRe0/0jtkmZ67dG160rc\nWaAx9QDhZ0IT2sy991sXBAFvjtC7nHST/IcPmo9EEiJB7cfFffqY0XHxPM+hKhA9\n0L3WOAHhAgMBAAECggEACAPcS1plcQJ249ZHa+8gKcCq43pXFdLna4WbGOat9td6\nra3JRoYURs5Ta1reejIG6+ohz64x3l38z/O39sTVaCLxScFtx0PAC2EqVQTONu8S\nkCyvLtQ7Rk+iYJknjl6A+PmXM/ReJkHERORapAwLHj9QaEJh3SWbxPksEOUfE8hH\nS6whR4/y7wzZhMXsIGk8QQiPl0PyBLjOXMg0RRSDNSpKuidAQE5OOb7QfJQDAmOV\n87MZv3QjVqShDGqfaC9JdwjHVgOX/Z9kePBFYcl50ySZy3HKhc9Vl82FQNLuDed7\nf8yLIJ9PooDrDRDbmXDfcK06S3mRpWW0mfV83oH7lQKBgQD+CIHto6KKb1Q3d6E2\nCkjokVnxZ5EEMFHRTbH8P0Zl9w+ZWQL1l6g1aTHQh+NJbgxD7ohJLq3ik5WOWAkX\n3p91gpVra27koH58QICRexd9EEyb7t2oAPySUgHqxwZVuGR49JXgWv7ZbfhrLusC\nnOWM0X31Gku+psrR4jjO4J4JQwKBgQDASBSgh71JLxh/bhjQEln4WawtICWT+RDz\n34tNUcX+TBucvmNNa6t5lhOjnj+yLvXotYXBCjbcSM9xsodhH054KlZ+wL2B8JDI\n/6ZBY1+8e5tx+SLmeOy0k/395B9SHNV4M87mM68fBk+BJFC5+NkRS8YldQlTSFuG\nLUbFBYQ0CwKBgEukxuO3dUAZtI8rvUJ1P46ZMZozx7fil4pmw1gkk1brgaadHcd5\n2GnHIEFDJYgJD/fugICiOL8eSUtwpYyJCxyXvNyWyhekPuXK4z3u1Gi2QMmyECjl\n2k/LwaxihV1jIe/ujO6Yygh+uZlZCDvn8mbDPumMYf+sdPqYjWf09Lo3AoGAdyl0\nlxPoS72DGh36BKEK3u171a9xemXFis2EABPodzNlfVtEIUvTxhMq8qB06xFNVr2A\nOeUBoL0CynyQh7EmKTRbzEvYZfnXUKmWuDlEsIOODzEN3vUcBMEejETe4D18UfUR\niPqI0dpQVUFTQh2lMKHcF4STlehmyB2xGRLVHocCgYA4PPhthOPGlYd5JL1Og+tu\n9n495NSwWTAi+mNjfK5/steYGQw9Qrag8JxUNtaT/vNQWQtHEcg7XtNp15FLXlU+\ng8zyjuyTGD/38yuKn18MLEGA/NyPnfKgppbYlqPaWk6qKCmSAqOoK0gGrX51H5TU\nOH5y8MF95X5xQ/dBXxfEcA==\n-----END PRIVATE KEY-----\n",
    "client_email": "once-92@new1-440719.iam.gserviceaccount.com",
    "client_id": "118139536468258384459",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/once-92%40new1-440719.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
  }


# Authentication using embedded JSON data
credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO)
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
