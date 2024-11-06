import streamlit as st
import os
import pandas as pd
import json
import plotly.express as px
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunRealtimeReportRequest, Dimension, Metric
from datetime import datetime, timedelta

# Set page configuration to wide layout
st.set_page_config(page_title="Finit Demo Dashboard", layout="wide")

# Google Analytics setup
PROPERTY_ID = "465906322"

# Retrieve the Google credentials as a JSON string from environment variables
google_credentials = os.environ.get('google_credentials')


# Parse the JSON string into a dictionary
credentials_info = json.loads(google_credentials)
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Instantiate the Google Analytics client
client = BetaAnalyticsDataClient(credentials=credentials)


# Caching the Google Analytics Request for 30 seconds to avoid redundant calls
@st.cache_data(ttl=30)
def get_realtime_active_users():
    try:
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
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Store data history in session state for persistence
if 'data_history' not in st.session_state:
    st.session_state['data_history'] = []


st.title("Demo Dashboard to See Active users all Around the World.")
st.write("---")

# Refresh data manually
if st.button("Refresh Data"):
    # Fetch new data
    new_data = get_realtime_active_users()

    # Append new data to history
    if new_data:
        st.session_state['data_history'].extend(new_data)

    # Filter history to only keep data from the last 30 minutes
    cutoff = datetime.now() - timedelta(minutes=30)
    st.session_state['data_history'] = [entry for entry in st.session_state['data_history'] if entry["Timestamp"] >= cutoff]

    # Convert history to DataFrame
    df = pd.DataFrame(st.session_state['data_history'])

    # Display the total number of unique active users today
    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            total_users = df["Active Users"].sum()
            st.metric("Total Active Users Today", total_users)
        with col2:
            peak_users = df["Active Users"].max()
            st.metric("Peak Active Users in Last 30 Minutes", peak_users)
    else:
        st.write("No active user data available for today.")

    # If data exists, plot the graphs
    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            # Main Graph: Bar chart showing active users per country in the last 30 minutes
            fig_bar = px.bar(df, x="Country", y="Active Users", color="Country",
                            title="Active Users by Country Over the Last 30 Minutes",
                            labels={"Active Users": "Active Users"}, height=400)
            fig_bar.update_traces(hovertemplate="Country: %{x}<br>Active Users: %{y}")
            st.plotly_chart(fig_bar, use_container_width=True)

        with col2:
            # Histogram for active users in the last 5 minutes
            cutoff_5min = datetime.now() - timedelta(minutes=5)
            recent_data = df[df["Timestamp"] >= cutoff_5min]
            if not recent_data.empty:
                fig_hist = px.histogram(recent_data, x="Country", y="Active Users",
                                        color="Country", title="Active Users in the Last 5 Minutes by Country",
                                        labels={"Active Users": "Active Users"}, height=400)
                fig_hist.update_traces(hovertemplate="Country: %{x}<br>Active Users: %{y}")
                st.plotly_chart(fig_hist, use_container_width=True)
            else:
                st.write("No active users data in the last 5 minutes.")

    # Creating a choropleth map with specified height and width
        fig_choropleth = px.choropleth(df, 
                                        locations="Country", 
                                        locationmode='country names', 
                                        color="Active Users",
                                        title="Active Users by Country",
                                        color_continuous_scale=px.colors.sequential.Plasma)

        # Update layout to set height and width
        fig_choropleth.update_layout(height=600, width=1300)  # Set height and width in pixels

        st.plotly_chart(fig_choropleth, use_container_width=False)  # Use container width set to False

    else:
        st.write("No active user data available for the last 30 minutes.")
