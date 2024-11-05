import streamlit as st
from google.oauth2 import service_account

# Load Google credentials from Streamlit secrets
try:
    json_credentials = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = service_account.Credentials.from_service_account_info(json_credentials)
except KeyError:
    st.error("Google credentials are not set in the environment variables.")
    st.stop()  # Stop the execution if the secret is not found

# Initialize the client
client = BetaAnalyticsDataClient(credentials=credentials)
