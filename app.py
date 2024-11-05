import streamlit as st
import json
from google.oauth2 import service_account
from google.analytics.data import BetaAnalyticsDataClient

# Load the Google service account credentials from Streamlit secrets
try:
    credentials_info = json.loads(st.secrets["google_service_account"]["json"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = BetaAnalyticsDataClient(credentials=credentials)
except json.JSONDecodeError as e:
    st.error(f"Error decoding JSON: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")
